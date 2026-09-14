// Product links are in HTML. These controls only filter the visible list.
const sheetControls = document.querySelector('.sheet-controls');
if (sheetControls) {
  const search = document.querySelector('#sheet-search');
  const category = document.querySelector('#sheet-category');
  const reset = document.querySelector('.sheet-reset');
  const count = document.querySelector('#sheet-count');
  const empty = document.querySelector('.sheet-empty');
  const normalize = value =>
    value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('fi-FI').trim();
  const label = n => (n === 1 ? '1 tuote' : `${n} tuotetta`);
  const products = [...document.querySelectorAll('.sheet-product')].map(element => ({
    element,
    search: normalize(element.dataset.search),
    category: element.dataset.category,
  }));
  const update = () => {
    const words = normalize(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const item of products) {
      const matches =
        (category.value === 'all' || category.value === item.category) &&
        words.every(word => item.search.includes(word));
      item.element.hidden = !matches;
      if (matches) visible++;
    }
    count.textContent = label(visible);
    empty.hidden = visible !== 0;
  };
  search.addEventListener('input', update);
  category.addEventListener('change', update);
  reset.addEventListener('click', () => {
    search.value = '';
    category.value = 'all';
    update();
    search.focus();
  });
  sheetControls.hidden = false;
  update();
}
