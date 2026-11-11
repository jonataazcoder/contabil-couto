import json, os, re, subprocess, sys, shutil, hashlib, urllib.parse
from html import escape
B = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(B, 'site'); OUT = os.path.join(B, 'dist')
SITE = (sys.argv[1] if len(sys.argv) > 1 else 'https://contabil-couto.vercel.app').rstrip('/')
WA_NUM = '5511919524301'
WA = 'https://wa.me/%s?text=%s' % (WA_NUM, urllib.parse.quote('Olá! Vim pelo site e gostaria de falar com a Contábil Couto.'))
WA_T = 'https://wa.me/%s?text=%s' % (WA_NUM, urllib.parse.quote('Olá! Tenho empresa e quero trocar de contador. Podemos conversar?'))

FAQ = [
 ("Quanto custa a contabilidade da minha empresa?", "Depende do regime, do número de funcionários e do volume de notas. Mandando essas três informações pelo WhatsApp, a gente devolve um orçamento fechado, sem surpresa no mês seguinte."),
 ("Quanto tempo leva para abrir uma empresa em Bragança Paulista?", "Com a documentação em mãos, o CNPJ costuma sair em poucos dias úteis. Inscrição municipal e alvará variam conforme a atividade e a análise da Prefeitura — a gente acompanha cada etapa e te avisa."),
 ("Sou MEI e meu faturamento passou de R$ 81 mil. E agora?", "Se o excesso for de até 20% (R$ 97.200), você migra para o Simples Nacional no ano seguinte e paga a diferença sobre o excedente. Acima disso, o desenquadramento é retroativo a janeiro. Quanto antes conversarmos, menor o custo."),
 ("Como fica a minha empresa com a Reforma Tributária?", "Em 2026 as notas já trazem IBS e CBS em caráter de teste. Em 2027 PIS e Cofins acabam e a CBS passa a valer. Revisamos o seu regime, o emissor de notas e os preços para a transição não pegar ninguém desprevenido."),
 ("Vocês atendem empresas de fora de Bragança?", "Sim. Atendemos presencialmente no Centro de Bragança Paulista e a distância empresas de Atibaia, Piracaia, Socorro, Extrema e de toda a região — documentos e guias circulam pelo digital."),
 ("Fazem imposto de renda de pessoa física?", "Fazemos. Declaração anual, carnê-leão, ganho de capital na venda de imóveis e regularização de malha fina. Com a isenção para quem ganha até R$ 5 mil por mês, vale revisar o que muda para você na declaração de 2027."),
]

def build_faq():
    out = []
    for q, a in FAQ:
        out.append('      <details class="rv"><summary>%s</summary><p>%s</p></details>' % (escape(q), escape(a)))
    return '\n'.join(out)

def jsonld():
    biz = {
        "@type": ["AccountingService", "LocalBusiness"], "@id": SITE + "/#empresa",
        "name": "Contábil Couto", "alternateName": "Contábil Couto – Contabilidade & Assessoria",
        "description": "Escritório de contabilidade e assessoria em Bragança Paulista: abertura e encerramento de empresas, departamento pessoal, escrita fiscal, contabilidade, imposto de renda e ITR.",
        "url": SITE + "/", "logo": SITE + "/img/logo.png", "image": SITE + "/img/og.jpg",
        "telephone": "+55-11-4032-8745", "email": "contabilcouto@hotmail.com",
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": "+55-11-4032-8745", "contactType": "customer service", "areaServed": "BR", "availableLanguage": "Portuguese"},
            {"@type": "ContactPoint", "telephone": "+55-11-2473-6852", "contactType": "customer service", "availableLanguage": "Portuguese"},
            {"@type": "ContactPoint", "telephone": "+55-11-91952-4301", "contactType": "customer service", "contactOption": "WhatsApp", "availableLanguage": "Portuguese"}],
        "address": {"@type": "PostalAddress", "streetAddress": "R. Cel. João Leme, 559 – Centro", "addressLocality": "Bragança Paulista", "addressRegion": "SP", "postalCode": "12900-161", "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": -22.9551223, "longitude": -46.5413089},
        "hasMap": "https://www.google.com/maps/place/?q=place_id:ChIJV017rCvKzpQRtTr34cjIm50",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
        "areaServed": [{"@type": "City", "name": n} for n in ["Bragança Paulista", "Atibaia", "Piracaia", "Socorro", "Extrema"]],
        "priceRange": "$$", "currenciesAccepted": "BRL",
        "sameAs": ["https://www.instagram.com/contabil_couto/"],
        "knowsAbout": ["MEI", "Simples Nacional", "Lucro Presumido", "Lucro Real", "Reforma Tributária", "IBS", "CBS", "NFS-e", "eSocial", "FGTS Digital", "Imposto de Renda", "ITR"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Serviços contábeis", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in
            ["Abertura e encerramento de empresas", "Departamento pessoal", "Escrita fiscal", "Contabilidade", "Imposto de renda", "ITR"]]},
    }
    g = [biz,
         {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Contábil Couto", "inLanguage": "pt-BR", "publisher": {"@id": SITE + "/#empresa"}},
         {"@type": "WebPage", "@id": SITE + "/#pagina", "url": SITE + "/", "name": "Contábil Couto | Contabilidade em Bragança Paulista", "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": SITE + "/#empresa"}, "inLanguage": "pt-BR", "primaryImageOfPage": SITE + "/img/og.jpg"},
         {"@type": "FAQPage", "@id": SITE + "/#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

def run(cmd, **kw):
    subprocess.run(cmd, shell=True, check=True, cwd=B, **kw)

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + '/css'); os.makedirs(OUT + '/js'); os.makedirs(OUT + '/img')
shutil.copytree(SRC + '/fonts', OUT + '/fonts')
run('npx --yes csso-cli site/css/src.css -o dist/css/site.css')
run('npx --yes terser site/js/src.js -c -m -o dist/js/site.js')
V = hashlib.sha1(open(OUT + '/css/site.css', 'rb').read() + open(OUT + '/js/site.js', 'rb').read()).hexdigest()[:8]

emb = open(B + '/emblem.min.svg').read()
inner = re.sub(r'^<svg[^>]*>|</svg>$', '', emb.strip())
html = open(SRC + '/index.src.html').read()
for k, v in {'{{SITE}}': SITE, '{{V}}': V, '{{JSONLD}}': jsonld(), '{{EMBLEM}}': inner,
             '{{WA}}': escape(WA), '{{WA_TROCA}}': escape(WA_T), '{{FAQ_HTML}}': build_faq()}.items():
    html = html.replace(k, v)
assert '{{' not in html, re.findall(r'\{\{\w+\}\}', html)
html = re.sub(r'\n\s*\n', '\n', html)
open(OUT + '/index.html', 'w').write(html)

# icons
gold_svg = emb.replace('currentColor', '#C9A86A')
icon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0F0E0C"/>'
        '<svg x="12" y="6" width="40" height="52" viewBox="0 0 768 1024">%s</svg></svg>') % inner.replace('currentColor', '#C9A86A')
