(function () {
  const grid = document.querySelector('#finds-grid');
  const category = document.querySelector('#catalog-category');
  if (!grid || !category || !window.KakobuyCatalog) return;

  const Catalog = window.KakobuyCatalog;
  const count = document.querySelector('#catalog-count');
  const filter = category.closest('.catalog-filter');
  const empty = document.querySelector('.finds-empty');
  let requestId = 0;

  function load() {
    const cat = category.value || 'all';
    const id = ++requestId;
    grid.setAttribute('aria-busy', 'true');
    Catalog.fetchProducts({ category: cat, page: 1, perPage: 24 })
      .then(function (data) {
        if (id !== requestId) return;
        const hits = (data && data.hits) || [];
        const found = data && data.found != null ? data.found : hits.length;
        grid.innerHTML = hits.map(Catalog.cardItem).join('');
        if (count) count.textContent = Catalog.labelCount(found);
        if (empty) empty.hidden = hits.length !== 0;
        const nextHash = cat === 'all' ? '' : '#' + encodeURIComponent(cat);
        if (location.hash !== nextHash) {
          history.replaceState(null, '', location.pathname + location.search + nextHash);
        }
      })
      .catch(function () {
        if (id !== requestId) return;
        grid.innerHTML = '';
        if (empty) {
          empty.hidden = false;
          empty.textContent = 'Tuotteita ei voitu ladata. Yritä hetken kuluttua uudelleen.';
        }
        if (count) count.textContent = '0 tuotetta';
      })
      .finally(function () {
        if (id === requestId) grid.removeAttribute('aria-busy');
      });
  }

  const fromHash = decodeURIComponent((location.hash || '').slice(1));
  if ([...category.options].some(function (opt) { return opt.value === fromHash; })) {
    category.value = fromHash;
  }
  if (filter) filter.hidden = false;
  category.addEventListener('change', load);
  window.addEventListener('hashchange', function () {
    const next = decodeURIComponent((location.hash || '').slice(1)) || 'all';
    if (category.value !== next && [...category.options].some(function (opt) { return opt.value === next; })) {
      category.value = next;
    }
    load();
  });
  load();
})();
