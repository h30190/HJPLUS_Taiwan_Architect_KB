/* 站台共用行為：導覽、hero、統計、貢獻者、活動。
   knowledge-base 介面另見 kb.js。無框架、無建置步驟。 */
(function () {
  'use strict';

  var ROOT = window.SITE_ROOT || '';
  var REPO = window.SITE_REPO || 'https://github.com/h30190/HJPLUS_Taiwan_Architect_KB';
  var API = 'https://api.github.com/repos/h30190/HJPLUS_Taiwan_Architect_KB';

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* GitHub issue 內容是外部輸入，一律轉義後才進 innerHTML。 */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  window.escHtml = esc;

  /* ── 行動版選單 ── */
  var toggle = $('#navToggle'), nav = $('#siteNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ── hero 之上的 header 反白 ── */
  var header = $('#siteHeader'), hero = $('.hero');
  if (header && hero) {
    var sync = function () {
      var past = window.scrollY > hero.offsetHeight - 70;
      header.classList.toggle('over-dark', !past);
    };
    sync();
    window.addEventListener('scroll', sync, { passive: true });
    requestAnimationFrame(function () { hero.classList.add('loaded'); });
  }

  /* ── hero 計數器：等 hero 揭示完才滾（沿用 V1 的節奏）──
     交給 IntersectionObserver 會壞掉：hero 一開始就在視窗內，data.json 一回來
     （通常 <100ms）動畫就跑完了，而 .hero-stats 要到 1.12s 才淡入，
     使用者只會看到最終數字。所以 hero 這幾顆改用時間排程，
     對齊 .hero-stats 淡入之後，時長也拉回 V1 的 1200ms。
     HTML 寫死的數字先收成 fallback，no-JS 時仍看得到值。 */
  var HERO_DELAY = 1500, HERO_DUR = 1200;
  var heroCounters = hero ? $$('[data-stat]', hero) : [];
  var heroCountersRan = false;

  heroCounters.forEach(function (el) {
    el.dataset.to = (el.textContent || '').replace(/[^0-9]/g, '') || '0';
    el.textContent = '0';
  });

  if (heroCounters.length) {
    setTimeout(function () {
      heroCountersRan = true;
      heroCounters.forEach(function (el) {
        countUp(el, parseInt(el.dataset.to, 10) || 0, HERO_DUR);
      });
    }, HERO_DELAY);
  }

  /* ── 圓點導覽 + 自動輪播（僅首頁，沿用 V1 行為）──
     V1 的「動感」主要來自這裡：載入 4 秒後每 5 秒自己捲到下一段，
     使用者一動就永久停止。標籤直接取每段的 .eyebrow 或 h2，
     不用另外維護一份對照表。 */
  (function () {
    if (!document.body.classList.contains('home')) return;
    var main = $('#main');
    if (!main) return;

    var secs = $$(':scope > section', main);
    if (secs.length < 2) return;

    var nav = document.createElement('nav');
    nav.className = 'dot-nav';
    nav.id = 'dotNav';
    nav.setAttribute('aria-label', '章節導覽');

    secs.forEach(function (sec, i) {
      if (!sec.id) sec.id = 'sec-' + (i + 1);
      /* hero 的 eyebrow 是一整句宣傳語，太長 —— 比照 V1 直接叫「首頁」 */
      var label;
      if (sec.classList.contains('hero')) {
        label = '首頁';
      } else {
        var eyebrow = $('.eyebrow', sec);
        var h = $('h2', sec);
        label = (eyebrow && eyebrow.textContent.trim()) ||
                (h && h.textContent.trim()) || ('第 ' + (i + 1) + ' 段');
        if (label.length > 6) label = label.slice(0, 6) + '…';
      }
      var a = document.createElement('a');
      a.href = '#' + sec.id;
      a.setAttribute('data-label', label);
      a.setAttribute('data-target', sec.id);
      a.setAttribute('aria-label', label);
      nav.appendChild(a);
    });
    document.body.appendChild(nav);

    var dots = $$('a', nav);
    /* 深色底的區塊要把圓點反白 */
    function isDark(sec) {
      return sec.classList.contains('dark') || sec.classList.contains('hero');
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        dots.forEach(function (d) {
          d.classList.toggle('active', d.getAttribute('data-target') === e.target.id);
        });
        nav.classList.toggle('dark-bg', isDark(e.target));
      });
    }, { threshold: 0.5 });
    secs.forEach(function (sec) { io.observe(sec); });

    /* ── 自動輪播 ──
       比照 V1：不檢查 prefers-reduced-motion。任何使用者操作都會永久停止，
       所以它不會跟人搶方向盤。 */
    var timer = null, alive = true;

    function stop() {
      alive = false;
      if (timer) { clearInterval(timer); timer = null; }
    }

    function next() {
      if (!alive) return;
      var cur = $('a.active', nav);
      var i = cur ? dots.indexOf(cur) : 0;
      if (i < 0 || i >= secs.length - 1) { stop(); return; }
      secs[i + 1].scrollIntoView({ behavior: 'smooth' });
    }

    /* 任何操作都永久停止 —— 自動移動的內容不該跟使用者搶方向盤 */
    ['wheel', 'touchstart', 'pointerdown'].forEach(function (ev) {
      window.addEventListener(ev, stop, { passive: true, once: true });
    });
    window.addEventListener('keydown', function (e) {
      if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' '].indexOf(e.key) !== -1) stop();
    });
    nav.addEventListener('click', stop);

    setTimeout(function () {
      if (alive) timer = setInterval(next, 5000);
    }, 4000);
  })();

  /* ── 捲動淡入 ──
     進入視窗時逐一浮現。只處理載入時就存在的元素 —— 之後由 JS 塞進來的
     內容（知識庫卡片、活動列表）不掛 .reveal，否則會閃一下才出現。 */
  (function () {
    if (!('IntersectionObserver' in window)) return;

    var SELECTORS = [
      '.section-head', '.card', '.compare-col', '.callout', '.code-block',
      '.event-card', '.table-wrap', '.contributors', '.video-embed',
      '.prose > h2', '.prose > h3', '.prose > blockquote',
      '.hero-actions ~ *'
    ].join(', ');

    var main = $('#main');
    if (!main) return;

    var items = $$(SELECTORS, main).filter(function (el) {
      /* hero 有自己的分段揭示；動態注入區塊不參與 */
      return !el.closest('.hero') && !el.closest('#kbResults') && !el.closest('#kbDash');
    });
    if (!items.length) return;

    /* 同一個父容器內依序錯開，形成由上而下的節奏 */
    var seen = new Map();
    items.forEach(function (el) {
      var key = el.parentElement;
      var i = (seen.get(key) || 0);
      seen.set(key, i + 1);
      el.classList.add('reveal');
      if (i) el.style.transitionDelay = Math.min(i * 70, 350) + 'ms';
    });

    var pending = new Set(items);

    function reveal(el) {
      el.classList.add('in');
      pending.delete(el);
      io.unobserve(el);
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) reveal(e.target); });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });

    /* 安全網：IntersectionObserver 只回報「被觀察到的」狀態變化，所以一次
       跳很遠（Ctrl+End、點錨點、瀏覽器搜尋跳轉）會讓中間的元素從未進入
       視窗 —— 那些內容就永遠停在 opacity 0。

       關鍵：只補救「已經整個捲過去」的元素（bottom < 0）。還在視窗裡或
       在下方的一律交給 IO —— 之前條件寫成 top < innerHeight，每次捲動都
       比 IO 早觸發，元素在還看不到的時候就淡完了，等於整個效果沒作用。 */
    var sweeping = false;
    function sweep() {
      sweeping = false;
      if (!pending.size) {
        window.removeEventListener('scroll', onScroll);
        return;
      }
      /* Set 不是 array-like，slice.call 會回傳空陣列 —— 必須用 Array.from */
      Array.from(pending).forEach(function (el) {
        if (el.getBoundingClientRect().bottom < 0) reveal(el);
      });
    }
    function onScroll() {
      if (sweeping) return;
      sweeping = true;
      requestAnimationFrame(sweep);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
  })();

  /* ── 文件頁的章節圓點導覽 ──
     首頁那組 dot-nav 綁在 section 上（一段一屏）並且會自動輪播；
     文件頁沒有分屏，章節單位是 h2，而且刻意不自動捲：
     免責條文與方法論要停下來細讀，讀到一半被捲走比頁面長更糟。
     標籤取 data-nav，沒有就用標題本身截短。 */
  (function () {
    if (!document.body.classList.contains('doc')) return;

    var heads = $$('.page-head h1, #main h2');
    if (heads.length < 4) return;    /* 章節太少，圓點只是雜訊 */

    var nav = document.createElement('nav');
    nav.className = 'dot-nav';
    nav.setAttribute('aria-label', '章節導覽');

    var items = heads.map(function (h, i) {
      if (!h.id) h.id = 'ch-' + (i + 1);
      var label = (h.getAttribute('data-nav') || h.textContent || '').trim();
      if (label.length > 12) label = label.slice(0, 11) + '…';
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.dataset.label = label;
      a.setAttribute('aria-label', label);
      /* 自己捲，不讓網址留下 hash：ch-N 是照出現順序自動編號的，
         章節一增減，複製出去的 #ch-5 就指到別章了。
         href 照樣留著，鍵盤與螢幕閱讀器要看得到這是連結。 */
      a.addEventListener('click', function (e) {
        e.preventDefault();
        h.scrollIntoView({ behavior: 'smooth' });
      });
      nav.appendChild(a);
      return { head: h, dot: a, dark: !!h.closest('section.dark, .page-head.dark') };
    });
    document.body.appendChild(nav);

    /* 判定線放在 header 底下一點：標題捲過這條線就算進入該章節 */
    var LINE_PAD = 24;
    var ticking = false;

    function syncActive() {
      ticking = false;
      var hh = parseInt(getComputedStyle(document.documentElement)
        .getPropertyValue('--header-h'), 10) || 60;
      var line = hh + LINE_PAD;
      var cur = items[0];
      items.forEach(function (it) {
        if (it.head.getBoundingClientRect().top <= line) cur = it;
      });
      items.forEach(function (it) { it.dot.classList.toggle('active', it === cur); });
      nav.classList.toggle('dark-bg', cur.dark);
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(syncActive);
    }

    syncActive();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);

  })();

  /* ── 知識庫工具列的篩選摺疊（只在窄螢幕作用） ── */
  (function () {
    var btn = $('#kbFilterToggle'), bar = $('.kb-toolbar');
    if (!btn || !bar) return;
    btn.addEventListener('click', function () {
      var open = bar.classList.toggle('filters-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  })();

  /* ── 橫向滑動卡片 ──
     右緣的淡出遮罩代表「右邊還有」，捲到底就得收掉，
     不然到底了還留一片灰，看起來像內容被裁掉。
     鍵盤左右鍵補上捲動：track 是 tabindex=0 的 group，
     但瀏覽器預設只給上下鍵捲，橫向捲動對鍵盤使用者等於沒有。 */
  $$('.hscroll').forEach(function (wrap) {
    var track = $('.hscroll-track', wrap);
    if (!track) return;

    var btns = $$('.hscroll-btn', wrap);

    /* 一次捲一張卡（含 gap），而不是捲一整個可視寬度 —— 卡片才會
       停在整數張的位置上，不會出現半張。 */
    function step() {
      var card = $('.hcard', track);
      return card ? card.offsetWidth + 16 : 280;
    }
    function scrollByCard(dir) {
      track.scrollBy({ left: dir * step(), behavior: 'smooth' });
    }

    function syncEdge() {
      /* 次像素誤差會讓「捲到底」永遠差 0.5px，留 2px 容錯 */
      var atStart = track.scrollLeft <= 2;
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
      wrap.classList.toggle('at-end', atEnd);
      btns.forEach(function (b) {
        var dir = parseInt(b.getAttribute('data-dir'), 10);
        b.disabled = dir < 0 ? atStart : atEnd;
      });
    }
    syncEdge();
    track.addEventListener('scroll', syncEdge, { passive: true });
    window.addEventListener('resize', syncEdge);

    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        scrollByCard(parseInt(b.getAttribute('data-dir'), 10));
      });
    });

    track.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      scrollByCard(e.key === 'ArrowRight' ? 1 : -1);
      e.preventDefault();
    });
  });

  /* ── 數字滾動 ── */
  function countUp(el, to, dur) {
    /* 太大的數字滾起來只是雜訊，直接顯示 */
    if (to > 5000) { el.textContent = to; return; }
    /* 從畫面上的現值起跳：真實統計比 fallback 晚到時，是接著滑而不是跳回 0 */
    var start = null, from = parseInt((el.textContent || '').replace(/[^0-9]/g, ''), 10) || 0;
    dur = dur || 900;
    function tick(now) {
      if (start === null) start = now;
      var p = Math.min((now - start) / dur, 1);
      el.textContent = Math.round(from + (to - from) * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function setCounters(values) {
    $$('[data-stat]').forEach(function (el) {
      var v = values[el.getAttribute('data-stat')];
      if (v == null) return;
      /* hero 那幾顆由上面的排程負責：還沒滾就換掉目標值，
         已經滾完（統計回得慢）就從現值再滑到真實值。 */
      if (heroCounters.indexOf(el) !== -1) {
        el.dataset.to = v;
        if (heroCountersRan) countUp(el, v, HERO_DUR);
        return;
      }
      var seen = false;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting && !seen) { seen = true; countUp(el, v); io.disconnect(); }
        });
      }, { threshold: 0.3 });
      io.observe(el);
    });
  }

  /* ── data.json：統計、貢獻者、最近更新 ── */
  window.siteData = fetch(ROOT + 'data.json')
    .then(function (r) { return r.ok ? r.json() : null; })
    .catch(function () { return null; });

  /* data.json 是建置時的快照，但 contributors 與 mergedPRs 只有 CI
     帶 --github-stats 跑才有值 —— 本機預覽時是 null，名單會是空的。
     所以照 V1 的做法，前端自己打一次 GitHub API 補上。 */
  var ghApplied = false;

  window.siteData.then(function (d) {
    if (!d) return;
    var s = d.stats || {};
    /* API 已經回來過就別用舊快照覆蓋它 */
    if (!ghApplied) {
      setCounters({
        commits: s.commits,
        skills: s.skills,
        categories: s.categories,
        contributors: s.contributors,
        mergedPRs: s.mergedPRs
      });
      renderContributors(d.contributors);
    }
    renderUpdates(d.updates);
  });

  /* ── GitHub API：貢獻者名單與即時計數 ──
     未認證的 API 每小時 60 次、search 更少，所以整批結果放進
     sessionStorage，同一次瀏覽不再重複打。
     任何一支失敗就讓它回 null，其餘照樣套用，不要一顆壞掉全盤放棄。 */
  (function () {
    var KEY = 'gh-stats-v3';   /* 結構加了 skills / categories，舊快取要失效 */
    var SEARCH = 'https://api.github.com/search/issues?q=repo:h30190/' +
      'HJPLUS_Taiwan_Architect_KB+type:pr+is:merged';

    function apply(g) {
      ghApplied = true;
      var vals = {};
      if (g.commits) vals.commits = g.commits;
      if (g.skills) vals.skills = g.skills;
      if (g.categories) vals.categories = g.categories;
      if (g.mergedPRs != null) vals.mergedPRs = g.mergedPRs;
      if (g.contributors && g.contributors.length) {
        vals.contributors = g.contributors.length;
        renderContributors(g.contributors);
      }
      setCounters(vals);
    }

    var cached = null;
    try { cached = JSON.parse(sessionStorage.getItem(KEY)); } catch (e) { /* 壞掉就重抓 */ }
    if (cached) { apply(cached); return; }

    /* commit 總數不在 body 裡，要從分頁 Link 標頭的 last 頁號讀 */
    function lastPage(res) {
      var m = (res.headers.get('Link') || '').match(/[?&]page=(\d+)>;\s*rel="last"/);
      return m ? parseInt(m[1], 10) : null;
    }

    Promise.all([
      fetch(API + '/commits?per_page=1')
        .then(lastPage).catch(function () { return null; }),
      fetch(API + '/contributors?per_page=100')
        .then(function (r) { return r.ok ? r.json() : []; })
        .then(function (a) {
          return Array.isArray(a) ? a.map(function (u) { return u.login; }) : [];
        })
        .catch(function () { return []; }),
      fetch(SEARCH)
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) { return d ? d.total_count : null; })
        .catch(function () { return null; }),
      /* 分類數 = raw/ 底下的目錄數 */
      fetch(API + '/contents/raw')
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (!Array.isArray(d)) return null;
          return d.filter(function (i) { return i.type === 'dir'; }).length;
        })
        .catch(function () { return null; }),
      /* 技能數 = raw/ 底下的 SKILL.md 數。
         V1 是掃全庫，會把 contributor-pr-workflow 與 知識樣板/ 那兩份
         也算進去（87 而不是 85），所以這裡限定 raw/ 開頭，
         跟 kb_index.py 產出的數字對得上。
         truncated 代表樹被截斷、數出來會偏少，那寧可不採用。 */
      fetch(API + '/git/trees/main?recursive=1')
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (!d || !d.tree || d.truncated) return null;
          return d.tree.filter(function (i) {
            return i.path.indexOf('raw/') === 0 && /SKILL\.md$/.test(i.path);
          }).length;
        })
        .catch(function () { return null; })
    ]).then(function (a) {
      var g = {
        commits: a[0], contributors: a[1], mergedPRs: a[2],
        categories: a[3], skills: a[4]
      };
      if (!g.commits && !g.contributors.length && g.mergedPRs == null &&
          !g.categories && !g.skills) return;
      try { sessionStorage.setItem(KEY, JSON.stringify(g)); } catch (e) { /* 無痕模式會擋 */ }
      apply(g);
    });
  })();

  /* 貢獻者名單做成跑馬燈：人數會一直長，攤開排會佔掉半個區塊，
     而且這份名單本身就是想被看見的東西，滾動比靜態清單更容易被注意到。
     滑鼠移上去或鍵盤 focus 進去就停，要點名字不必追著跑。 */
  function renderContributors(list) {
    var box = $('#contributorList');
    if (!box || !list || !list.length) return;

    var html = list.map(function (c) {
      var login = typeof c === 'string' ? c : c.login;
      return '<a class="contributor" href="https://github.com/' + encodeURIComponent(login) +
        '" target="_blank" rel="noopener">@' + esc(login) + '</a>';
    }).join('');

    /* 這裡跟背景圖譜的取捨不同，所以尊重 prefers-reduced-motion：
       圖譜停下來只是少了氣氛，跑馬燈停下來就是一排完整的名字，
       資訊一點沒少，關掉的代價幾乎是零。人少時也不必滾。 */
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || list.length < 8) {
      box.className = 'contributors';
      box.innerHTML = html;
      return;
    }

    /* 兩份等寬的名單並排，動畫捲一份的距離（-50%）就無縫接回開頭。
       複本對輔助技術隱藏，否則每個名字都會被讀兩次。 */
    box.className = 'contributors contrib-marquee';
    box.innerHTML =
      '<div class="contrib-marquee-track">' +
        '<div class="contrib-group">' + html + '</div>' +
        '<div class="contrib-group" aria-hidden="true">' + html + '</div>' +
      '</div>';

    /* 名單越長就滾越久，讓速度固定在每秒約 60px，不會人一多就飆過去 */
    var group = $('.contrib-group', box);
    if (group) {
      var secs = Math.max(18, Math.round(group.scrollWidth / 60));
      $('.contrib-marquee-track', box).style.animationDuration = secs + 's';
    }
  }

  function renderUpdates(list) {
    var box = $('#updateList');
    if (!box || !list || !list.length) return;
    box.innerHTML = list.slice(0, 6).map(function (u) {
      return '<li><span class="date">' + esc(u.date) + '</span>' + esc(u.text) + '</li>';
    }).join('');
  }

  /* ── 近期活動（GitHub issues，label: event） ── */
  (function () {
    var list = $('#eventList');
    if (!list) return;

    var EMPTY = '<div class="event-empty">活動資訊尚未公布，敬請持續關注。' +
      '<br><a href="' + REPO + '/issues/new?template=event.yml" target="_blank" rel="noopener">想辦一場小聚？開個 issue。</a></div>';

    var cached = null;
    try { cached = sessionStorage.getItem('gh-events'); } catch (e) { /* private mode */ }
    if (cached) { render(JSON.parse(cached)); return; }

    fetch(API + '/issues?labels=event&state=open&per_page=5')
      .then(function (r) { return r.json(); })
      .then(function (issues) {
        if (!Array.isArray(issues) || !issues.length) { list.innerHTML = EMPTY; return; }
        try { sessionStorage.setItem('gh-events', JSON.stringify(issues)); } catch (e) { /* quota */ }
        render(issues);
      })
      .catch(function () { list.innerHTML = EMPTY; });

    function field(body, emoji) {
      var lines = body.split('\n');
      for (var i = 0; i < lines.length; i++) {
        if (lines[i].indexOf(emoji) === -1) continue;
        var m = lines[i].match(/[：:）)\]]\s*(.+)/);
        if (m) return m[1].trim();
        for (var j = i + 1; j < lines.length && j <= i + 3; j++) {
          var l = lines[j].trim();
          if (l && l.indexOf('### ') !== 0) return l;
        }
      }
      return '';
    }

    function render(issues) {
      var today = new Date(new Date().toDateString());
      var html = issues.map(function (issue) {
        var body = issue.body || '';
        var title = (issue.title || '').replace(/^\[活動\]\s*/, '');
        var when = field(body, '📅');
        var where = field(body, '📍');
        var link = field(body, '🔗') || issue.html_url;
        var desc = field(body, '📝');

        var d = when.match(/(\d{4}-\d{2}-\d{2})/);
        if (d && new Date(d[1]) < today) return '';

        /* 只接受 http(s)，擋掉 javascript: 之類的連結 */
        var safeLink = /^https?:\/\//i.test(link) ? link : issue.html_url;

        return '<div class="event-card"><div class="event-info"><div class="event-meta">' +
          (when ? '<strong>' + esc(when) + '</strong>' : '') +
          (where ? ' · ' + esc(where) : '') +
          '</div><h3>' + esc(title) + '</h3>' +
          (desc ? '<p>' + esc(desc) + '</p>' : '') +
          '</div><div class="event-action"><a class="btn btn-primary btn-sm" href="' +
          esc(safeLink) + '" target="_blank" rel="noopener">看詳情</a></div></div>';
      }).join('');
      list.innerHTML = html || EMPTY;
    }
  })();
})();
