<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if (!isset($_GET['url']) || !$_GET['url']) {
    http_response_code(400);
    echo 'Missing url';
    exit;
}

$url = $_GET['url'];

if (!preg_match('#^https?://#i', $url)) {
    http_response_code(400);
    echo 'Invalid url';
    exit;
}

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_SSL_VERIFYHOST => false,
    CURLOPT_USERAGENT      => 'BROKEN_LORD_PROXY/1.0',
    CURLOPT_TIMEOUT        => 20,
]);

$response = curl_exec($ch);
$info     = curl_getinfo($ch);
$error    = curl_error($ch);
curl_close($ch);

if ($response === false) {
    http_response_code(500);
    echo 'Error fetching: ' . $error;
    exit;
}

if (!empty($info['content_type'])) {
    header('Content-Type: ' . $info['content_type']);
} else {
    header('Content-Type: text/plain; charset=UTF-8');
}

echo $response;
