<?php
/** @var array $config */
/** @var array $products */
/** @var array $faqs */
$register = config('register_url');
$country = e($config['country']);
?>
<section class="lite-hero">
  <div class="container">
    <span class="hero-flag"><?= $config['flag'] ?></span>
    <h1><?= __t('hero_h1', ['country' => $country]) ?></h1>
    <p class="hero-sub"><?= __t('hero_sub') ?></p>
    <p class="hero-coupon"><?= __t('hero_coupon') ?></p>
    <a href="<?= e($register) ?>" target="_blank" rel="noopener sponsored" class="btn btn-brand btn-lg btn-block"><?= __t('hero_cta') ?></a>
  </div>
</section>

<?= class_exists(\App\Services\DestLocal::class) ? \App\Services\DestLocal::html() : '' ?>

<section class="lite-section">
  <div class="container">
    <div class="section-head"><h2><?= __t('featured_title') ?></h2></div>
    <div class="products-grid">
      <?php foreach ($products as $p): ?>
      <article class="product-card">
        <?php if (!empty($p['image'])): ?>
        <img src="<?= e($p['image']) ?>" alt="<?= e($p['title']) ?>" loading="lazy" width="280" height="280">
        <?php else: ?>
        <div class="product-placeholder" aria-hidden="true">📦</div>
        <?php endif; ?>
        <div class="product-body">
          <h3><?= e($p['title']) ?></h3>
          <p class="price"><?= e($p['local_price']) ?></p>
          <a href="<?= e(outbound_url($p['target'])) ?>" target="_blank" rel="noopener sponsored" class="btn btn-brand btn-sm"><?= __t('buy_btn') ?></a>
        </div>
      </article>
      <?php endforeach; ?>
    </div>
    <p class="section-cta"><a href="<?= e($config['full_site']) ?>" target="_blank" rel="noopener" class="btn btn-outline"><?= __t('featured_browse') ?></a></p>
  </div>
</section>

<section class="lite-section lite-categories">
  <div class="container">
    <div class="section-head section-head-cat">
      <img src="/assets/images/cssbuy-logo.png" alt="CSSBuy" class="cat-brand-mark" width="32" height="32" loading="lazy">
      <div class="section-eyebrow"><?= __t('cat_eyebrow') ?></div>
      <h2><?= __t('cat_title') ?></h2>
    </div>
    <div class="cat-grid" role="list">
      <?php foreach ($categories as $cat): ?>
      <a class="cat-card" href="<?= e($cat['url']) ?>" target="_blank" rel="noopener" role="listitem">
        <span class="emoji" aria-hidden="true"><?= $cat['emoji'] ?></span>
        <span class="cat-label"><?= e($cat['label']) ?></span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<style>
.lite-categories .section-head-cat { text-align: center; }
.lite-categories .cat-brand-mark { display: block; margin: 0 auto 10px; width: 32px; height: 32px; }
.lite-categories .cat-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 12px;
  width: 100%;
}
.lite-categories .cat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  min-height: 96px;
  padding: 22px 10px;
  background: #fff;
  border: 1px solid #e6e8ec;
  border-radius: 12px;
  color: #1a1a1a !important;
  font-weight: 600;
  font-size: 14px;
  line-height: 1.25;
  text-decoration: none;
  box-sizing: border-box;
}
.lite-categories .cat-card .emoji { font-size: 1.75rem; line-height: 1; }
.lite-categories .cat-card .cat-label { color: inherit; }
.lite-categories .cat-card:hover {
  border-color: #00C853;
  background: #e8f8ee;
  color: #009E44 !important;
}
@media (max-width: 960px) {
  .lite-categories .cat-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
}
@media (max-width: 560px) {
  .lite-categories .cat-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
</style>

<section class="lite-section">
  <div class="container">
    <div class="section-head"><h2><?= __t('how_title') ?></h2><p><?= __t('how_sub') ?></p></div>
    <div class="steps-grid">
      <div class="step-card"><div class="num">1</div><h3><?= __t('how_1_t') ?></h3><p><?= __t('how_1_d') ?></p></div>
      <div class="step-card"><div class="num">2</div><h3><?= __t('how_2_t') ?></h3><p><?= __t('how_2_d') ?></p></div>
      <div class="step-card"><div class="num">3</div><h3><?= __t('how_3_t') ?></h3><p><?= __t('how_3_d') ?></p></div>
    </div>
  </div>
</section>

<section class="lite-section">
  <div class="container">
    <div class="section-head"><h2><?= __t('why_title') ?></h2></div>
    <ul class="why-list">
      <li><?= __t('why_1') ?></li>
      <li><?= __t('why_2') ?></li>
      <li><?= __t('why_3') ?></li>
    </ul>
  </div>
</section>

<section class="lite-section trust-block">
  <div class="container">
    <h2><?= __t('trust_h2') ?></h2>
    <p><?= __t('trust_p') ?></p>
    <div class="trust-stats">
      <span><?= __t('trust_1') ?></span>
      <span><?= __t('trust_2') ?></span>
      <span><?= __t('trust_3') ?></span>
    </div>
  </div>
</section>

<section class="lite-section alt" id="faq">
  <div class="container">
    <div class="section-head"><h2><?= __t('faq_title') ?></h2></div>
    <div class="faq-list">
      <?php foreach ($faqs as $faq): ?>
      <details class="faq-item">
        <summary><?= e($faq['q']) ?></summary>
        <p><?= e($faq['a']) ?></p>
      </details>
      <?php endforeach; ?>
    </div>
  </div>
</section>
