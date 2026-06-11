<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=600');
header('Access-Control-Allow-Origin: *');

$topic = strtolower(trim((string)($_GET['topic'] ?? 'shipping')));
$slugMap = [
    'shipping' => [
        'the-duration-for-which-parcel-can-be-stored-in-the-orientdig-warehouse-for-free-is-30-days',
        'why-should-i-combine-delivery',
        'compensation-standard-for-insured-parcel',
        'about-orientdig-2',
    ],
    'coupons' => [
        'affiliate-system-rules',
        'about-orientdig-2',
    ],
    'coupon' => [
        'affiliate-system-rules',
        'about-orientdig-2',
    ],
];
$slugs = $slugMap[$topic] ?? $slugMap['shipping'];
$base = 'https://orientdig.com/wp-json/wp/v2/help-center';

function http_get(string $url): ?string {
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_CONNECTTIMEOUT => 8,
        CURLOPT_TIMEOUT => 20,
        CURLOPT_HTTPHEADER => ['Accept: application/json', 'User-Agent: OrientDigHelpProxy/1.0'],
    ]);
    $body = curl_exec($ch);
    $code = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    if ($body === false || $code < 200 || $code >= 300) return null;
    return $body;
}

function pick_english(array $posts): ?array {
    foreach ($posts as $p) {
        $title = html_entity_decode(strip_tags((string)($p['title']['rendered'] ?? '')), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        if ($title !== '' && preg_match('/^[\x20-\x7E]+$/', $title)) return $p;
    }
    return $posts[0] ?? null;
}

function fix_html(string $html): string {
    $html = preg_replace('#src="/#', 'src="https://orientdig.com/', $html);
    $html = preg_replace('#href="/#', 'href="https://orientdig.com/', $html);
    return preg_replace('#<script[^>]*>.*?</script>#is', '', $html);
}

$articles = [];
$seen = [];
foreach ($slugs as $slug) {
    $raw = http_get($base . '?slug=' . rawurlencode($slug));
    if (!$raw) continue;
    $posts = json_decode($raw, true);
    if (!is_array($posts)) continue;
    $post = pick_english($posts);
    if (!$post) continue;
    $id = (int)($post['id'] ?? 0);
    if ($id && isset($seen[$id])) continue;
    if ($id) $seen[$id] = true;
    $html = fix_html((string)($post['content']['rendered'] ?? ''));
    preg_match_all('#src="([^"]+\.(?:png|jpe?g|webp|gif))"#i', $html, $m);
    $articles[] = [
        'slug' => $slug,
        'title' => html_entity_decode(strip_tags((string)($post['title']['rendered'] ?? '')), ENT_QUOTES | ENT_HTML5, 'UTF-8'),
        'html' => $html,
        'images' => array_values(array_unique($m[1] ?? [])),
        'source' => 'https://orientdig.com/help-center-detail?slug=' . rawurlencode($slug),
    ];
}

echo json_encode([
    'ok' => count($articles) > 0,
    'topic' => $topic,
    'fetched_at' => gmdate('c'),
    'articles' => $articles,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
