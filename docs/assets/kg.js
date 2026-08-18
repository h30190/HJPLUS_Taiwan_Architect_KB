/* 知識圖譜動態背景。
   節點來自 data.json 的 tree（scripts/update_landing_page.py 掃 raw/ 產生），
   所以背景畫的是這個知識庫真實的分類結構，不是裝飾用的隨機粒子。

   動態分四層，疊起來才看得出「活的」：
     1. 自轉      整張圖極慢旋轉        ← V1 參數原封不動
     2. 漂移      每個節點各自呼吸      ← V1 參數原封不動
     3. 捲動視差  跟著頁面被拖著跑      ← 新增，這層最明顯
     4. 滑鼠      整張圖朝游標偏移      ← 新增（V1 只有局部推開）

   自 v1 landing page 移植，另外補了：
     · 尊重 prefers-reduced-motion（只畫一張靜態圖）
     · 離開畫面就停止繪製（IntersectionObserver）
     · 節點密度依容器面積決定，避免小區塊擠成一團
     · canvas bitmap 由 ResizeObserver 追蹤，內容撐開時不會被拉伸 */
(function () {
  'use strict';

  /* hero 有自己的照片背景，不畫圖譜；要排除其他區塊就加 .no-kg */
  var TARGETS = 'section:not(.hero):not(.no-kg), .page-head:not(.no-kg)';

  var REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var FALLBACK_TREE = [
    '建築顧問方法論', '建築法規', '建築執照', '建築性能', '建築設計與規劃',
    '建築施工與材料', '專業複委託', '公共工程', '專案管理', '經營管理', '設計軟體與工具'
  ].map(function (n) { return { name: n, children: [] }; });

  /* ── 新增動態的可調參數 ── */
  var PARALLAX = 0.22;     // 捲動視差強度：0 = 不動，1 = 跟著捲動 1:1
  var PARALLAX_MAX = 140;  // 視差位移上限（px），避免節點整批被推出畫面
  var MOUSE_SHIFT = 28;    // 整張圖跟隨游標的最大偏移（px）
  var MOUSE_EASE = 0.05;   // 跟隨緩動係數，越小越黏、越有被拖著跑的感覺

  /* ── 全站共用的輸入狀態：捲動與滑鼠各只掛一組監聽，不是每個 canvas 一份 ── */
  var pageY = window.pageYOffset || 0;
  var viewH = window.innerHeight || 800;
  var ptr = { x: -9999, y: -9999, on: false };   // viewport 座標
  var ptrN = { x: 0, y: 0 };                     // 正規化 -1 ~ 1

  window.addEventListener('scroll', function () {
    pageY = window.pageYOffset || document.documentElement.scrollTop || 0;
  }, { passive: true });

  window.addEventListener('resize', function () {
    viewH = window.innerHeight || 800;
  });

  window.addEventListener('mousemove', function (e) {
    ptr.x = e.clientX;
    ptr.y = e.clientY;
    ptr.on = true;
    ptrN.x = (e.clientX / (window.innerWidth || 1)) * 2 - 1;
    ptrN.y = (e.clientY / (viewH || 1)) * 2 - 1;
  }, { passive: true });

  document.addEventListener('mouseleave', function () {
    ptr.on = false;
    ptrN.x = ptrN.y = 0;
  });

  function dist(a, b) {
    return Math.sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
  }

  /* 依容器背景亮度決定線條與節點顏色 */
  function palette(wrap) {
    var bg = getComputedStyle(wrap).backgroundColor;
    var isDark = false;
    if (bg && bg !== 'transparent') {
      var m = bg.match(/[\d.]+/g);
      if (m && m.length >= 3) {
        var alpha = m.length >= 4 ? +m[3] : 1;
        if (alpha > 0) {
          isDark = (0.299 * +m[0] + 0.587 * +m[1] + 0.114 * +m[2]) < 128;
        }
      }
    }
    return {
      fg: isDark ? '255,255,255' : '150,150,150',
      dim: isDark ? '255,255,255' : '185,185,185',
      mul: isDark ? 1 : 1.25,
      opacity: isDark ? 0.65 : 0.6   /* V1 的值 */
    };
  }

  function initOne(wrap, tree) {
    var canvas = document.createElement('canvas');
    canvas.className = 'kg-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    wrap.classList.add('kg-host');
    wrap.insertBefore(canvas, wrap.firstChild);

    var pal = palette(wrap);
    canvas.style.opacity = String(pal.opacity);

    var ctx = canvas.getContext('2d');
    var W = 0, H = 0;
    var hostTop = 0, hostLeft = 0;   /* 文件座標，視差與游標換算都要用 */
    var nodes = [];
    var time = 0;
    var visible = false;
    var rafId = null;
    var mShift = { x: 0, y: 0 };     /* 平滑後的滑鼠偏移 */

    /* 游標改由全站監聽提供，不再依賴 hover 這個區塊 —— 這樣整頁的圖譜
       會一起朝游標偏移，而不是只有滑過的那一塊有反應。 */

    /* 小區塊（例如子頁的 page-head）只放得下分類層，
       否則節點會擠成一團看起來像雜訊 */
    function depthForArea() {
      /* 窄畫面即使面積夠大，橫向空間也不足以攤開三層 —— 節點會擠成雜訊 */
      if (W < 640) return W < 420 ? 0 : 1;
      var area = W * H;
      if (area < 260000) return 0;
      if (area < 620000) return 1;
      return 2;
    }

    function build() {
      nodes = [];
      if (!W || !H) return;
      var maxDepth = depthForArea();
      var pad = Math.min(60, W * 0.08);

      function place(cx, cy, spread, minGap, tries) {
        var p, ok;
        for (var t = 0; t < tries; t++) {
          p = spread
            ? { x: cx + (Math.random() - 0.5) * spread, y: cy + (Math.random() - 0.5) * spread }
            : { x: pad + Math.random() * (W - pad * 2), y: pad + Math.random() * (H - pad * 2) };
          if (p.x < pad || p.x > W - pad || p.y < pad || p.y > H - pad) continue;
          ok = true;
          for (var i = 0; i < nodes.length; i++) {
            if (dist(p, nodes[i]) < minGap) { ok = false; break; }
          }
          if (ok) return p;
        }
        return null;
      }

      function add(p, name, level, r, parent) {
        var n = { name: name, x: p.x, y: p.y, ox: p.x, oy: p.y, level: level, r: r, parent: parent };
        nodes.push(n);
        return n;
      }

      tree.forEach(function (cat) {
        var p = place(0, 0, 0, 90, 300);
        if (!p) return;
        var cn = add(p, cat.name, 0, 8, null);
        if (maxDepth < 1) return;

        (cat.children || []).forEach(function (sub) {
          var sp = place(p.x, p.y, 160, 40, 150);
          if (!sp) return;
          var sn = add(sp, sub.name, 1, 5, cn);
          if (maxDepth < 2) return;

          (sub.skills || []).forEach(function (skill) {
            var kp = place(sp.x, sp.y, 80, 25, 80);
            if (kp) add(kp, skill, 2, 3, sn);
          });
        });
      });
    }

    /* 有些區塊非常高（知識庫列表可達 10000px 以上）。整段鋪滿會讓 bitmap
       吃掉數十 MB，而且圖譜在那個比例下只會變成縱向糊斑。所以 canvas 高度
       壓在 1.2 個視窗高，超出的部分靠底部遮罩淡出。 */
    var MAX_H_FACTOR = 1.2;

    function resize() {
      var rect = wrap.getBoundingClientRect();
      hostTop = rect.top + (window.pageYOffset || 0);
      hostLeft = rect.left;
      var w = Math.max(1, Math.round(rect.width));
      var full = Math.max(1, Math.round(rect.height));
      var h = Math.min(full, Math.round(window.innerHeight * MAX_H_FACTOR));

      if (w === W && h === H) return;   /* 尺寸沒變就別重建，免得抖動 */

      W = canvas.width = w;
      H = canvas.height = h;
      canvas.style.height = h + 'px';
      /* 只有被截斷時才淡出，剛好鋪滿的區塊不需要 */
      if (full > h + 4) canvas.classList.add('kg-clipped');
      else canvas.classList.remove('kg-clipped');

      build();
      if (REDUCED) draw(true);
    }

    /* 捲動視差：用「這個區塊的中心離視窗中心多遠」換算縱向位移。
       區塊由下方進場時圖譜被往上拖，離場時繼續往上滑 —— 就是被拖著跑的感覺。 */
    function parallaxY() {
      var offset = ((pageY + viewH / 2) - (hostTop + H / 2)) * PARALLAX;
      if (offset > PARALLAX_MAX) return PARALLAX_MAX;
      if (offset < -PARALLAX_MAX) return -PARALLAX_MAX;
      return offset;
    }

    function draw(once) {
      if (!once && !visible) { rafId = null; return; }
      time += 0.02;

      /* 滑鼠偏移：緩動追過去，放手後慢慢回中 */
      mShift.x += (ptrN.x * MOUSE_SHIFT - mShift.x) * MOUSE_EASE;
      mShift.y += (ptrN.y * MOUSE_SHIFT - mShift.y) * MOUSE_EASE;
      var shiftX = mShift.x;
      var shiftY = mShift.y + parallaxY();

      /* 游標在這塊 canvas 上的局部座標（推開與發亮用） */
      var mx = ptr.on ? ptr.x - hostLeft : -9999;
      var my = ptr.on ? ptr.y - (hostTop - pageY) : -9999;

      /* 整體極慢自轉：漂移在原座標上算，旋轉與位移只影響繪製位置 */
      var cx = W / 2, cy = H / 2;
      var angle = time * 0.015;
      var cosA = Math.cos(angle), sinA = Math.sin(angle);
      function spun(n) {
        var dx = n.x - cx, dy = n.y - cy;
        return {
          x: cx + dx * cosA - dy * sinA + shiftX,
          y: cy + dx * sinA + dy * cosA + shiftY
        };
      }

      ctx.clearRect(0, 0, W, H);

      if (!once) {
        nodes.forEach(function (n) {
          var speed = 1 - n.level * 0.3;
          var amp = 11 - n.level * 2;
          var ddx = n.ox - n.x + Math.sin(time * speed + n.oy * 0.003) * amp;
          var ddy = n.oy - n.y + Math.cos(time * speed * 1.2 + n.ox * 0.003) * amp;

          var mdx = mx - n.x, mdy = my - n.y;
          var md = Math.sqrt(mdx * mdx + mdy * mdy);
          if (md < 100 && md > 1) {
            ddx += mdx / md * (100 - md) / 100 * 2.25;
            ddy += mdy / md * (100 - md) / 100 * 2.25;
          }
          n.x += ddx * 0.11;
          n.y += ddy * 0.11;
        });
      }

      /* 連線：親子 */
      ctx.lineWidth = 0.5;
      ctx.strokeStyle = 'rgba(' + pal.dim + ',' + (0.07 * pal.mul) + ')';
      nodes.forEach(function (n) {
        if (!n.parent) return;
        var a = spun(n), b = spun(n.parent);
        ctx.beginPath(); ctx.moveTo(b.x, b.y); ctx.lineTo(a.x, a.y); ctx.stroke();
      });

      /* 連線：分類 ⟷ 分類（近的才連） */
      var tops = nodes.filter(function (n) { return n.level === 0; });
      ctx.strokeStyle = 'rgba(' + pal.dim + ',' + (0.03 * pal.mul) + ')';
      for (var i = 0; i < tops.length; i++) {
        var a2 = spun(tops[i]);
        for (var j = i + 1; j < tops.length; j++) {
          var b2 = spun(tops[j]);
          if (dist(a2, b2) < 280) {
            ctx.beginPath(); ctx.moveTo(a2.x, a2.y); ctx.lineTo(b2.x, b2.y); ctx.stroke();
          }
        }
      }

      /* 節點 */
      nodes.forEach(function (n) {
        var gp = spun(n);
        var pulse = once ? 1 : 1 + Math.sin(time * 4 + n.ox * 0.1) * 0.15;
        var br = n.r * pulse;
        var glowR = br * (n.level < 2 ? 5 : 4);
        var alpha = (0.12 + n.level * 0.07) * pal.mul;

        var md = Math.sqrt((mx - n.x) * (mx - n.x) + (my - n.y) * (my - n.y));
        if (md < 100) alpha += (100 - md) / 100 * 0.5 * pal.mul;
        if (alpha > 1) alpha = 1;

        var grad = ctx.createRadialGradient(gp.x, gp.y, 0, gp.x, gp.y, glowR);
        grad.addColorStop(0, 'rgba(' + pal.fg + ',' + alpha + ')');
        grad.addColorStop(1, 'rgba(' + pal.fg + ',0)');
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(gp.x, gp.y, glowR, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = 'rgba(' + pal.fg + ',' + ((0.12 + n.level * 0.08) * pal.mul) + ')';
        ctx.beginPath(); ctx.arc(gp.x, gp.y, br, 0, Math.PI * 2); ctx.fill();

        if (n.level === 0) {
          ctx.font = '11px -apple-system,BlinkMacSystemFont,"Noto Sans TC",sans-serif';
          ctx.fillStyle = 'rgba(' + pal.dim + ',' + (0.2 * pal.mul) + ')';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'top';
          ctx.fillText(n.name, gp.x, gp.y + br + 4);
        }
      });

      if (!once) rafId = requestAnimationFrame(tick);
    }

    /* rAF 會把 timestamp 當第一個參數傳進來，所以不能把 draw 直接當 callback
       —— 那個 timestamp 會被當成 `once` 而讓動畫只跑一幀。 */
    function tick() { draw(false); }

    /* 先量尺寸建好節點，再開始觀察 —— 否則第一幀會畫在還沒建圖的空狀態上 */
    resize();

    if (!REDUCED) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          visible = entry.isIntersecting;
          if (visible && !rafId) rafId = requestAnimationFrame(tick);
          else if (!visible && rafId) { cancelAnimationFrame(rafId); rafId = null; }
        });
      }, { threshold: 0 }).observe(wrap);
    }

    var t;
    function scheduleResize() {
      clearTimeout(t);
      t = setTimeout(resize, 160);
    }
    window.addEventListener('resize', scheduleResize);

    /* 關鍵：區塊高度是由 JS 非同步撐開的（知識庫 85 張卡、活動列表…），
       單靠 window resize 量不到，bitmap 會停在初始的小尺寸然後被 CSS 拉伸。 */
    if (window.ResizeObserver) {
      new ResizeObserver(scheduleResize).observe(wrap);
    }

    return {
      /* 頁面整體變高時（知識庫塞完 85 張卡），這個區塊的文件位置會位移，
         視差算式用的 hostTop 必須跟著更新，否則視差會偏掉。 */
      refresh: function () {
        hostTop = wrap.getBoundingClientRect().top + (window.pageYOffset || 0);
        hostLeft = wrap.getBoundingClientRect().left;
      }
    };
  }

  function init(tree) {
    var hosts = document.querySelectorAll(TARGETS);
    var instances = [];
    for (var i = 0; i < hosts.length; i++) instances.push(initOne(hosts[i], tree));

    if (window.ResizeObserver) {
      new ResizeObserver(function () {
        instances.forEach(function (inst) { inst.refresh(); });
      }).observe(document.body);
    }
  }

  /* data.json 讀不到時（例如以 file:// 開啟）退回只有分類骨架的圖譜 */
  (window.siteData || Promise.resolve(null)).then(function (d) {
    init(d && d.tree && d.tree.length ? d.tree : FALLBACK_TREE);
  });
})();
