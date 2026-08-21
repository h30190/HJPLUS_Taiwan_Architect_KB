/* 知識庫瀏覽介面 — 由 docs/kb.json（scripts/kb_index.py 掃 raw/ 產生）驅動。
   兩件事：① 方便找資料 ② 看得出每筆資料的狀況。
   篩選條件會同步到網址，所以任何一個檢視都可以直接貼給別人。

   註：kb.json 仍帶有查證相關欄位（verified / status / data-currency），
   但目前一律不呈現。要開回來的話，這裡加上對應的欄位與篩選即可，
   資料層不需要動。 */
(function () {
  'use strict';

  var esc = window.escHtml;
  var ROOT = window.SITE_ROOT || '';

  var FILTER_KEYS = ['q', 'category', 'klass', 'flag'];

  var state = {
    q: '',
    category: '',
    klass: '',
    flag: '',
    sort: 'category',
    view: 'card'
  };

  var DATA = null;

  var el = {
    dash: document.getElementById('kbDash'),
    filters: document.getElementById('kbFilters'),
    search: document.getElementById('kbSearch'),
    searchBox: document.getElementById('kbSearchBox'),
    clear: document.getElementById('kbClear'),
    results: document.getElementById('kbResults'),
    count: document.getElementById('kbCount'),
    sort: document.getElementById('kbSort'),
    viewCard: document.getElementById('kbViewCard'),
    viewTable: document.getElementById('kbViewTable')
  };

  var FLAGS = {
    todo: { label: '待台灣適配', test: function (e) { return e.hasTodo; } },
    planned: { label: '籌備中', test: function (e) { return e.isPlanned; } },
    flat: { label: '結構待整理', test: function (e) { return e.layout === 'flat'; } },
    thin: { label: '中文說明偏薄', test: function (e) { return e.domainChars < 800; } },
    incomplete: { label: '後設資料不全', test: function (e) { return e.missing.length > 0; } },
    noref: { label: '缺參考資料', test: function (e) { return !e.hasReferences; } }
  };

  var GAP_LABEL = {
    region: '適用地區',
    audience: '適用對象',
    license: '授權標示',
    compatibility: '相容性標示'
  };

  var KLASS_LABEL = { A: 'A 通用', B: 'B 待適配', C: 'C 台灣法規' };

  /* ── 網址 ⇄ 狀態 ── */
  function readUrl() {
    var p = new URLSearchParams(location.search);
    FILTER_KEYS.concat(['sort', 'view']).forEach(function (k) {
      if (p.has(k)) state[k] = p.get(k);
    });
    if (location.hash === '#status') {
      requestAnimationFrame(function () {
        var t = document.getElementById('status');
        if (t) t.scrollIntoView();
      });
    }
  }

  function writeUrl() {
    var p = new URLSearchParams();
    Object.keys(state).forEach(function (k) {
      var isDefault = (k === 'sort' && state[k] === 'category') ||
        (k === 'view' && state[k] === 'card');
      if (state[k] && !isDefault) p.set(k, state[k]);
    });
    var qs = p.toString();
    /* 直接用 file:// 打開時 replaceState 會擋下來，篩選照常運作即可 */
    try {
      history.replaceState(null, '', qs ? '?' + qs : location.pathname);
    } catch (e) { /* non-http origin */ }
  }

  /* ── 篩選 ── */
  function match(e) {
    if (state.category && e.category !== state.category) return false;
    if (state.klass && e.klass !== state.klass) return false;
    if (state.flag && FLAGS[state.flag] && !FLAGS[state.flag].test(e)) return false;
    if (state.q) {
      var hay = (e.title + ' ' + e.name + ' ' + e.summary + ' ' + e.description +
        ' ' + e.category + ' ' + e.breadcrumb.join(' ')).toLowerCase();
      /* 空白分隔的多關鍵字一律 AND */
      var terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
      if (!terms.every(function (t) { return hay.indexOf(t) !== -1; })) return false;
    }
    return true;
  }

  var byTitle = function (a, b) { return a.title.localeCompare(b.title, 'zh-Hant'); };

  var SORTS = {
    category: function (a, b) { return a.category.localeCompare(b.category, 'zh-Hant') || byTitle(a, b); },
    title: byTitle,
    updated: function (a, b) { return (b.updated || '').localeCompare(a.updated || ''); },
    stale: function (a, b) { return (a.updated || '').localeCompare(b.updated || ''); },
    thin: function (a, b) { return a.domainChars - b.domainChars; }
  };

  /* ── 元件 ── */
  function badges(e) {
    var out = [];
    if (e.klass) out.push('<span class="badge badge-plain">' + esc(KLASS_LABEL[e.klass] || e.klass) + '</span>');
    if (e.hasTodo) out.push('<span class="badge badge-todo">待台灣適配</span>');
    if (e.isPlanned) out.push('<span class="badge badge-todo">籌備中</span>');
    if (e.hasReferences) out.push('<span class="badge badge-plain">附參考資料</span>');
    if (e.hasScripts) out.push('<span class="badge badge-plain">附腳本</span>');
    return out.join('');
  }

  function cardHtml(e) {
    return '<article class="kb-card">' +
      '<div class="kb-card-top"><div><h3>' + esc(e.title) + '</h3>' +
      '<div class="kb-path">' + esc(e.breadcrumb.join(' › ') || e.category) + '</div></div></div>' +
      '<div class="kb-card-badges">' + badges(e) + '</div>' +
      '<p class="kb-desc">' + esc(e.summary || e.description) + '</p>' +
      (e.description
        ? '<details class="kb-ai"><summary>AI 讀到的版本（英文）</summary>' +
          '<p>' + esc(e.description) + '</p></details>'
        : '') +
      '<div class="kb-name">' + esc(e.name) + '</div>' +
      '<div class="kb-card-foot">' +
      '<span>' + (e.updated ? '更新 ' + esc(e.updated) : '') + '</span>' +
      '<span class="kb-links">' +
      (e.domainUrl ? '<a href="' + esc(e.domainUrl) + '" target="_blank" rel="noopener">中文說明</a>' : '') +
      '<a href="' + esc(e.skillUrl) + '" target="_blank" rel="noopener">SKILL</a>' +
      '</span></div></article>';
  }

  function rowHtml(e) {
    var gaps = e.missing.length
      ? e.missing.map(function (k) { return esc(GAP_LABEL[k] || k); }).join('、')
      : '—';
    return '<tr>' +
      '<td class="t-title">' + esc(e.title) + '<div class="t-name">' + esc(e.name) + '</div></td>' +
      '<td class="t-summary">' + esc(e.summary) + '</td>' +
      '<td>' + esc(e.category) + '</td>' +
      '<td>' + (e.klass ? esc(e.klass) : '—') + '</td>' +
      '<td>' + (e.hasTodo ? '<span class="badge badge-todo">待適配</span>' : '') +
        (e.isPlanned ? '<span class="badge badge-todo">籌備中</span>' : '') +
        (!e.hasTodo && !e.isPlanned ? '—' : '') + '</td>' +
      '<td class="small muted">' + gaps + '</td>' +
      '<td class="num">' + e.domainChars + '</td>' +
      '<td>' + esc(e.updated || '—') + '</td>' +
      '<td class="t-links">' +
      (e.domainUrl ? '<a href="' + esc(e.domainUrl) + '" target="_blank" rel="noopener">中文</a>' : '') +
      '<a href="' + esc(e.skillUrl) + '" target="_blank" rel="noopener">SKILL</a></td>' +
      '</tr>';
  }

  function renderResults() {
    var list = DATA.entries.filter(match).sort(SORTS[state.sort] || SORTS.category);

    el.count.innerHTML = '共 <strong>' + list.length + '</strong> 筆' +
      (list.length !== DATA.entries.length ? '（全部 ' + DATA.entries.length + ' 筆）' : '');

    if (!list.length) {
      el.results.innerHTML = '<div class="kb-empty"><h3>沒有符合的技能</h3>' +
        '<p>換個關鍵字，或按「清除篩選」看全部 ' + DATA.entries.length + ' 筆。</p></div>';
      return;
    }

    if (state.view === 'table') {
      el.results.innerHTML = '<div class="kb-table-wrap"><table class="kb-table"><thead><tr>' +
        '<th>技能</th><th>中文說明（domain.md）</th><th>分類</th><th>類別</th><th>標記</th><th>缺少的後設欄位</th>' +
        '<th class="num">中文說明字數</th><th>最後更新</th><th>原始檔</th>' +
        '</tr></thead><tbody>' + list.map(rowHtml).join('') + '</tbody></table></div>';
    } else {
      el.results.innerHTML = '<div class="kb-grid">' + list.map(cardHtml).join('') + '</div>';
    }
  }

  /* ── 篩選器（數字為「套用其他條件後」的結果，避免出現點了必為 0 的選項） ── */
  function countWith(key, value) {
    var saved = state[key];
    state[key] = value;
    var n = DATA.entries.filter(match).length;
    state[key] = saved;
    return n;
  }

  function chip(key, value, label) {
    var active = state[key] === value;
    var n = countWith(key, value);
    var disabled = n === 0 && !active;
    return '<button class="chip' + (active ? ' active' : '') + '" data-key="' + key +
      '" data-value="' + esc(value) + '"' + (disabled ? ' disabled' : '') + '>' +
      esc(label) + '<span class="chip-count">' + n + '</span></button>';
  }

  function group(label, key, values) {
    return '<div class="kb-filter-group"><span class="kb-filter-label">' + label + '</span>' +
      values.map(function (v) { return chip(key, v[0], v[1]); }).join('') + '</div>';
  }

  function renderFilters() {
    var s = DATA.summary;
    var cats = Object.keys(s.categories).filter(function (c) { return s.categories[c].total > 0; });

    var html = '';
    html += group('分類', 'category',
      [['', '全部']].concat(cats.map(function (c) { return [c, c]; })));
    html += group('類別', 'klass',
      [['', '全部']].concat(['A', 'B', 'C'].map(function (k) { return [k, KLASS_LABEL[k]]; })));
    html += group('待補', 'flag',
      [['', '不限']].concat(Object.keys(FLAGS).map(function (k) { return [k, FLAGS[k].label]; })));
    html += '<button class="kb-reset" id="kbReset">清除篩選</button>';

    el.filters.innerHTML = html;
  }

  /* ── 資料狀況儀表板 ── */
  function renderDash() {
    var s = DATA.summary, total = s.total;

    var stats = '<div class="stat-row">' +
      '<div class="stat"><div class="stat-num">' + total + '</div><div class="stat-label">技能總數</div></div>' +
      '<div class="stat"><div class="stat-num">' + Object.keys(s.categories).length +
        '</div><div class="stat-label">分類（含 ' + s.emptyCategories.length + ' 個空的）</div></div>' +
      '<div class="stat is-warn"><div class="stat-num">' + s.withTodo + '</div><div class="stat-label">待台灣適配</div></div>' +
      '<div class="stat is-idle"><div class="stat-num">' + s.flatLayout + '</div><div class="stat-label">結構待整理</div></div>' +
      '<div class="stat is-idle"><div class="stat-num">' + (total - s.withReferences) + '</div><div class="stat-label">未附參考資料</div></div>' +
      '</div>';

    var coverage = '<div class="coverage-list">' +
      Object.keys(s.coverage).map(function (k) {
        var c = s.coverage[k];
        return '<div class="coverage-row"><span class="cov-key">' + esc(GAP_LABEL[k] || k) + '</span>' +
          '<span class="cov-track"><span class="cov-fill" style="width:' + c.pct + '%"></span></span>' +
          '<span class="cov-val">' + c.have + '/' + total + '</span></div>';
      }).join('') + '</div>';

    var cats = Object.keys(s.categories).sort(function (a, b) {
      return s.categories[b].total - s.categories[a].total ||
        a.localeCompare(b, 'zh-Hant');
    });
    var catRows = cats.map(function (c) {
      var v = s.categories[c];
      var link = v.total
        ? '<a href="?category=' + encodeURIComponent(c) + '">' + esc(c) + '</a>'
        : esc(c);
      return '<tr><td>' + link + '</td>' +
        '<td class="num">' + v.total + '</td>' +
        '<td class="num">' + (v.todo || '') + '</td>' +
        '<td>' + (v.total ? '' : '<span class="badge badge-unknown">尚無內容</span>') + '</td></tr>';
    }).join('');

    /* 最久沒被動過的幾筆 — 法規會修，久沒更新的內容風險最高 */
    var stale = DATA.entries.slice().sort(SORTS.stale).slice(0, 8).map(function (e) {
      return '<div class="gap-item"><div class="gap-title">' + esc(e.title) +
        '<small>' + esc(e.breadcrumb.join(' › ') || e.category) + '</small></div>' +
        '<span class="badge badge-plain">' + esc(e.updated || '無紀錄') + '</span>' +
        '<a class="btn btn-outline btn-sm" href="' + esc(e.domainUrl || e.skillUrl) +
        '" target="_blank" rel="noopener">看內容</a></div>';
    }).join('');

    el.dash.innerHTML =
      stats +
      '<div class="grid grid-2 mt-40">' +
      '<div><h3>後設資料覆蓋率</h3>' +
      '<p class="small muted">每一條沒填滿的，就是一個範圍明確的小任務。</p>' + coverage + '</div>' +
      '<div><h3>各分類進度</h3>' +
      '<p class="small muted">點分類名稱可直接篩選。</p>' +
      '<div class="table-wrap"><table><thead><tr><th>分類</th><th class="num">技能</th>' +
      '<th class="num">待適配</th><th></th></tr></thead><tbody>' + catRows + '</tbody></table></div></div>' +
      '</div>' +
      '<div class="mt-40"><h3>最久沒有更新的內容</h3>' +
      '<p class="small muted">法規會修。越久沒被動過的內容，越需要有人回去看一眼。</p>' +
      '<div class="gap-list">' + stale + '</div></div>';
  }

  /* ── 事件 ── */
  function bind() {
    el.filters.addEventListener('click', function (ev) {
      var chipEl = ev.target.closest ? ev.target.closest('.chip') : null;
      if (chipEl && !chipEl.disabled) {
        var key = chipEl.getAttribute('data-key');
        var value = chipEl.getAttribute('data-value');
        state[key] = state[key] === value ? '' : value;
        update();
        return;
      }
      if (ev.target.id === 'kbReset') {
        FILTER_KEYS.forEach(function (k) { state[k] = ''; });
        el.search.value = '';
        el.searchBox.classList.remove('has-value');
        update();
      }
    });

    var timer;
    el.search.addEventListener('input', function () {
      el.searchBox.classList.toggle('has-value', !!el.search.value);
      clearTimeout(timer);
      timer = setTimeout(function () { state.q = el.search.value.trim(); update(); }, 140);
    });
    el.clear.addEventListener('click', function () {
      el.search.value = '';
      state.q = '';
      el.searchBox.classList.remove('has-value');
      el.search.focus();
      update();
    });

    el.sort.addEventListener('change', function () { state.sort = el.sort.value; update(); });
    el.viewCard.addEventListener('click', function () { state.view = 'card'; update(); });
    el.viewTable.addEventListener('click', function () { state.view = 'table'; update(); });
  }

  function update() {
    el.viewCard.classList.toggle('active', state.view === 'card');
    el.viewTable.classList.toggle('active', state.view === 'table');
    el.sort.value = state.sort;
    renderFilters();
    renderResults();
    writeUrl();
  }

  /* ── 啟動 ── */
  fetch(ROOT + 'kb.json')
    .then(function (r) {
      if (!r.ok) throw new Error('kb.json ' + r.status);
      return r.json();
    })
    .then(function (d) {
      DATA = d;
      readUrl();
      el.search.value = state.q;
      el.searchBox.classList.toggle('has-value', !!state.q);
      renderDash();
      bind();
      update();
    })
    .catch(function (err) {
      el.results.innerHTML = '<div class="kb-empty"><h3>讀不到知識庫索引</h3>' +
        '<p>本機預覽請先執行 <code>python scripts/build_site.py</code> 產生 <code>docs/kb.json</code>。</p>' +
        '<p class="small muted">' + esc(err.message) + '</p></div>';
      if (el.dash) el.dash.innerHTML = '';
    });
})();
