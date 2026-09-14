document.querySelectorAll('[data-catalog]').forEach(link => {
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
});
const menuButton = document.querySelector('.menu-button');
const navLinks = document.querySelector('.nav-links');
if (menuButton && navLinks) {
  menuButton.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  navLinks.querySelectorAll('a').forEach(link =>
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      menuButton.setAttribute('aria-expanded', 'false');
    })
  );
}
document.querySelectorAll('.faq-question').forEach(button =>
  button.addEventListener('click', () => {
    const item = button.closest('.faq-item');
    const opening = !item.classList.contains('open');
    item.classList.toggle('open', opening);
    button.setAttribute('aria-expanded', String(opening));
  })
);
document.querySelectorAll('[data-year]').forEach(item => {
  item.textContent = String(new Date().getFullYear());
});

const categorySelect = document.querySelector('#catalog-category');
if (categorySelect) {
  const groups = [...document.querySelectorAll('.catalog-group')];
  const count = document.querySelector('#catalog-count');
  const label = n => (n === 1 ? '1 tuote' : `${n} tuotetta`);
  const updateCategory = (value, updateUrl = false) => {
    const valid = value === 'all' || groups.some(group => group.id === value);
    const selected = valid ? value : 'all';
    categorySelect.value = selected;
    let visibleCount = 0;
    groups.forEach(group => {
      group.hidden = selected !== 'all' && group.id !== selected;
      if (!group.hidden) visibleCount += group.querySelectorAll('.catalog-card').length;
    });
    if (count) count.textContent = label(visibleCount);
    if (updateUrl) {
      history.replaceState(
        null,
        '',
        location.pathname + location.search + (selected === 'all' ? '' : '#' + selected)
      );
    }
  };
  categorySelect.closest('.catalog-filter').hidden = false;
  const jump = document.querySelector('.catalog-jump');
  if (jump) jump.hidden = true;
  updateCategory(location.hash.slice(1));
  categorySelect.addEventListener('change', () => updateCategory(categorySelect.value, true));
  window.addEventListener('hashchange', () => updateCategory(location.hash.slice(1)));
}
