#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pages.py — генератор статических страниц Prodigy LAB.

Зачем: шапка, подвал, пиксель, виджет чата и базовая разметка одинаковы на всех
страницах. Держать это копипастой в девяти файлах — гарантированный рассинхрон
фактов, а рассинхрон фактов ломает и людей, и AI-системы.

Контент страниц лежит в scripts/pages_content.py. Факты о компании берутся
из BUSINESS_FACTS.json — цены и дисклеймеры не дублируются в разметке страниц.

Запуск: npm run pages
"""
import json, os, re, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = json.load(open(os.path.join(ROOT, 'BUSINESS_FACTS.json'), encoding='utf-8'))
ORIGIN = 'https://prodigylab.studio'
PIXEL = '1713332936325081'

A_MUTED = 'class="text-sm font-medium text-text-muted hover:text-accent-green transition-colors"'
CARD = 'class="border border-border-subtle bg-white p-6 hover:border-accent-green transition-colors"'


def head(p):
    lang = p.get('lang', 'en')
    url = f"{ORIGIN}/{p['slug']}/"
    ld = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(b, ensure_ascii=False, indent=1)}\n</script>'
        for b in p.get('jsonld', []))
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(p['title'])}</title>
<meta name="description" content="{H.escape(p['description'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Prodigy LAB">
<meta property="og:title" content="{H.escape(p['title'])}">
<meta property="og:description" content="{H.escape(p['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{'ru_RU' if lang == 'ru' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/tw.css">
<link rel="stylesheet" href="/assets/site.css">
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','{PIXEL}');fbq('track','PageView');
</script>
<noscript><img alt="" height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={PIXEL}&ev=PageView&noscript=1"/></noscript>
{ld}
<script src="/assets/ai-referrals.js" defer></script>
</head>
<body class="bg-background">'''


def nav(lang):
    t = dict(sv='Услуги', pr='Цены', ab='О студии', cs='Кейсы', cta='Написать') if lang == 'ru' \
        else dict(sv='Services', pr='Pricing', ab='About', cs='Cases', cta='Talk to us')
    home = '/' if lang == 'ru' else '/en/'
    return f'''
<nav class="sticky top-0 w-full z-50 bg-white/80 backdrop-blur-xl border-b border-border-subtle" aria-label="{'Основная навигация' if lang=='ru' else 'Primary'}">
<div class="flex justify-between items-center max-w-[1200px] mx-auto px-8 h-20">
<a href="{home}" class="flex items-center gap-3" aria-label="Prodigy LAB — {'на главную' if lang=='ru' else 'home'}"><div class="text-xl font-bold tracking-tighter"><span class="text-accent-green">PRODIGY</span> <span class="font-light">LAB</span></div></a>
<div class="hidden md:flex gap-10 items-center">
<a {A_MUTED} href="/services/">{t['sv']}</a>
<a {A_MUTED} href="/about/">{t['ab']}</a>
<a {A_MUTED} href="/case-studies/">{t['cs']}</a>
<a {A_MUTED} href="/en/pricing/">{t['pr']}</a>
</div>
<a href="https://wa.me/18182690416" target="_blank" rel="noopener" class="bg-accent-green text-white px-6 py-3 text-xs font-bold uppercase tracking-widest hover:brightness-90 hover:scale-[1.02] active:scale-[0.98] transition-all">{t['cta']}</a>
</div>
</nav>
<main id="main">'''


def footer(lang):
    slogan = FACTS['identity']['slogan_ru'] if lang == 'ru' else FACTS['identity']['slogan_en']
    links = ([('/', 'Главная'), ('/services/', 'Услуги'), ('/about/', 'О студии'),
              ('/case-studies/', 'Кейсы'), ('/en/pricing/', 'Цены'),
              ('/prodigybot/', 'ProdigyBot'), ('/scan/', 'Бесплатная проверка'),
              ('/privacy/', 'Политика конфиденциальности')] if lang == 'ru' else
             [('/en/', 'Home'), ('/services/', 'Services'), ('/about/', 'About'),
              ('/case-studies/', 'Cases'), ('/en/pricing/', 'Pricing'),
              ('/prodigybot/', 'ProdigyBot'), ('/scan/', 'Free scan'),
              ('/en/privacy/', 'Privacy Policy')])
    ls = "".join(f'<a class="hover:text-accent-green transition-colors" href="{h}">{n}</a>' for h, n in links)
    return f'''</main>
<footer class="bg-white border-t border-border-subtle py-20">
<div class="max-w-[1200px] mx-auto px-8">
<div class="text-2xl font-bold tracking-tighter mb-4"><span class="text-accent-green">PRODIGY</span> <span class="font-light">LAB</span></div>
<p class="text-lg italic text-accent-green mb-8 max-w-sm">{slogan}</p>
<div class="flex flex-wrap gap-x-10 gap-y-3 text-[11px] font-mono uppercase tracking-widest text-text-muted mb-8">{ls}</div>
<div class="font-mono text-[11px] uppercase tracking-[0.3em] text-text-muted">© 2026 Prodigy LAB · {FACTS['identity']['legalName']} · California, USA</div>
</div>
</footer>
<script>
  (function (d, t) {{
    var BASE_URL = "https://chat.prodigylab.studio";
    var g = d.createElement(t), s = d.getElementsByTagName(t)[0];
    g.src = BASE_URL + "/packs/js/sdk.js"; g.defer = true; g.async = true;
    s.parentNode.insertBefore(g, s);
    g.onload = function () {{
      window.chatwootSettings = window.chatwootSettings || {{}}; window.chatwootSettings.locale = "{lang}";
      window.chatwootSDK.run({{ websiteToken: "J1xMPSabyx7EfRVPrmZEMLYB", baseUrl: BASE_URL }});
    }};
  }})(document, "script");
</script>
</body>
</html>'''


# ---------- строительные блоки контента ----------

def hero(eyebrow, h1, lead, ctas=(), note=''):
    b = [f'<section class="max-w-[1200px] mx-auto px-8 pt-20 pb-16">']
    b.append(f'<span class="font-mono text-[11px] tracking-[0.3em] text-accent-green font-semibold uppercase mb-6 block">{eyebrow}</span>')
    b.append(f'<h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-[1.05] mb-8 max-w-4xl">{h1}</h1>')
    b.append(f'<p class="text-lg md:text-xl text-text-muted leading-relaxed max-w-2xl mb-10">{lead}</p>')
    if ctas:
        b.append('<div class="flex flex-col sm:flex-row gap-4 mb-8">')
        for i, (href, label, ext) in enumerate(ctas):
            cls = ('bg-accent-green text-white' if i == 0 else 'bg-white border border-border-subtle text-on-surface hover:bg-surface')
            tgt = ' target="_blank" rel="noopener"' if ext else ''
            b.append(f'<a href="{href}"{tgt} class="{cls} px-10 py-5 font-bold text-sm tracking-widest uppercase text-center hover:brightness-95 active:scale-[0.98] transition-all">{label}</a>')
        b.append('</div>')
    if note:
        b.append(f'<p class="font-mono text-[11px] text-text-muted tracking-[0.2em] uppercase">{note}</p>')
    b.append('</section>')
    return "\n".join(b)


def qa(title, items, surface=False):
    """Answer-first блок: вопрос -> прямой ответ в первом абзаце -> детали."""
    wrap_o = '<section class="bg-surface border-y border-border-subtle py-section-gap"><div class="max-w-[1200px] mx-auto px-8">' if surface \
        else '<section class="max-w-[1200px] mx-auto px-8 py-section-gap">'
    wrap_c = '</div></section>' if surface else '</section>'
    b = [wrap_o, f'<h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-12 max-w-3xl">{title}</h2>']
    for q, direct, detail in items:
        b.append('<div class="border-b border-border-subtle py-8 max-w-3xl">')
        b.append(f'<h3 class="text-xl md:text-2xl font-bold mb-4">{q}</h3>')
        b.append(f'<p class="text-lg text-on-surface leading-relaxed mb-3"><strong>{direct}</strong></p>')
        if detail:
            b.append(f'<p class="text-text-muted leading-relaxed">{detail}</p>')
        b.append('</div>')
    b.append(wrap_c)
    return "\n".join(b)


def facts_table(title, rows, surface=False):
    wrap_o = '<section class="bg-surface border-y border-border-subtle py-section-gap"><div class="max-w-[1200px] mx-auto px-8">' if surface \
        else '<section class="max-w-[1200px] mx-auto px-8 py-section-gap">'
    wrap_c = '</div></section>' if surface else '</section>'
    tr = "".join(
        f'<tr class="border-b border-border-subtle"><th scope="row" class="text-left align-top py-4 pr-8 font-bold whitespace-nowrap">{k}</th>'
        f'<td class="py-4 text-text-muted">{v}</td></tr>' for k, v in rows)
    return (f'{wrap_o}<h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-10">{title}</h2>'
            f'<div class="overflow-x-auto"><table class="w-full max-w-3xl border-collapse"><tbody>{tr}</tbody></table></div>{wrap_c}')


def cols(title, items, lead='', surface=False, n=2):
    wrap_o = '<section class="bg-surface border-y border-border-subtle py-section-gap"><div class="max-w-[1200px] mx-auto px-8">' if surface \
        else '<section class="max-w-[1200px] mx-auto px-8 py-section-gap">'
    wrap_c = '</div></section>' if surface else '</section>'
    b = [wrap_o, f'<h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 max-w-3xl">{title}</h2>']
    if lead:
        b.append(f'<p class="text-lg text-text-muted mb-12 max-w-2xl">{lead}</p>')
    b.append(f'<div class="grid md:grid-cols-{n} gap-x-16 gap-y-8">')
    for h3, txt in items:
        b.append(f'<div><h3 class="text-lg font-bold mb-2">{h3}</h3><p class="text-text-muted leading-relaxed">{txt}</p></div>')
    b.append('</div>' + wrap_c)
    return "\n".join(b)


def steps(title, items, surface=False):
    wrap_o = '<section class="bg-surface border-y border-border-subtle py-section-gap"><div class="max-w-[1200px] mx-auto px-8">' if surface \
        else '<section class="max-w-[1200px] mx-auto px-8 py-section-gap">'
    wrap_c = '</div></section>' if surface else '</section>'
    b = [wrap_o, f'<h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-10">{title}</h2><ol class="grid md:grid-cols-3 gap-8">']
    for i, (h3, txt) in enumerate(items, 1):
        b.append(f'<li><div class="font-mono text-[11px] text-accent-green mb-3">{i:02d}</div>'
                 f'<h3 class="font-bold mb-2">{h3}</h3><p class="text-sm text-text-muted leading-relaxed">{txt}</p></li>')
    b.append('</ol>' + wrap_c)
    return "\n".join(b)


def cards(title, items, lead='', surface=True):
    wrap_o = '<section class="bg-surface border-y border-border-subtle py-section-gap"><div class="max-w-[1200px] mx-auto px-8">' if surface \
        else '<section class="max-w-[1200px] mx-auto px-8 py-section-gap">'
    wrap_c = '</div></section>' if surface else '</section>'
    b = [wrap_o, f'<h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-6">{title}</h2>']
    if lead:
        b.append(f'<p class="text-lg text-text-muted mb-12 max-w-2xl">{lead}</p>')
    b.append('<div class="grid md:grid-cols-3 gap-6">')
    for href, h3, txt in items:
        b.append(f'<a href="{href}" {CARD}><h3 class="font-bold mb-2">{h3}</h3><p class="text-sm text-text-muted leading-relaxed">{txt}</p></a>')
    b.append('</div>' + wrap_c)
    return "\n".join(b)


def disclaimer(lang='ru'):
    """Видимый блок-дисклеймер. Не в FAQ, не мелким шрифтом — отдельной секцией."""
    txt = FACTS['notProvided']['disclaimer_ru'] if lang == 'ru' else FACTS['notProvided']['disclaimer_en']
    ttl = 'Чего мы не делаем' if lang == 'ru' else 'What we do not do'
    return (f'<section class="max-w-[1200px] mx-auto px-8 py-16"><div class="border-l-4 border-accent-green bg-surface p-8 max-w-3xl">'
            f'<h2 class="text-xl font-bold mb-4">{ttl}</h2>'
            f'<p class="text-text-muted leading-relaxed">{txt}</p></div></section>')


def cta_band(title, text, href, label, ext=False):
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    return (f'<section class="max-w-[1200px] mx-auto px-8 py-section-gap"><div class="border border-border-subtle p-10 md:p-14 max-w-3xl">'
            f'<h2 class="text-2xl md:text-3xl font-bold mb-4">{title}</h2>'
            f'<p class="text-text-muted leading-relaxed mb-8">{text}</p>'
            f'<a href="{href}"{tgt} class="inline-block bg-accent-green text-white px-10 py-5 font-bold text-sm tracking-widest uppercase hover:brightness-90 active:scale-[0.98] transition-all">{label}</a>'
            f'</div></section>')


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', d + (' ' + x if x else ''))}}
        for q, d, x in items]}


def breadcrumb_ld(slug, name, lang='en'):
    home = f"{ORIGIN}/" if lang == 'ru' else f"{ORIGIN}/en/"
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Prodigy LAB", "item": home},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{ORIGIN}/{slug}/"}]}


def service_ld(slug, name, desc, price=None):
    d = {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
         "provider": {"@type": "Organization", "name": "Prodigy LAB", "legalName": FACTS['identity']['legalName'], "url": ORIGIN + "/"},
         "areaServed": {"@type": "Country", "name": "United States"}, "description": desc,
         "url": f"{ORIGIN}/{slug}/"}
    if price:
        d["offers"] = {"@type": "Offer", "price": str(price), "priceCurrency": "USD",
                       "url": f"{ORIGIN}/{slug}/", "availability": "https://schema.org/InStock"}
    return d


def write(p):
    body = "\n".join(p['sections'])
    out = head(p) + nav(p.get('lang', 'en')) + body + footer(p.get('lang', 'en'))
    d = os.path.join(ROOT, p['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    return len(out)


if __name__ == '__main__':
    import pages_content
    total = 0
    for p in pages_content.PAGES:
        n = write(p)
        total += 1
        print(f"  ✓ /{p['slug']}/  ({n // 1024} KB)  {p['title'][:52]}")
    print(f"Собрано страниц: {total}")