open(OUT + '/icon.svg', 'w').write(icon)
open(B + '/logo_gold.svg', 'w').write(gold_svg)
run('node render.js "%s"' % SITE)

open(OUT + '/site.webmanifest', 'w').write(json.dumps({"name": "Contábil Couto", "short_name": "Couto", "start_url": "/", "display": "standalone", "background_color": "#0F0E0C", "theme_color": "#0F0E0C", "lang": "pt-BR",
    "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False))
open(OUT + '/robots.txt', 'w').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)
open(OUT + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n<url><loc>%s/</loc><lastmod>2026-11-11</lastmod><changefreq>monthly</changefreq><priority>1.0</priority><image:image><image:loc>%s/img/og.jpg</image:loc></image:image></url>\n</urlset>\n' % (SITE, SITE))
open(OUT + '/llms.txt', 'w').write("""# Contábil Couto

> Escritório de contabilidade e assessoria no Centro de Bragança Paulista (SP). Atende MEI, Simples Nacional, Lucro Presumido e Lucro Real.

## Serviços
- Abertura e encerramento de empresas
- Departamento pessoal (folha, eSocial, FGTS Digital)
- Escrita fiscal (incluindo IBS/CBS da Reforma Tributária e NFS-e)
- Contabilidade (balancete, DRE, balanço)
- Imposto de renda pessoa física
- ITR

## Contato
- Endereço: R. Cel. João Leme, 559 – Centro, Bragança Paulista – SP, 12900-161
- Horário: segunda a sexta, 8h às 18h
- Telefones: (11) 4032-8745 · (11) 2473-6852
- WhatsApp: (11) 91952-4301
- E-mail: contabilcouto@hotmail.com
- Instagram: https://www.instagram.com/contabil_couto/

## Páginas
- [Início](%s/)
""" % SITE)
open(OUT + '/404.html', 'w').write('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Página não encontrada | Contábil Couto</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0F0E0C;color:#EEE7D9;font:16px/1.6 system-ui,sans-serif;text-align:center;padding:24px}h1{font:italic 600 44px/1.1 Georgia,serif;color:#C9A86A;margin:0 0 12px}a{color:#0F0E0C;background:#C9A86A;padding:12px 22px;border-radius:99px;text-decoration:none;font-weight:700;display:inline-block;margin-top:20px}</style><div><h1>Página não encontrada</h1><p>O endereço que você procurou não existe ou mudou de lugar.</p><a href="/">Voltar para o início</a></div></html>')
LONG = 'public, max-age=31536000, immutable'
open(OUT + '/vercel.json', 'w').write(json.dumps({
    "cleanUrls": True, "trailingSlash": False,
    "headers": [
        {"source": "/fonts/(.*)", "headers": [{"key": "Cache-Control", "value": LONG}]},
        {"source": "/(css|js)/(.*)", "headers": [{"key": "Cache-Control", "value": LONG}]},
        {"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000"}]},
        {"source": "/(.*)", "headers": [
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
            {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
            {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"}]}
    ]}, indent=1))
tot = 0
for r, _, fs in os.walk(OUT):
    for f in fs:
        tot += os.path.getsize(os.path.join(r, f))
print('built', SITE, 'v', V, 'total', tot)
from PIL import Image
im = Image.open(OUT + '/fav32.png'); im.save(OUT + '/favicon.ico', sizes=[(32, 32)]); os.remove(OUT + '/fav32.png')
