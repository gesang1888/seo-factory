<?php
/** @var array $config */
/** @var string $page_title */
/** @var string $meta_desc */
$c = $config;
$host = $GLOBALS['domain_host'] ?? '';
$reqPath = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$reqPath = ($reqPath !== '/' ? rtrim($reqPath, '/') : '/') ?: '/';
// GSC_CANONICAL_TRIM
$canonical = canonical_url($reqPath);
$canonical = strtok($canonical, '?');
$robots = $robots ?? 'index, follow';
$fontsBody = str_replace(' ', '+', $c['fonts']['body']);
$fontsDisplay = str_replace(' ', '+', $c['fonts']['display']);
$register = config('register_url');
$tpl = e($c['template']);
$lang = e($c['lang']);
$spreadsheetSite = rtrim($c['full_site'], '/');
$navGuides = nav_guide_slugs();
?>
<!DOCTYPE html>
<html lang="<?= $lang ?>">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><?= e($page_title) ?></title>
<meta name="description" content="<?= e($meta_desc) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<meta property="og:type" content="website">
<meta property="og:title" content="<?= e($page_title) ?>">
<meta property="og:description" content="<?= e($meta_desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta name="theme-color" content="#E85D1A">
<link rel="icon" href="/assets/images/favicon.ico" type="image/x-icon">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=<?= $fontsBody ?>:wght@400;600;700&family=<?= $fontsDisplay ?>:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/lite.css?v=4">
<style id="site-theme">:root {
  --color-brand-orange: #E85D1A;
  --color-local-primary: <?= e($c['colors']['local_primary']) ?>;
  --color-local-accent: <?= e($c['colors']['local_accent']) ?>;
  --font-main: "<?= e($c['fonts']['body']) ?>", Inter, system-ui, sans-serif;
  --font-display: "<?= e($c['fonts']['display']) ?>", Georgia, serif;
}</style>
<script type="application/ld+json"><?= json_encode([
    '@context' => 'https://schema.org',
    '@type' => 'WebSite',
    'name' => 'CSSBuy ' . $c['country'],
    'url' => 'https://' . $host . '/',
    'description' => $meta_desc,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
<?php if (!empty($faq_schema)): ?>
<script type="application/ld+json"><?= $faq_schema ?></script>
<?php endif; ?>
</head>
<body class="tpl-<?= $tpl ?>" data-currency="<?= e($c['currency']['code']) ?>" data-rate="<?= e((string)$c['currency']['rate']) ?>">
<div class="lite-topbar"><div class="container"><?= __t('topbar') ?> · <a href="https://www.cssbuy.com/" target="_blank" rel="noopener">CSSBuy.com →</a></div></div>
<header class="lite-header">
  <div class="container lite-header-inner">
    <a href="/" class="lite-brand">
      <img src="/assets/images/cssbuy-logo.png" alt="CSSBuy" width="36" height="36">
      <span>CSSBuy<small><?= e($c['country']) ?> · <?= e($c['currency']['code']) ?></small></span>
      <span class="lite-flag"><?= $c['flag'] ?></span>
    </a>
    <nav class="lite-nav">
      <a href="/"><?= __t('nav_home') ?></a>
      <?php foreach ($navGuides as $slug): ?>
      <a href="/guide/<?= e($slug) ?>"><?= e(\App\Services\GuideContent::get($c['lang'], $slug)['nav_label'] ?? ucfirst(str_replace('-', ' ', $slug))) ?></a>
      <?php endforeach; ?>
      <a href="/spreadsheet"><?= __t('nav_browse_finds') ?></a>
    </nav>
    <a href="<?= e($register) ?>" target="_blank" rel="noopener sponsored" class="btn btn-brand"><?= __t('nav_register') ?></a>
  </div>
</header>
<main><?= $content ?? '' ?></main>
<footer class="lite-footer">
  <div class="container lite-footer-inner">
    <div class="lite-footer-brand">
      <img src="/assets/images/cssbuy-logo.png" alt="CSSBuy" width="32" height="32">
      <span>CSSBuy <?= e($c['country']) ?></span>
    </div>
    <p class="footer-cluster-note"><strong><?= __t('footer_agent_role') ?></strong> · <?= __t('footer_spreadsheet_role') ?>
      <a href="<?= e($spreadsheetSite) ?>/" target="_blank" rel="noopener"><?= e($spreadsheetSite) ?></a></p>
    <p class="footer-guide-links">
      <?php
      $footerGuideLinks = [];
      foreach (array_slice(guide_page_slugs(), 0, 5) as $slug) {
          $g = \App\Services\GuideContent::get($c['lang'], $slug);
          if ($g) {
              $footerGuideLinks[] = '<a href="/guide/' . e($slug) . '">' . e($g['nav_label'] ?? $slug) . '</a>';
          }
      }
      echo implode(' · ', $footerGuideLinks);
      ?>
    </p>
    <p class="disc"><?= __t('footer_disclaimer') ?></p>
    <p><a href="/sitemap.xml"><?= __t('footer_sitemap') ?></a></p>
  </div>
</footer>
<div class="whatsapp-float" title="<?= e(__t('wa_tooltip')) ?>" onclick="window.open('https://wa.me/8615396628356','_blank')" role="button" aria-label="WhatsApp">
  <span class="flag-badge"><?= $c['flag'] ?></span>
  <svg viewBox="0 0 24 24" fill="#fff" width="28" height="28" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.097-.125.147-.172.183-.183.099-.198.213-.424.297-.646.084-.222.033-.402-.015-.562-.048-.16-.446-1.084-.612-1.484-.166-.4-.333-.346-.446-.354-.114-.008-.247-.01-.38-.01a.73.73 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.809 2.049.099.133 1.397 2.134 3.384 2.991.472.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 0 0 .614.614l4.458-1.495A11.945 11.945 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818a9.818 9.818 0 0 1-5.006-1.372l-.358-.213-2.642.886.886-2.578-.233-.375A9.818 9.818 0 1 1 12 21.818z"/></svg>
</div>
<script src="/assets/js/lite.js?v=1" defer></script>
</body>
</html>
