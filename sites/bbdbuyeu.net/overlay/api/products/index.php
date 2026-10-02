<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=120');
header('Access-Control-Allow-Origin: *');
header('X-Robots-Tag: noindex, nofollow');

$upstream = 'https://w2clinks.com/public/typesense-search.php';
$page = max(1, (int)($_GET['page'] ?? 1));
$perPage = max(1, min(60, (int)($_GET['per_page'] ?? $_GET['limit'] ?? 24)));
$sort = preg_replace('/[^a-z0-9_-]/i', '', (string)($_GET['sort'] ?? 'newest')) ?: 'newest';
$keyword = trim((string)($_GET['keyword'] ?? $_GET['q'] ?? ''));
$category = trim((string)($_GET['category'] ?? ''));

$query = http_build_query(array_filter([
    'page' => $page,
    'per_page' => $perPage,
    'sort' => $sort,
    'keyword' => $keyword !== '' ? $keyword : null,
    'category' => $category !== '' ? $category : null,
]));

$ch = curl_init($upstream . '?' . $query);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_CONNECTTIMEOUT => 8,
    CURLOPT_TIMEOUT => 15,
    CURLOPT_HTTPHEADER => ['Accept: application/json', 'User-Agent: BBDBuyEUProductAPI/1.0'],
]);
$body = curl_exec($ch);
$code = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

if ($body === false || $code < 200 || $code >= 300) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'hits' => [], 'items' => [], 'found' => 0, 'total' => 0, 'totalProducts' => 0]);
    exit;
}

$data = json_decode($body, true);
if (!is_array($data)) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'hits' => [], 'items' => [], 'found' => 0, 'total' => 0, 'totalProducts' => 0]);
    exit;
}

$base = 'https://w2clinks.com';
$hits = [];
foreach (($data['hits'] ?? []) as $row) {
    if (!is_array($row)) {
        continue;
    }
    $title = (string)($row['title'] ?? '');
    $aid = (int)($row['aid'] ?? 0);
    $cny = (float)($row['price'] ?? 0);
    $u = (string)($row['url'] ?? '');
    if ($u !== '' && isset($u[0]) && $u[0] === '/') {
        $u = $base . $u;
    }
    $hits[] = [
        'aid' => $aid,
        'id' => $aid,
        'title' => $title,
        'name' => $title,
        'url' => $u,
        'image' => (string)($row['image'] ?? ''),
        'img' => (string)($row['image'] ?? ''),
        'price_cny' => $cny,
        'price' => $cny > 0 ? round($cny / 7.2, 2) : 0,
        'category' => (string)($row['category'] ?? ''),
        'brand' => (string)($row['brand'] ?? ''),
    ];
}

$found = (int)($data['found'] ?? count($hits));
echo json_encode([
    'ok' => true,
    'hits' => $hits,
    'items' => $hits,
    'products' => $hits,
    'found' => $found,
    'total' => $found,
    'totalProducts' => $found,
    'page' => $page,
    'per_page' => $perPage,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
