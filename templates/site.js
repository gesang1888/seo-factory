(function () {
  var CFG = window.OD_SITE_CONFIG || {};
  var rates = (CFG.currencies || []).reduce(function (acc, c) {
    acc[c.code] = c.rateFromCny || 1;
    return acc;
  }, {});
  var symbols = (CFG.currencies || []).reduce(function (acc, c) {
    acc[c.code] = c.symbol || c.code;
    return acc;
  }, {});

  function getCurrency() {
    try {
      return localStorage.getItem('od_currency') || CFG.defaultCurrency || 'USD';
    } catch (e) {
      return CFG.defaultCurrency || 'USD';
    }
  }

  function setCurrency(code) {
    try {
      localStorage.setItem('od_currency', code);
    } catch (e) {}
    document.documentElement.setAttribute('data-currency', code);
    applyPrices();
  }

  function formatPrice(cny) {
    if (cny == null || cny === '') return '';
    var n = Number(cny);
    if (!isFinite(n)) return '';
    var code = getCurrency();
    var rate = rates[code] || rates.CNY || 1;
    var sym = symbols[code] || code + ' ';
    var val = code === 'CNY' ? n : n * rate;
    return sym + (code === 'CNY' ? Math.round(val) : val.toFixed(2));
  }

  function applyPrices() {
    document.querySelectorAll('[data-price-cny]').forEach(function (el) {
      el.textContent = formatPrice(el.getAttribute('data-price-cny'));
    });
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderProducts(hits) {
    var grid = document.getElementById('od-product-grid');
    if (!grid || !hits || !hits.length) return;
    var spreadsheet = CFG.spreadsheetUrl || 'https://w2clinks.com/spreadsheet/';
    grid.innerHTML = hits
      .map(function (p) {
        var href = p.url || spreadsheet;
        var img = p.image
          ? '<img src="' + esc(p.image) + '" alt="' + esc(p.title) + '" loading="lazy" decoding="async">'
          : '<div class="od-no-img">Find</div>';
        var price = p.price_cny != null ? '<span class="od-price" data-price-cny="' + esc(p.price_cny) + '"></span>' : '';
        return (
          '<a class="od-product-card" href="' +
          esc(href) +
          '" target="_blank" rel="noopener">' +
          '<div class="od-product-thumb">' +
          img +
          '</div><div class="od-product-body"><h3>' +
          esc(p.title) +
          '</h3><p class="od-product-meta">' +
          esc(p.category || '') +
          '</p>' +
          price +
          '</div></a>'
        );
      })
      .join('');
    applyPrices();
  }

  function fetchProducts() {
    var grid = document.getElementById('od-product-grid');
    if (!grid) return;
    fetch('/api/products.php?per_page=12&sort=newest', { cache: 'no-store' })
      .then(function (r) {
        return r.json();
      })
      .then(function (d) {
        if (d && d.ok && d.hits) renderProducts(d.hits);
      })
      .catch(function () {});
  }

  function renderHelpArticles(container, articles) {
    if (!container || !articles || !articles.length) return;
    container.innerHTML = articles
      .map(function (a) {
        var imgs = (a.images || [])
          .slice(0, 2)
          .map(function (src) {
            return '<img src="' + esc(src) + '" alt="" loading="lazy" class="od-policy-img">';
          })
          .join('');
        return (
          '<article class="od-policy-article">' +
          '<h3>' +
          esc(a.title) +
          '</h3>' +
          (imgs ? '<div class="od-policy-imgs">' + imgs + '</div>' : '') +
          '<div class="od-policy-html">' +
          a.html +
          '</div>' +
          '<p class="od-policy-src"><a href="' +
          esc(a.source) +
          '" target="_blank" rel="noopener">Read on OrientDig Help Center</a></p>' +
          '</article>'
        );
      })
      .join('');
  }

  function fetchHelp(topic) {
    var box = document.getElementById('od-live-help');
    if (!box) return;
    box.classList.add('is-loading');
    fetch('/api/orientdig-help.php?topic=' + encodeURIComponent(topic), { cache: 'no-store' })
      .then(function (r) {
        return r.json();
      })
      .then(function (d) {
        if (d && d.articles) renderHelpArticles(box, d.articles);
        var ts = document.getElementById('od-live-ts');
        if (ts && d.fetched_at) ts.textContent = new Date(d.fetched_at).toLocaleString();
      })
      .catch(function () {})
      .finally(function () {
        box.classList.remove('is-loading');
      });
  }

  function bindLang() {
    var sel = document.getElementById('od-lang-select');
    if (!sel) return;
    sel.addEventListener('change', function () {
      var url = sel.options[sel.selectedIndex].getAttribute('data-url');
      if (url) window.location.href = url;
    });
  }

  function bindCurrency() {
    var sel = document.getElementById('od-currency-select');
    if (!sel) return;
    sel.value = getCurrency();
    sel.addEventListener('change', function () {
      setCurrency(sel.value);
    });
    document.documentElement.setAttribute('data-currency', getCurrency());
    applyPrices();
  }

  function bindRefresh() {
    var btn = document.getElementById('od-refresh-help');
    if (!btn) return;
    btn.addEventListener('click', function () {
      fetchHelp(btn.getAttribute('data-topic') || 'shipping');
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    bindLang();
    bindCurrency();
    bindRefresh();
    fetchProducts();
    var helpBox = document.getElementById('od-live-help');
    if (helpBox) fetchHelp(helpBox.getAttribute('data-topic') || 'shipping');
  });
})();
