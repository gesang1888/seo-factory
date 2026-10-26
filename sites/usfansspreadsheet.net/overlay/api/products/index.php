<?php
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: public, max-age=300');
header('Access-Control-Allow-Origin: *');

$w2cBase = 'https://w2clinks.com';
$searchApi = $w2cBase . '/public/typesense-search.php';
$apiKey = getenv('USFANS_W2C_API_KEY') ?: '';
$spreadsheet = 'https://w2clinks.com/spreadsheet/usfans/';
$limit = max(1, min(48, (int)($_GET['limit'] ?? 24)));
$page = max(1, (int)($_GET['page'] ?? 1));
$keyword = trim((string)($_GET['keyword'] ?? $_GET['q'] ?? ''));
$category = trim((string)($_GET['category'] ?? ''));
$typeid = trim((string)($_GET['typeid'] ?? ''));
$sort = trim((string)($_GET['sort'] ?? 'newest'));



function proxy_image(string $url): string {
    $url = trim($url);
    if ($url === '') return '';
    if (strpos($url, '/wd-img/') === 0) {
        $path = $url;
    } elseif (preg_match('#^https?://si\.geilicdn\.com/(.+)$#i', $url, $m)) {
        $path = '/wd-img/si.geilicdn.com/' . $m[1];
    } else {
        return $url;
    }
    // Bust Cloudflare edge 404s cached before the /wd-img/ proxy existed.
    if (strpos($path, '_wp=1') === false) {
        $path .= (strpos($path, '?') === false ? '?' : '&') . '_wp=1';
    }
    return $path;
}


function http_get_json(string $url, string $apiKey): ?array {
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_CONNECTTIMEOUT => 8,
        CURLOPT_TIMEOUT => 20,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $apiKey,
            'X-API-Key: ' . $apiKey,
            'Accept: application/json',
            'User-Agent: UsFansSpreadsheet/2.1',
        ],
    ]);
    $body = curl_exec($ch);
    $code = (int)curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    if ($body === false || $code < 200 || $code >= 300) return null;
    $json = json_decode($body, true);
    return is_array($json) ? $json : null;
}

$query = [
    'page' => (string)$page,
    'per_page' => (string)$limit,
    'sort' => $sort !== '' ? $sort : 'newest',
    'api_key' => $apiKey,
];
if ($keyword !== '') $query['q'] = $keyword;
if ($category !== '') $query['category'] = $category;
if ($typeid !== '') $query['typeid'] = $typeid;

$data = http_get_json($searchApi . '?' . http_build_query($query), $apiKey);
$items = [];
$total = 0;

if ($data) {
    $total = (int)($data['found'] ?? $data['total'] ?? $data['count'] ?? 0);
    if (isset($data['hits']) && is_array($data['hits'])) {
        foreach ($data['hits'] as $hit) {
            if (!is_array($hit)) continue;
            $title = trim((string)($hit['title'] ?? ''));
            if ($title === '') continue;
            $path = (string)($hit['url'] ?? '');
            $target = $path !== ''
                ? ($path[0] === '/' ? $w2cBase . $path : $path)
                : $spreadsheet . '?' . http_build_query([
                    'utm_source' => 'usfansspreadsheet',
                    'utm_medium' => 'aggregator',
                    'utm_campaign' => 'usfans',
                ]);
            $price = (string)($hit['price'] ?? '');
            $items[] = [
                'title' => $title,
                'image' => proxy_image((string)($hit['image'] ?? '')),
                'category' => (string)($hit['category'] ?? 'Finds'),
                'brand' => (string)($hit['brand'] ?? ''),
                'price' => $price,
                'currency' => 'CNY',
                'target' => $target,
                'href' => $target,
            ];
            if (count($items) >= $limit) break;
        }
    }
}

echo json_encode([
    'ok' => true,
    'page' => $page,
    'limit' => $limit,
    'total' => $total,
    'query' => $keyword,
    'category' => $category,
    'typeid' => $typeid,
    'items' => $items,
    'products' => $items,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
