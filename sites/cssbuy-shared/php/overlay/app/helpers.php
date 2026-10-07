<?php

function config(string $key, $default = null)
{
    static $boot;
    if ($boot === null) {
        $boot = require BASE_PATH . '/bootstrap/app.php';
    }
    if ($key === 'domains') {
        return $boot['domains'] ?? $default;
    }
    if (strpos($key, 'domains.') === 0) {
        $host = substr($key, strlen('domains.'));
        return $boot['domains'][$host] ?? $default;
    }
    $parts = explode('.', $key);
    $value = $boot;
    foreach ($parts as $part) {
        if (!is_array($value) || !array_key_exists($part, $value)) {
            return $default;
        }
        $value = $value[$part];
    }
    return $value;
}

function view(string $name, array $data = []): string
{
    extract($data, EXTR_SKIP);
    $path = BASE_PATH . '/resources/views/' . str_replace('.', '/', $name) . '.php';
    if (!is_file($path)) {
        http_response_code(500);
        return 'View not found: ' . htmlspecialchars($name);
    }
    ob_start();
    include $path;
    return ob_get_clean();
}

function __t(string $key, array $replace = []): string
{
    static $strings = [];
    $lang = $GLOBALS['locale'] ?? 'en';
    if (!isset($strings[$lang])) {
        $file = BASE_PATH . '/resources/lang/' . $lang . '.json';
        $strings[$lang] = is_file($file)
            ? json_decode(file_get_contents($file), true)
            : [];
    }
    $text = $strings[$lang][$key] ?? $key;
    foreach ($replace as $k => $v) {
        $text = str_replace(':' . $k, (string) $v, $text);
    }
    return $text;
}

function cache_remember(string $key, int $ttl, callable $callback)
{
    $dir = BASE_PATH . '/storage/cache';
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
    $file = $dir . '/' . md5($key) . '.cache';
    if (is_file($file) && (time() - filemtime($file)) < $ttl) {
        $payload = json_decode(file_get_contents($file), true);
        if (is_array($payload)) {
            return $payload;
        }
    }
    $value = $callback();
    file_put_contents($file, json_encode($value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    return $value;
}

function current_host(): string
{
    $host = $_SERVER['HTTP_HOST'] ?? 'localhost';
    return preg_replace('/:\d+$/', '', strtolower($host));
}

function canonical_url(string $path = '/'): string
{
    $host = current_host();
    $scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    return $scheme . '://' . $host . $path;
}

function outbound_url(?string $url): string
{
    $url = (string) $url;
    if ($url === '' || preg_match('#(fashionrepsspreadsheet|litbuy|allchinabuy|allchina-buy)#i', $url)) {
        return 'https://www.cssbuy.com/';
    }
    if (stripos($url, 'cssbuy.com') === false) {
        return 'https://www.cssbuy.com/';
    }
    return $url;
}

function e(?string $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

function categories_for_locale(string $lang, string $fullSite): array
{
    static $all;
    if ($all === null) {
        $all = require BASE_PATH . '/config/categories.php';
    }
    $base = rtrim($fullSite, '/');
    $out = [];
    foreach ($all as $cat) {
        $label = $cat['labels'][$lang] ?? $cat['labels']['en'] ?? $cat['slug'];
        $out[] = [
            'slug' => $cat['slug'],
            'emoji' => $cat['emoji'],
            'label' => $label,
            'url' => $base . '/category/' . $cat['slug'] . '/',
        ];
    }
    return $out;
}

function guide_page_slugs(): array
{
    return array_keys(require BASE_PATH . '/config/guide_pages.php');
}

function nav_guide_slugs(): array
{
    $meta = require BASE_PATH . '/config/guide_pages.php';
    $out = [];
    foreach ($meta as $slug => $cfg) {
        if (!empty($cfg['nav'])) {
            $out[] = $slug;
        }
    }

    return $out;
}
