(function (global) {
  const CFG = global.KAKOBUY_CATALOG || global.KAKOBUY_FI || {};
  const I18N = Object.assign(
    {
      locale: 'fi-FI',
      product: 'Tuote',
      productOne: '1 tuote',
      products: 'tuotetta',
      other: 'Muut',
      priceOnKakobuy: 'Hinta Kakobuyssa',
      openOnKakobuy: 'Avaa Kakobuyssa ↗',
      openAria: 'Avaa {title} Kakobuyssa (uusi välilehti)',
      openAriaCard: '{title} – avaa Kakobuyssa',
      prev: 'Edellinen',
      next: 'Seuraava',
      pageOf: 'Sivu {current} / {pages}',
      loadError: 'Tuotteita ei voitu ladata. Yritä hetken kuluttua uudelleen.',
      emptyCount: '0 tuotetta',
    },
    CFG.i18n || {}
  );

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function labelCount(n) {
    const num = Number(n) || 0;
    const formatted = num.toLocaleString(I18N.locale || undefined);
    if (num === 1 && I18N.productOne) return I18N.productOne;
    return `${formatted} ${I18N.products}`;
  }

  function formatMoney(cny) {
    const value = Number(cny);
    if (!Number.isFinite(value)) return I18N.priceOnKakobuy;
    if ((CFG.currency || 'EUR') === 'CAD') {
      const cadPerCny = Number(CFG.cadPerCny) || 0.2067;
      return `≈ C$${Math.round(value * cadPerCny)}`;
    }
    const rate = Number(CFG.cnyPerEur) || 7.7762;
    return `≈ ${Math.round(value / rate)} €`;
  }

  function formatCny(cny) {
    const value = Number(cny);
    if (!Number.isFinite(value)) return '';
    const formatted = (I18N.locale || '').startsWith('en')
      ? String(value)
      : String(value).replace('.', ',');
    return `${formatted} CNY`;
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
    return match ? match.label : id || I18N.other;
  }

  function sheetItem(hit) {
    const href = kakobuyHref(hit);
    const title = hit.title || I18N.product;
    const label = categoryLabel(hit.category);
    const img = hit.image
      ? `<img src="${esc(hit.image)}" width="750" height="750" alt="${esc(title)}" loading="lazy" decoding="async">`
      : '<img alt="" width="750" height="750">';
    return (
      `<li class="sheet-product" data-category="${esc(hit.category || '')}">` +
      img +
      `<div class="sheet-product-info"><span>${esc(label)}</span><h2>${esc(title)}</h2></div>` +
      `<div class="sheet-price"><strong>${esc(formatMoney(hit.price_cny))}</strong>` +
      `<small>${esc(formatCny(hit.price_cny))}</small></div>` +
      `<a class="sheet-buy" href="${esc(href)}" target="_blank" rel="sponsored noopener noreferrer" ` +
      `aria-label="${esc(I18N.openAria.replace('{title}', title))}">${esc(I18N.openOnKakobuy)}</a></li>`
    );
  }

  function cardItem(hit) {
    const href = kakobuyHref(hit);
    const title = hit.title || I18N.product;
    const label = categoryLabel(hit.category);
    const img = hit.image
      ? `<img src="${esc(hit.image)}" width="750" height="750" alt="${esc(title)}" loading="lazy" decoding="async">`
      : '';
    const brand = hit.brand ? `<p class="catalog-advice">${esc(hit.brand)}</p>` : '';
    return (
      `<article class="catalog-card">` +
      `<a class="catalog-image" href="${esc(href)}" target="_blank" rel="sponsored noopener noreferrer" aria-label="${esc(I18N.openAriaCard.replace('{title}', title))}">` +
      `${img}<span>${esc(label)}</span></a>` +
      `<div class="catalog-body"><h3>${esc(title)}</h3>` +
      `<div class="catalog-meta"><strong>${esc(formatMoney(hit.price_cny))}</strong>` +
      `<small>${esc(formatCny(hit.price_cny))}</small></div>${brand}` +
      `<a class="text-link" href="${esc(href)}" target="_blank" rel="sponsored noopener noreferrer">${esc(I18N.openOnKakobuy)}</a>` +
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
    i18n: I18N,
    labelCount,
    formatEur: formatMoney,
    formatMoney,
    formatCny,
    kakobuyHref,
    categoryLabel,
    sheetItem,
    cardItem,
    fetchProducts,
  };
})(window);
