(function (global) {
  const CFG = global.KAKOBUY_FI || {};

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function labelCount(n) {
    const num = Number(n) || 0;
    const formatted = num.toLocaleString('fi-FI');
    return num === 1 ? '1 tuote' : `${formatted} tuotetta`;
  }

  function formatEur(cny) {
    const rate = Number(CFG.cnyPerEur) || 7.7762;
    const value = Number(cny);
    if (!Number.isFinite(value)) return 'Hinta Kakobuyssa';
    return `≈ ${Math.round(value / rate)} €`;
  }

  function formatCny(cny) {
    const value = Number(cny);
    if (!Number.isFinite(value)) return '';
    return `${String(value).replace('.', ',')} CNY`;
  }

  function sourceUrl(hit) {
    const id = hit && hit.item_id;
    if (!id) return '';
    if (hit.shop === 'taobao') return `https://item.taobao.com/item.htm?id=${id}`;
    if (hit.shop === '1688') return `https://detail.1688.com/offer/${id}.html`;
    return `https://weidian.com/item.html?itemID=${id}`;
  }

  function kakobuyHref(hit) {
    const source = sourceUrl(hit);
    const aff = CFG.affcode || 'yze69';
    if (source) {
      return (
        'https://kakobuy.com/item/details?url=' +
        encodeURIComponent(source) +
        '&affcode=' +
        encodeURIComponent(aff)
      );
    }
    return '/kakobuy-spreadsheet/';
  }

  function categoryLabel(id) {
    const cats = CFG.categories || [];
    const match = cats.find(function (c) {
      return c.id === id;
    });
    return match ? match.label : id || 'Muut';
  }

  function sheetItem(hit) {
    const href = kakobuyHref(hit);
    const title = hit.title || 'Tuote';
    const label = categoryLabel(hit.category);
    const img = hit.image
      ? `<img src="${esc(hit.image)}" width="750" height="750" alt="${esc(title)}" loading="lazy" decoding="async">`
      : '<img alt="" width="750" height="750">';
    return (
      `<li class="sheet-product" data-category="${esc(hit.category || '')}">` +
      img +
      `<div class="sheet-product-info"><span>${esc(label)}</span><h2>${esc(title)}</h2></div>` +
      `<div class="sheet-price"><strong>${esc(formatEur(hit.price_cny))}</strong>` +
      `<small>${esc(formatCny(hit.price_cny))}</small></div>` +
      `<a class="sheet-buy" href="${esc(href)}" target="_blank" rel="sponsored noopener noreferrer" ` +
      `aria-label="Avaa ${esc(title)} Kakobuyssa (uusi välilehti)">Avaa Kakobuyssa ↗</a></li>`
    );
  }

  function cardItem(hit) {
    const href = kakobuyHref(hit);
    const title = hit.title || 'Tuote';
    const label = categoryLabel(hit.category);
    const img = hit.image
      ? `<img src="${esc(hit.image)}" width="750" height="750" alt="${esc(title)}" loading="lazy" decoding="async">`
      : '';
    const brand = hit.brand ? `<p class="catalog-advice">${esc(hit.brand)}</p>` : '';
    return (
      `<article class="catalog-card">` +
      `<a class="catalog-image" href="${esc(href)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="${esc(title)} – avaa Kakobuyssa">` +
      `${img}<span>${esc(label)}</span></a>` +
      `<div class="catalog-body"><h3>${esc(title)}</h3>` +
      `<div class="catalog-meta"><strong>${esc(formatEur(hit.price_cny))}</strong>` +
      `<small>${esc(formatCny(hit.price_cny))}</small></div>${brand}` +
      `<a class="text-link" href="${esc(href)}" target="_blank" rel="sponsored noopener noreferrer">Avaa Kakobuyssa ↗</a>` +
      `</div></article>`
    );
  }

  function fetchProducts(params) {
    const query = new URLSearchParams();
    query.set('page', String(params.page || 1));
    query.set('per_page', String(params.perPage || 24));
    query.set('sort', params.sort || 'newest');
    if (params.q) query.set('q', params.q);
    if (params.category && params.category !== 'all') query.set('category', params.category);
    return fetch((CFG.api || '/api/products.php') + '?' + query.toString(), { cache: 'no-store' }).then(
      function (response) {
        if (!response.ok) throw new Error('products ' + response.status);
        return response.json();
      }
    );
  }

  global.KakobuyCatalog = {
    esc,
    labelCount,
    formatEur,
    formatCny,
    kakobuyHref,
    categoryLabel,
    sheetItem,
    cardItem,
    fetchProducts,
  };
})(window);
