#!/usr/bin/env python3
"""
Costruisce la sezione "Per la tua salute è utile sapere…" del sito Farmacia La Falce Giovanni.

Ogni articolo è un file JSON in articoli/ con questi campi:
  slug       nome della pagina, senza spazi (es. "holter-pressorio-come-funziona")
  titolo     titolo dell'articolo
  data       data di pubblicazione, AAAA-MM-GG
  categoria  es. "Servizi della farmacia", "Prevenzione", "Stagione", "Iniziative"
  sommario   una o due frasi per l'elenco e per Google (max ~155 caratteri)
  corpo      testo in HTML semplice (<p>, <h2>, <ul>, <ol>, <strong>, <a>)

Uso:  python3 costruisci_blog.py <cartella del sito>
Genera: blog/<slug>.html per ogni articolo, blog/index.html, il riquadro
"ultimi articoli" in index.html (tra i commenti ULTIMI-ARTICOLI) e sitemap.xml.
Gli articoli con data futura non vengono pubblicati.
"""
import html, json, os, sys, datetime, glob

SITO = 'https://www.farmacialafalcegiovanni.it'
MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio',
        'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
NOTA = ("Le informazioni di questo articolo hanno scopo divulgativo e non sostituiscono "
        "il parere del medico o del farmacista. Per dubbi sulla tua salute rivolgiti al tuo medico.")


def data_it(iso):
    d = datetime.date.fromisoformat(iso)
    return f'{d.day} {MESI[d.month - 1]} {d.year}'


def esc(t):
    return html.escape(t, quote=True)


def carica(cartella_articoli, oggi):
    articoli = []
    for f in glob.glob(os.path.join(cartella_articoli, '*.json')):
        a = json.load(open(f, encoding='utf-8'))
        for campo in ('slug', 'titolo', 'data', 'categoria', 'sommario', 'corpo'):
            if not a.get(campo):
                raise SystemExit(f'{f}: manca il campo "{campo}"')
        if a['data'] <= oggi:
            articoli.append(a)
    articoli.sort(key=lambda a: (a['data'], a['slug']), reverse=True)
    return articoli


TESTA = '''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descrizione}">
<meta name="theme-color" content="#00804E">
<link rel="canonical" href="{canonico}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<meta property="og:type" content="{og_tipo}">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="Farmacia La Falce Giovanni">
<meta property="og:title" content="{titolo_og}">
<meta property="og:description" content="{descrizione}">
<meta property="og:url" content="{canonico}">
<meta property="og:image" content="{sito}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="../fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="blog.css">
{extra}
</head>
<body>
<a class="salta" href="#contenuto">Vai al contenuto</a>
<header class="testata">
  <div class="wrap">
    <a class="marchio" href="../index.html">
      <svg viewBox="0 0 30 30" aria-hidden="true"><path fill="#00804E" d="M10 0h10v10h10v10H20v10H10V20H0V10h10z"/></svg>
      <span>Farmacia La Falce Giovanni</span>
    </a>
    <nav aria-label="Menu principale">
      <a href="../index.html">Il sito</a>
      <a href="index.html">Per la tua salute</a>
      <a class="btn" href="tel:+390957500061">Chiama</a>
    </nav>
  </div>
</header>
<main id="contenuto">
'''

PIEDE = '''</main>
<footer class="piede">
  <div class="wrap">
    <strong>Farmacia La Falce Giovanni</strong>
    <p>Via Fasano 112, 95030 Gravina di Catania (CT). Tel. <a href="tel:+390957500061">095 7500061</a>, WhatsApp <a href="https://wa.me/390957500061">+39 095 7500061</a>, email <a href="mailto:farmacialafalcegiovanni@gmail.com">farmacialafalcegiovanni@gmail.com</a></p>
    <p>Titolare dott. Giovanni La Falce, iscritto all'Albo dei Farmacisti di Catania n. 2172. P.IVA 03243920877</p>
    <p class="link-legali"><a href="../privacy.html">Informativa sulla privacy</a> <a href="../cookie.html">Informativa sui cookie</a></p>
  </div>
</footer>
</body>
</html>
'''


