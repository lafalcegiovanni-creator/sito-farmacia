<?php
/*
 * Modulo "Scrivici" del sito Farmacia La Falce Giovanni.
 * Riceve i dati da index.html e li invia per email alla farmacia.
 *
 * PRIMA DI PUBBLICARE: nel pannello Aruba crea la casella indicata in $MITTENTE
 * (serve come mittente tecnico: i server Aruba accettano solo mittenti del dominio).
 */

$DESTINATARIO = 'farmacialafalcegiovanni@gmail.com';
$MITTENTE     = 'noreply@farmacialafalcegiovanni.it';
$PAGINA       = 'index.html';
$ATTESA_SECONDI = 60; // tempo minimo tra due invii dallo stesso browser

date_default_timezone_set('Europe/Rome');
session_start();

function torna($ok, $dettaglio = '') {
    global $PAGINA;
    http_response_code($ok ? 200 : 400);
    header('Content-Type: text/html; charset=UTF-8');
    $titolo = $ok ? 'Messaggio inviato' : 'Messaggio non inviato';
    $testo  = $ok
        ? 'Grazie, abbiamo ricevuto il tuo messaggio. Ti risponderemo via email il prima possibile, negli orari di apertura.'
        : 'Il messaggio non è stato inviato. ' . ($dettaglio !== '' ? $dettaglio . ' ' : '') . 'Torna indietro e riprova, oppure chiamaci al 095 7500061.';
    echo '<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
       . '<meta name="robots" content="noindex"><title>' . $titolo . ' | Farmacia La Falce Giovanni</title>'
       . '<style>body{margin:0;background:#F3F6F4;color:#22292B;font-family:"Segoe UI",Roboto,Arial,sans-serif;font-size:1.15rem;line-height:1.6}'
       . 'main{max-width:640px;margin:0 auto;padding:64px 20px}h1{font-size:2rem;line-height:1.15;margin:0 0 16px;color:' . ($ok ? '#00653D' : '#A3271B') . '}'
       . 'a{display:inline-block;margin-top:24px;background:#00804E;color:#fff;font-weight:700;text-decoration:none;padding:14px 22px;border-radius:10px}</style>'
       . '</head><body><main><h1>' . $titolo . '</h1><p>' . htmlspecialchars($testo, ENT_QUOTES, 'UTF-8') . '</p>'
       . '<a href="' . $PAGINA . '#contatti">Torna al sito</a></main></body></html>';
    exit;
}
function pulisci($testo, $max) {
    $testo = trim((string)$testo);
    $testo = str_replace("\0", '', $testo);
    return mb_substr($testo, 0, $max, 'UTF-8');
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: ' . $PAGINA); exit; }
if (!function_exists('mb_substr')) { function mb_substr($t, $i, $l) { return substr($t, $i, $l); } }

// Trappola antispam: un utente vero lascia vuoto il campo "sito"
if (!empty($_POST['sito'])) torna(true);

// Limite di frequenza
if (isset($_SESSION['ultimo_invio']) && time() - $_SESSION['ultimo_invio'] < $ATTESA_SECONDI) torna(false, 'Hai appena inviato un messaggio: attendi un minuto prima di inviarne un altro.');

$nome      = pulisci($_POST['nome'] ?? '', 100);
$email     = pulisci($_POST['email'] ?? '', 150);
$messaggio = pulisci($_POST['messaggio'] ?? '', 2000);
$consenso  = isset($_POST['consenso']);

// Nessun a capo nei campi che finiscono nelle intestazioni
$nome  = preg_replace('/[\r\n]+/', ' ', $nome);
$email = preg_replace('/[\r\n]+/', '', $email);

if ($nome === '' || $messaggio === '' || !$consenso || !filter_var($email, FILTER_VALIDATE_EMAIL)) torna(false, 'Mancano alcuni dati: nome, email valida, messaggio e conferma dell\'informativa sulla privacy.');

$quando  = date('d/m/Y H:i');
$oggetto = 'Messaggio dal sito da ' . $nome;
$corpo   = "Nuovo messaggio dal modulo \"Scrivici\" del sito.\n\n"
         . "Nome: $nome\n"
         . "Email: $email\n"
         . "Data e ora: $quando\n"
         . "Informativa privacy: dichiarata letta il $quando\n\n"
         . "Messaggio:\n$messaggio\n\n"
         . "Per rispondere usa semplicemente \"Rispondi\".\n";

$intestazioni = 'From: "Sito Farmacia La Falce" <' . $MITTENTE . ">\r\n"
              . 'Reply-To: ' . $email . "\r\n"
              . "MIME-Version: 1.0\r\n"
              . "Content-Type: text/plain; charset=UTF-8\r\n"
              . "Content-Transfer-Encoding: 8bit\r\n";

$inviato = mail(
    $DESTINATARIO,
    '=?UTF-8?B?' . base64_encode($oggetto) . '?=',
    $corpo,
    $intestazioni,
    '-f' . $MITTENTE
);

if ($inviato) $_SESSION['ultimo_invio'] = time();
torna($inviato, $inviato ? '' : 'Si è verificato un problema tecnico.');
