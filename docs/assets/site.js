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

    /* ── 自動輪播 ── */
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

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
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
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

  /* ── 數字滾動 ── */
  function countUp(el, to) {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || to > 5000) { el.textContent = to; return; }
    var start = null, dur = 900, from = 0;
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

  window.siteData.then(function (d) {
    if (!d) return;
    var s = d.stats || {};
    setCounters({
      commits: s.commits,
      skills: s.skills,
      categories: s.categories,
      contributors: s.contributors,
      mergedPRs: s.mergedPRs
    });
    renderContributors(d.contributors);
    renderUpdates(d.updates);
  });

  function renderContributors(list) {
    var box = $('#contributorList');
    if (!box || !list || !list.length) return;
    box.innerHTML = list.map(function (c) {
      var login = typeof c === 'string' ? c : c.login;
      return '<a class="contributor" href="https://github.com/' + encodeURIComponent(login) +
        '" target="_blank" rel="noopener">@' + esc(login) + '</a>';
    }).join('');
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