def pagina_articolo(a, precedente, successivo):
    canonico = f'{SITO}/blog/{a["slug"]}.html'
    dati = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": a['titolo'], "description": a['sommario'],
        "datePublished": a['data'], "dateModified": a.get('aggiornato', a['data']),
        "inLanguage": "it-IT", "mainEntityOfPage": canonico,
        "image": f'{SITO}/og-image.jpg',
        "author": {"@type": "Organization", "name": "Farmacia La Falce Giovanni", "url": SITO + '/'},
        "publisher": {"@type": "Organization", "name": "Farmacia La Falce Giovanni",
                      "logo": {"@type": "ImageObject", "url": f'{SITO}/apple-touch-icon.png'}}
    }
    extra = '<script type="application/ld+json">\n' + json.dumps(dati, ensure_ascii=False, indent=2) + '\n</script>'
    out = TESTA.format(titolo=esc(a['titolo'] + ' | Farmacia La Falce Giovanni'), titolo_og=esc(a['titolo']),
                       descrizione=esc(a['sommario']), canonico=canonico, og_tipo='article', sito=SITO, extra=extra)
    out += f'''<article class="articolo wrap-stretto">
  <p class="briciole"><a href="index.html">Per la tua salute è utile sapere…</a> <span aria-hidden="true">/</span> {esc(a['categoria'])}</p>
  <h1>{esc(a['titolo'])}</h1>
  <p class="firma">A cura della Farmacia La Falce Giovanni. <time datetime="{a['data']}">{data_it(a['data'])}</time></p>
  <p class="sommario">{esc(a['sommario'])}</p>
  <div class="corpo">
{a['corpo']}
  </div>
  <aside class="contatti-articolo" aria-label="Contatti">
    <p><strong>Vuoi prenotare un esame, chiedere un farmaco o inviarci la ricetta per farci preparare i farmaci?</strong></p>
    <p>Chiamaci al <a href="tel:+390957500061">095 7500061</a>, scrivici su <a href="https://wa.me/390957500061">WhatsApp</a> o per email a <a href="mailto:farmacialafalcegiovanni@gmail.com">farmacialafalcegiovanni@gmail.com</a>, oppure passa in farmacia, in Via Fasano 112 a Gravina di Catania.</p>
  </aside>
  <p class="nota">{NOTA}</p>
'''
    nav = []
    if successivo:
        nav.append(f'<a href="{successivo["slug"]}.html">Articolo successivo: {esc(successivo["titolo"])}</a>')
    if precedente:
        nav.append(f'<a href="{precedente["slug"]}.html">Articolo precedente: {esc(precedente["titolo"])}</a>')
    if nav:
        out += '  <nav class="altri" aria-label="Altri articoli">' + ''.join(nav) + '</nav>\n'
    out += '</article>\n' + PIEDE
    return out


def scheda(a, prefisso, titolo_tag='h3'):
    return (f'<li class="scheda-articolo"><span class="categoria">{esc(a["categoria"])}</span>'
            f'<{titolo_tag}><a href="{prefisso}{a["slug"]}.html">{esc(a["titolo"])}</a></{titolo_tag}>'
            f'<time datetime="{a["data"]}">{data_it(a["data"])}</time>'
            f'<p>{esc(a["sommario"])}</p></li>')


def pagina_elenco(articoli):
    out = TESTA.format(titolo='Per la tua salute è utile sapere… | Farmacia La Falce Giovanni', titolo_og='Per la tua salute è utile sapere…',
                       descrizione='Ogni giorno un articolo della Farmacia La Falce Giovanni di Gravina di Catania: prevenzione, consigli pratici e servizi della farmacia.',
                       canonico=f'{SITO}/blog/', og_tipo='website', sito=SITO, extra='')
    out += '''<section class="wrap elenco">
  <h1>Per la tua salute è utile sapere…</h1>
  <p class="intro">Ogni giorno un nuovo articolo della farmacia: prevenzione, consigli pratici e i nostri servizi spiegati da vicino.</p>
'''
    if articoli:
        out += '  <ul class="schede-articoli">\n' + '\n'.join('    ' + scheda(a, '', 'h2') for a in articoli) + '\n  </ul>\n'
    else:
        out += '  <p>I primi articoli arrivano a breve.</p>\n'
    out += '</section>\n' + PIEDE
    return out


def aggiorna_home(sito, articoli):
    p = os.path.join(sito, 'index.html')
    s = open(p, encoding='utf-8').read()
    inizio, fine = '<!-- ULTIMI-ARTICOLI-INIZIO -->', '<!-- ULTIMI-ARTICOLI-FINE -->'
    i, j = s.index(inizio) + len(inizio), s.index(fine)
    blocco = '\n      <ul class="schede-articoli">\n' + '\n'.join('        ' + scheda(a, 'blog/') for a in articoli[:3]) + '\n      </ul>\n      '
    open(p, 'w', encoding='utf-8').write(s[:i] + blocco + s[j:])


def sitemap(sito, articoli, oggi):
    righe = [f'  <url><loc>{SITO}/</loc><lastmod>{oggi}</lastmod></url>',
             f'  <url><loc>{SITO}/blog/</loc><lastmod>{articoli[0]["data"] if articoli else oggi}</lastmod></url>']
    righe += [f'  <url><loc>{SITO}/blog/{a["slug"]}.html</loc><lastmod>{a.get("aggiornato", a["data"])}</lastmod></url>' for a in articoli]
    open(os.path.join(sito, 'sitemap.xml'), 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(righe) + '\n</urlset>\n')


def main():
    if len(sys.argv) < 2:
        raise SystemExit('Uso: python3 costruisci_blog.py <cartella del sito>')
    sito = sys.argv[1]
    qui = os.path.dirname(os.path.abspath(__file__))
    oggi = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1))).date().isoformat()
    articoli = carica(os.path.join(qui, 'articoli'), oggi)
    blog = os.path.join(sito, 'blog')
    os.makedirs(blog, exist_ok=True)
    for k, a in enumerate(articoli):
        successivo = articoli[k - 1] if k > 0 else None
        precedente = articoli[k + 1] if k + 1 < len(articoli) else None
        open(os.path.join(blog, a['slug'] + '.html'), 'w', encoding='utf-8').write(pagina_articolo(a, precedente, successivo))
    open(os.path.join(blog, 'index.html'), 'w', encoding='utf-8').write(pagina_elenco(articoli))
    aggiorna_home(sito, articoli)
    sitemap(sito, articoli, oggi)
    print(f'Pubblicati {len(articoli)} articoli.')


if __name__ == '__main__':
    main()
