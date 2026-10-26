/* USFans Spreadsheet search */
(function () {
  const API = '/api/products/index.php';
  const grid = document.getElementById('search-results');
  const status = document.getElementById('search-status');
  const form = document.getElementById('search-form');
  const input = document.getElementById('search-input');
  const chips = document.querySelectorAll('[data-cat-filter]');
  if (!grid || !form) return;

  const params = new URLSearchParams(location.search);
  let q = params.get('q') || params.get('keyword') || '';
  let category = params.get('category') || '';
  let typeid = params.get('typeid') || '';
  let page = parseInt(params.get('page') || '1', 10);

  if (input && q) input.value = q;

  function usd(cny) {
    const n = parseFloat(String(cny).replace(/[^\d.]/g, ''));
    if (!n) return '';
    return '≈ $' + (n * 0.139).toFixed(2);
  }

  function proxyImg(u) {
    if (!u) return '';
    var src = u.indexOf('/wd-img/') === 0 ? u : u.replace(/^https?:\/\/si\.geilicdn\.com\//i, '/wd-img/si.geilicdn.com/');
    if (src.indexOf('_wp=1') === -1) src += (src.indexOf('?') === -1 ? '?' : '&') + '_wp=1';
    return src;
  }
  function card(item) {
    const src = proxyImg(item.image);
    const img = src
      ? `background:#f0f0ee url('${src.replace(/'/g, "%27")}') center/cover no-repeat`
      : 'background:var(--bg-alt)';
    const price = item.price ? `¥${item.price}` : '';
    const usdP = item.price ? usd(item.price) : '';
    return `<a href="${item.href}" target="_blank" rel="noopener" class="prod">
      <div class="prod-img" style="${img}"><span class="qc">📷 QC</span></div>
      <div class="prod-body">
        <h4>${item.title}</h4>
        <div class="price">${price}${usdP ? ` <small>${usdP}</small>` : ''}</div>
      </div>
    </a>`;
  }

  async function load() {
    grid.innerHTML = '<p class="search-loading">Loading finds…</p>';
    if (status) status.textContent = 'Searching…';
    const qs = new URLSearchParams({ page: String(page), limit: '24', sort: 'newest' });
    if (q) qs.set('q', q);
    if (category) qs.set('category', category);
    if (typeid) qs.set('typeid', typeid);
    try {
      const res = await fetch(`${API}?${qs}`);
      const data = await res.json();
      const items = data.items || data.products || [];
      const total = data.total || items.length;
      if (!items.length) {
        grid.innerHTML = '<p class="search-empty">No finds matched. Try a different keyword or browse <a href="/categories/">all 33 categories</a>.</p>';
        if (status) status.textContent = q ? `No results for "${q}"` : 'No results';
        return;
      }
      grid.innerHTML = items.map(card).join('');
      const label = q ? `"${q}"` : (category || 'all finds');
      if (status) status.textContent = `Showing ${items.length} of ${total.toLocaleString()}+ · ${label}`;
    } catch (e) {
      grid.innerHTML = '<p class="search-empty">Search temporarily unavailable. <a href="https://w2clinks.com/spreadsheet/usfans/" target="_blank" rel="noopener">Open full spreadsheet →</a></p>';
    }
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    q = (input.value || '').trim();
    page = 1;
    category = '';
    typeid = '';
    const u = new URL(location.href);
    u.searchParams.set('q', q);
    u.searchParams.delete('category');
    u.searchParams.delete('typeid');
    u.searchParams.delete('page');
    history.replaceState(null, '', u);
    chips.forEach(c => c.classList.remove('active'));
    load();
  });

  chips.forEach(function (chip) {
    if (chip.dataset.category === category) chip.classList.add('active');
    chip.addEventListener('click', function () {
      category = chip.dataset.category || '';
      typeid = chip.dataset.typeid || '';
      q = '';
      if (input) input.value = '';
      page = 1;
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const u = new URL(location.href);
      if (category) { u.searchParams.set('category', category); u.searchParams.set('typeid', typeid); }
      else { u.searchParams.delete('category'); u.searchParams.delete('typeid'); }
      u.searchParams.delete('q');
      history.replaceState(null, '', u);
      load();
    });
  });

  load();
})();
