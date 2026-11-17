# Sito Farmacia La Falce Giovanni – istruzioni per Claude

Leggi questo file all'inizio di ogni sessione. Rispondi al titolare in italiano, con linguaggio semplice e non tecnico.

## La farmacia
- Farmacia La Falce Giovanni, Via Fasano 112, 95030 Gravina di Catania (CT). Aperta dal 1996.
- Titolare: dott. Giovanni La Falce (Albo Farmacisti Catania n. 2172). P.IVA 03243920877.
- Tel. e WhatsApp 095 7500061 (+39 095 7500061). Email farmacialafalcegiovanni@gmail.com. PEC 14831@pec.federfarma.it.
- Sito: www.farmacialafalcegiovanni.it (dominio su Aruba). Facebook: https://www.facebook.com/FarmaciaLafalceGiovanni/
- Orari: lun-ven 8:30-13:00 e 16:00-20:00; sabato 8:30-13:00; domenica chiuso.

## Servizi e prezzi (usare sempre questi)
- ECG a riposo in telemedicina: 25 €, sempre a pagamento (mai in convenzione SSN).
- Holter cardiaco (da 24 ore a 7 giorni): 70 €. Holter pressorio 24 ore: 35 €. Con ricetta dematerializzata del medico ed esenzione per reddito o patologia sono gratuiti.
- Densitometria ossea a ultrasuoni al tallone (apparecchio Beetle): 15 €.
- Scelta e cambio del medico di famiglia: 5 € a persona (portare tessera sanitaria, documento, cellulare).
- Prenotazione CUP di visite ed esami: 3 € (portare la ricetta dematerializzata).
- Pagamento ticket, avvisi pagoPA (anche bollette luce/gas/acqua con QR pagoPA) e bollo auto. NON citare commissioni.
- Consegna a domicilio 2 € a Gravina di Catania, Catania, Mascalucia, San Giovanni La Punta, Sant'Agata li Battiati, Misterbianco, Tremestieri Etneo, Belpasso. Richiesta la mattina → consegna il pomeriggio; richiesta il pomeriggio → la mattina seguente.
- Preparazioni galeniche (di solito entro 2 giorni lavorativi), angolo veterinaria, misurazione pressione, peso/altezza/IMC.

## Tono dei testi
- Professionale ma comprensibile per tutti; contenuti di servizio nell'interesse del cliente.
- Leggermente tecnico, con terminologia da farmacia e valori di riferimento numerici quando utili, restando chiaro.
- Ricordare sempre che si può contattare la farmacia anche per email (oltre a telefono e WhatsApp) per prenotare esami, chiedere farmaci e inviare ricette. Non scoraggiare l'invio delle ricette.
- Il catalogo WhatsApp NON va citato finché il titolare non dice che è attivo.

## Struttura del repository
- `sito/` – il sito completo, pronto da caricare su Aruba (contenuto della cartella nella radice del sito): index.html, privacy.html, cookie.html, contatti.php, .htaccess, robots.txt, sitemap.xml, favicon.svg, apple-touch-icon.png, og-image.jpg, fonts/, foto/, blog/.
- `blog/` – sorgenti del blog "Per la tua salute è utile sapere…":
  - `costruisci_blog.py` genera le pagine: `python3 blog/costruisci_blog.py sito`
  - `articoli/AAAA-MM-GG-titolo.json` un file per articolo (campi: slug, titolo, data, categoria, sommario, corpo in HTML semplice). Gli articoli con data futura non vengono pubblicati.
  - `blog.css` stile del blog (copiato anche in `sito/blog/`).
- `verifica/farmacia-la-falce-pagina-unica.html` – tutto il sito in un solo file, solo per vederlo in anteprima. NON va pubblicato. Se cambia `sito/index.html`, va rigenerato (caratteri, foto e icone incorporati in base64, senza preload né srcset).

## Modulo contatti
- `contatti.php` invia a farmacialafalcegiovanni@gmail.com, mittente tecnico noreply@farmacialafalcegiovanni.it (casella da creare su Aruba), "Rispondi a" = email del cliente.

## Blog
- Un articolo al giorno, firmato "Farmacia La Falce Giovanni" (non il titolare), pubblicato senza approvazione preventiva; il titolare li legge e chiede modifiche. Non proporgli calendari di argomenti.
- Lunghezza di riferimento: l'articolo sull'Holter pressorio (equilibrato).
- Argomenti: prevenzione, consigli di salute, servizi della farmacia, iniziative legate a date o giornate particolari.
- Pubblicazione automatica ancora da attivare. Proposta: GitHub Pages da questo repository su un sottodominio (es. consigli.farmacialafalcegiovanni.it) con record CNAME su Aruba. In quel caso i link relativi del blog verso il sito principale (../index.html, ../fonts/, ../favicon.svg, ../privacy.html…) vanno resi assoluti o copiati, e il riquadro "ultimi articoli" della home su Aruba diventa un rimando fisso al blog.

## Stato al 17/11/2026
- Il vecchio sito su Solo (soloist.ai) chiude il 30/11/2026.
- Da fare: attivare Hosting Linux Basic su Aruba e creare noreply@; caricare `sito/` (dal PC della farmacia o dal pannello Aruba: dal cloud la connessione FTP verso Aruba è bloccata); provare pagine e modulo (anche cartella Spam di Gmail); spostare il dominio prima del 30/11.
- Facoltativi ancora mancanti: link diretto alle recensioni Google, pagina turni Federfarma Catania, chiusure/ferie/festa patronale (CHIUSURE, APERTURE, FESTE_LOCALI nello script di index.html), coordinate per i dati strutturati.
- Revisione di privacy e cookie da parte di un consulente.
- Copie anche sul Google Drive della farmacia, cartella "Sito farmacia" (zip + pagina unica).
