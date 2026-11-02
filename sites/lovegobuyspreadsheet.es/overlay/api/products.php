<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$upstream = 'https://w2clinks.com/public/typesense-search.php';
$page = max(1, (int)($_GET['page'] ?? 1));
$perPage = max(1, min(48, (int)($_GET['per_page'] ?? $_GET['limit'] ?? 24)));
$sort = preg_replace('/[^a-z0-9_-]/i', '', (string)($_GET['sort'] ?? 'newest')) ?: 'newest';
$q = trim((string)($_GET['q'] ?? $_GET['keyword'] ?? ''));
$category = trim((string)($_GET['category'] ?? ''));
$brand = trim((string)($_GET['brand'] ?? ''));
$typeid = trim((string)($_GET['typeid'] ?? ''));

header('Cache-Control: public, max-age=' . ($q !== '' || $category !== '' || $brand !== '' ? 60 : 300));

function w2c_api_key(): string
{
    foreach (['W2CLINKS_API_KEY', 'W2C_PRODUCTS_API_KEY'] as $name) {
        $env = getenv($name);
        if (is_string($env) && $env !== '') {
            return $env;
        }
    }
    $local = __DIR__ . '/config.local.php';
    if (is_file($local)) {
        $cfg = include $local;
        if (is_array($cfg) && !empty($cfg['api_key'])) {
            return (string) $cfg['api_key'];
        }
    }
    return '';
}

$params = [
    'page' => $page,
    'per_page' => $perPage,
    'sort' => $sort,
];
if ($q !== '') {
    $params['q'] = $q;
}
if ($category !== '') {
    $params['category'] = $category;
}
if ($brand !== '') {
    $params['brand'] = $brand;
}
if ($typeid !== '' && ctype_digit($typeid)) {
    $params['typeid'] = $typeid;
}

$apiKey = w2c_api_key();
if ($apiKey !== '') {
    $params['api_key'] = $apiKey;
}

$url = $upstream . '?' . http_build_query($params);

$headers = [
    'Accept: application/json',
    'User-Agent: LoveGoBuySpreadsheetProxy/1.1',
];
if ($apiKey !== '') {
    $headers[] = 'Authorization: Bearer ' . $apiKey;
    $headers[] = 'X-API-Key: ' . $apiKey;
    $headers[] = 'X-TYPESENSE-API-KEY: ' . $apiKey;
}

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_CONNECTTIMEOUT => 8,
    CURLOPT_TIMEOUT => 15,
    CURLOPT_HTTPHEADER => $headers,
]);
$body = curl_exec($ch);
$code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);

if ($body === false || $code < 200 || $code >= 300) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'hits' => [], 'found' => 0, 'items' => []]);
    exit;
}
echo $body;
