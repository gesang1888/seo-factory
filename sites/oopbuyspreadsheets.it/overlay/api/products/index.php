<?php
declare(strict_types=1);
$_GET['per_page'] = (string) max(1, min(48, (int) ($_GET['limit'] ?? $_GET['per_page'] ?? 24)));
$upstream = dirname(__DIR__) . '/products.php';
if (!is_file($upstream)) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code(502);
    echo json_encode(['ok' => false, 'items' => []]);
    exit;
}
ob_start();
require $upstream;
$raw = ob_get_clean();
$data = json_decode((string) $raw, true);
if (!is_array($data)) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code(502);
    echo json_encode(['ok' => false, 'items' => []]);
    exit;
}
$sheet = 'https://w2clinks.com/spreadsheet/oopbuy/';
$base = 'https://w2clinks.com';
$items = [];
foreach (($data['hits'] ?? $data['items'] ?? []) as $h) {
    if (!is_array($h)) {
        continue;
    }
    $href = (string) ($h['url'] ?? $h['href'] ?? $h['target'] ?? '');
    if ($href === '') {
        $href = $sheet;
    } elseif ($href[0] === '/') {
        $href = $base . $href;
    }
    $items[] = [
        'title' => (string) ($h['title'] ?? ''),
        'image' => (string) ($h['image'] ?? ''),
        'price' => $h['price_cny'] ?? $h['price'] ?? '',
        'currency' => (string) ($h['currency'] ?? 'CNY'),
        'href' => $href,
        'target' => $href,
    ];
}
header('Content-Type: application/json; charset=utf-8');
echo json_encode(
    [
        'ok' => true,
        'items' => $items,
        'products' => $items,
        'found' => $data['found'] ?? count($items),
        'page' => $data['page'] ?? 1,
        'spreadsheet' => $sheet,
    ],
    JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
);
