(function () {
  const sheetControls = document.querySelector('.sheet-controls');
  const list = document.querySelector('#sheet-products');
  if (!sheetControls || !list || !window.KakobuyCatalog) return;

  const Catalog = window.KakobuyCatalog;
  const search = document.querySelector('#sheet-search');
  const category = document.querySelector('#sheet-category');
  const reset = document.querySelector('.sheet-reset');
  const count = document.querySelector('#sheet-count');
  const empty = document.querySelector('.sheet-empty');
  const pager = document.querySelector('#sheet-pager');
  const PER_PAGE = 24;
  let page = 1;
  let timer = 0;
  let requestId = 0;

  function stateFromUrl() {
    const params = new URLSearchParams(location.search);
    return {
      q: (params.get('q') || '').trim(),
      category: params.get('category') || 'all',
      page: Math.max(1, parseInt(params.get('page') || '1', 10) || 1),
    };
  }

  function writeUrl(q, cat, nextPage) {
    const params = new URLSearchParams();
    if (q) params.set('q', q);
    if (cat && cat !== 'all') params.set('category', cat);
    if (nextPage > 1) params.set('page', String(nextPage));
    const next = location.pathname + (params.toString() ? '?' + params.toString() : '');
    history.replaceState(null, '', next);
  }

  function renderPager(found, current) {
    if (!pager) return;
    const pages = Math.max(1, Math.ceil((Number(found) || 0) / PER_PAGE));
    if (pages <= 1) {
      pager.innerHTML = '';
      pager.hidden = true;
      return;
    }
    pager.hidden = false;
    const prevDisabled = current <= 1 ? ' disabled' : '';
    const nextDisabled = current >= pages ? ' disabled' : '';
    pager.innerHTML =
      `<button type="button" class="sheet-page" data-page="${current - 1}"${prevDisabled}>Edellinen</button>` +
      `<span>Sivu ${current.toLocaleString('fi-FI')} / ${pages.toLocaleString('fi-FI')}</span>` +
      `<button type="button" class="sheet-page" data-page="${current + 1}"${nextDisabled}>Seuraava</button>`;
  }

  function load() {
    const q = (search.value || '').trim();
    const cat = category.value || 'all';
    const id = ++requestId;
    list.setAttribute('aria-busy', 'true');
    Catalog.fetchProducts({ q, category: cat, page, perPage: PER_PAGE })
      .then(function (data) {
        if (id !== requestId) return;
        const hits = (data && data.hits) || [];
        const found = data && data.found != null ? data.found : hits.length;
        list.innerHTML = hits.map(Catalog.sheetItem).join('');
        if (count) count.textContent = Catalog.labelCount(found);
        if (empty) empty.hidden = hits.length !== 0;
        renderPager(found, page);
        writeUrl(q, cat, page);
      })
      .catch(function () {
        if (id !== requestId) return;
        list.innerHTML = '';
        if (empty) {
          empty.hidden = false;
          empty.textContent = 'Tuotteita ei voitu ladata. Yritä hetken kuluttua uudelleen.';
        }
        if (count) count.textContent = '0 tuotetta';
        renderPager(0, 1);
      })
      .finally(function () {
        if (id === requestId) list.removeAttribute('aria-busy');
      });
  }

  const initial = stateFromUrl();
  search.value = initial.q;
  if ([...category.options].some(function (opt) { return opt.value === initial.category; })) {
    category.value = initial.category;
  }
  page = initial.page;

  search.addEventListener('input', function () {
    window.clearTimeout(timer);
    timer = window.setTimeout(function () {
      page = 1;
      load();
    }, 280);
  });
  category.addEventListener('change', function () {
    page = 1;
    load();
  });
  if (reset) {
    reset.addEventListener('click', function () {
      search.value = '';
      category.value = 'all';
      page = 1;
      load();
      search.focus();
    });
  }
  if (pager) {
    pager.addEventListener('click', function (event) {
      const button = event.target.closest('[data-page]');
      if (!button || button.disabled) return;
      const next = parseInt(button.getAttribute('data-page') || '1', 10);
      if (!Number.isFinite(next) || next < 1) return;
      page = next;
      load();
      list.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
  }

  const chips = document.querySelector('.sheet-categories');
  if (chips) {
    chips.addEventListener('click', function (event) {
      const link = event.target.closest('[data-sheet-category]');
      if (!link) return;
      event.preventDefault();
      category.value = link.getAttribute('data-sheet-category') || 'all';
      page = 1;
      load();
      sheetControls.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
  }

  sheetControls.hidden = false;
  if (typeof search.value !== "string") return;
  load();
})();
