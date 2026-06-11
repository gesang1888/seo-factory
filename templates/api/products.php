<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=300');
header('Access-Control-Allow-Origin: *');

$upstream = 'https://w2clinks.com/public/typesense-search.php';
$page = max(1, (int)($_GET['page'] ?? 1));
$perPage = max(1, min(24, (int)($_GET['per_page'] ?? 12)));
$sort = preg_replace('/[^a-z0-9_-]/i', '', (string)($_GET['sort'] ?? 'newest')) ?: 'newest';
$keyword = trim((string)($_GET['keyword'] ?? ''));
$category = trim((string)($_GET['category'] ?? ''));

$query = http_build_query(array_filter([
    'page' => $page,
    'per_page' => $perPage,
    'sort' => $sort,
    'keyword' => $keyword !== '' ? $keyword : null,
    'category' => $category !== '' ? $category : null,
]));

$url = $upstream . '?' . $query;

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_CONNECTTIMEOUT => 8,
    CURLOPT_TIMEOUT => 15,
    CURLOPT_HTTPHEADER => ['Accept: application/json', 'User-Agent: OrientDigSpreadsheetProxy/1.0'],
]);
$body = curl_exec($ch);
$code = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

if ($body === false || $code < 200 || $code >= 300) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'hits' => [], 'found' => 0]);
    exit;
}

$data = json_decode($body, true);
if (!is_array($data)) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'hits' => [], 'found' => 0]);
    exit;
}

$base = 'https://w2clinks.com';
$hits = [];
foreach (($data['hits'] ?? []) as $row) {
    if (!is_array($row)) continue;
    $u = (string)($row['url'] ?? '');
    if ($u !== '' && $u[0] === '/') $u = $base . $u;
    $hits[] = [
        'title' => (string)($row['title'] ?? ''),
        'url' => $u,
        'image' => (string)($row['image'] ?? ''),
        'price_cny' => $row['price'] ?? null,
        'category' => (string)($row['category'] ?? ''),
        'brand' => (string)($row['brand'] ?? ''),
    ];
}

echo json_encode([
    'ok' => true,
    'found' => (int)($data['found'] ?? count($hits)),
    'page' => $page,
    'per_page' => $perPage,
    'hits' => $hits,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
