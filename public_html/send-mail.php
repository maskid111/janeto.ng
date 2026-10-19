<?php
/**
 * JANETO.NG contact form handler (both the "Contact Us" section form and the envelope popup form).
 * Uses PHP's built-in mail(), so it needs a host where mail() is enabled (most cPanel/DirectAdmin plans).
 * Always answers with JSON: {"ok":true} or {"ok":false,"error":"..."}.
 */

// ---------------------------------------------------------------- settings
const MAIL_TO      = 'ovationsglam@gmail.com';   // where messages are delivered
const SITE_NAME    = 'JANETO.NG';
const RATE_LIMIT   = 5;                          // max messages ...
const RATE_WINDOW  = 600;                        // ... per IP per 10 minutes
// Sender address. It should be a mailbox on YOUR domain (e.g. create no-reply@yourdomain in
// DirectAdmin > E-mail Accounts) so Gmail doesn't reject it as spoofed. Leave '' to use no-reply@<current domain>.
const MAIL_FROM    = '';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function respond(int $status, array $body): void {
    http_response_code($status);
    echo json_encode($body);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(405, ['ok' => false, 'error' => 'Method not allowed.']);
}

// Only accept submissions from this site's own pages.
$host = preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? '');
foreach (['HTTP_ORIGIN', 'HTTP_REFERER'] as $h) {
    if (!empty($_SERVER[$h])) {
        $from = parse_url($_SERVER[$h], PHP_URL_HOST);
        if ($from && strcasecmp($from, $host) !== 0) {
            respond(403, ['ok' => false, 'error' => 'Forbidden.']);
        }
        break;
    }
}

// Honeypot: real visitors never see or fill this field.
if (!empty($_POST['website'])) {
    respond(200, ['ok' => true]);
}

// ---------------------------------------------------------------- input
function field(string $key, int $max): string {
    $v = isset($_POST[$key]) && is_string($_POST[$key]) ? trim($_POST[$key]) : '';
    $v = str_replace("\0", '', $v);
    return function_exists('mb_substr') ? mb_substr($v, 0, $max, 'UTF-8') : substr($v, 0, $max);
}
function one_line(string $v): string {
    return trim(preg_replace('/[\r\n\t]+/', ' ', $v));   // blocks header injection
}

$name    = one_line(field('name', 100));
$email   = one_line(field('email', 254));
$phone   = one_line(field('phone', 40));
$message = field('message', 5000);
$source  = field('form', 20) === 'popup' ? 'Contact Us popup' : 'Conect with me form';

$errors = [];
if ($name === '')                                   $errors['name']  = 'This field is required.';
if ($email === '')                                  $errors['email'] = 'This field is required.';
elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors['email'] = 'Please enter a valid email.';
if ($phone !== '' && !preg_match('/^[0-9+()\-.\s]{5,40}$/', $phone))
                                                    $errors['phone'] = 'Please enter a valid phone number.';
if ($errors) {
    respond(422, ['ok' => false, 'error' => 'Please correct the highlighted fields.', 'fields' => $errors]);
}

// ---------------------------------------------------------------- rate limit (per IP, file based)
$ip   = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$file = rtrim(sys_get_temp_dir(), '/\\') . '/janeto_mail_' . md5($ip . __FILE__);
$now  = time();
$hits = [];
if (is_readable($file)) {
    $hits = array_filter(array_map('intval', explode(',', (string) @file_get_contents($file))),
        static fn ($t) => $t > $now - RATE_WINDOW);
}
if (count($hits) >= RATE_LIMIT) {
    respond(429, ['ok' => false, 'error' => 'Too many messages. Please try again in a few minutes.']);
}

// ---------------------------------------------------------------- send
$domain   = preg_replace('/^www\./i', '', $host) ?: 'localhost';
$fromAddr = MAIL_FROM !== '' ? MAIL_FROM : 'no-reply@' . $domain;

$subject = '=?UTF-8?B?' . base64_encode('New message from ' . SITE_NAME . ' website – ' . $name) . '?=';
$body    = "You have a new message from the " . $source . " on " . SITE_NAME . ".\n\n"
         . "Name:    " . $name . "\n"
         . "Email:   " . $email . "\n"
         . ($phone !== '' ? "Phone:   " . $phone . "\n" : '')
         . "\nMessage:\n" . ($message !== '' ? $message : '(no message)') . "\n\n"
         . "--\nSent " . gmdate('Y-m-d H:i') . " UTC from IP " . $ip . "\n";

$headers = implode("\r\n", [
    'From: ' . SITE_NAME . ' Website <' . $fromAddr . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: PHP/' . PHP_VERSION,
]);

$sent = @mail(MAIL_TO, $subject, $body, $headers, '-f' . $fromAddr);
if (!$sent) {
    // some hosts reject the -f parameter; retry without it
    $sent = @mail(MAIL_TO, $subject, $body, $headers);
}
if (!$sent) {
    respond(500, ['ok' => false, 'error' => 'The message could not be sent right now.']);
}

$hits[] = $now;
@file_put_contents($file, implode(',', $hits), LOCK_EX);
respond(200, ['ok' => true]);
