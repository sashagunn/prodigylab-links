#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix-prodigybot-meta.py — правит то, на что указал Bing Webmaster Tools по /prodigybot/:
длинный meta description и полное отсутствие structured markup.

FAQPage собирается ИЗ РЕАЛЬНОГО текста страницы (блок «Коротко о главном» и его
переводы), а не пишется отдельно. Это принципиально: разметка, не совпадающая
с содержимым страницы, — нарушение правил и поисковиков, и AI-систем.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = 'https://prodigylab.studio'
FACTS = json.load(open(os.path.join(ROOT, 'BUSINESS_FACTS.json'), encoding='utf-8'))

MARK_S = '<!-- PRODIGYBOT-SCHEMA:START (генерируется scripts/fix-prodigybot-meta.py — руками не править) -->'
MARK_E = '<!-- PRODIGYBOT-SCHEMA:END -->'

# Якорь блока FAQ на каждом языке + человекочитаемые title/description в лимитах.
LANGS = {
    'prodigybot/index.html': dict(
        lang='ru', home=f'{ORIGIN}/', url=f'{ORIGIN}/prodigybot/', anchor='Коротко о главном',
        title='ProdigyBot — AI-продавец в мессенджерах | Prodigy LAB',
        desc='AI-продавец отвечает за 4 секунды 24/7 в Instagram, WhatsApp, Telegram и на сайте, ведёт к заявке и зовёт человека. От $600 + $290/мес.',
        name='ProdigyBot — AI-продавец', crumb='ProdigyBot'),
    'en/prodigybot/index.html': dict(
        lang='en', home=f'{ORIGIN}/en/', url=f'{ORIGIN}/en/prodigybot/', anchor='The short answers',
        title='ProdigyBot — AI Sales Assistant | Prodigy LAB',
        desc='An AI salesperson replying in 4 seconds, 24/7, on Instagram, WhatsApp, Telegram and your site. Qualifies, follows up, hands over to a human. From $600 + $290/mo.',
        name='ProdigyBot — AI Sales Assistant', crumb='ProdigyBot'),
    'es/prodigybot/index.html': dict(
        lang='es', home=f'{ORIGIN}/es/', url=f'{ORIGIN}/es/prodigybot/', anchor='En resumen',
        title='ProdigyBot — vendedor con IA | Prodigy LAB',
        desc='Vendedor con IA que responde en 4 segundos, 24/7, en Instagram, WhatsApp, Telegram y tu sitio. Califica y pasa a una persona. Desde $600 + $290/mes.',
        name='ProdigyBot — vendedor con IA', crumb='ProdigyBot'),
    'pt/prodigybot/index.html': dict(
        lang='pt', home=f'{ORIGIN}/pt/', url=f'{ORIGIN}/pt/prodigybot/', anchor='Em resumo',
        title='ProdigyBot — vendedor com IA | Prodigy LAB',
        desc='Vendedor com IA que responde em 4 segundos, 24/7, no Instagram, WhatsApp, Telegram e no site. Qualifica e passa para uma pessoa. A partir de $600 + $290/mês.',
        name='ProdigyBot — vendedor com IA', crumb='ProdigyBot'),
    'de/prodigybot/index.html': dict(
        lang='de', home=f'{ORIGIN}/de/', url=f'{ORIGIN}/de/prodigybot/', anchor='Kurz gefasst',
        title='ProdigyBot — KI-Verkäufer für Messenger | Prodigy LAB',
        desc='KI-Verkäufer: antwortet in 4 Sekunden, rund um die Uhr, auf Instagram, WhatsApp, Telegram und der Website. Qualifiziert und übergibt an Menschen. Ab $600 + $290/Mon.',
        name='ProdigyBot — KI-Verkäufer', crumb='ProdigyBot'),
}

STRIP = re.compile(r'<[^>]+>')


def clean(s):
    return re.sub(r'\s+', ' ', STRIP.sub('', s)).strip()


def extract_faq(html, anchor):
    """Тянем пары вопрос-ответ из реального FAQ-блока страницы."""
    i = html.find(anchor)
    if i == -1:
        # запасной путь: последние h3+p на странице — это и есть FAQ
        pairs = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', html, re.S)[-6:]
    else:
        pairs = re.findall(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', html[i:i + 9000], re.S)
    out = []
    for q, a in pairs:
        q, a = clean(q), clean(a)
        if q and a and q.endswith(('?', '？')):
            out.append((q, a))
    return out


def blocks(cfg, faq):
    """Product — потому что у ProdigyBot есть тарифы с ценами прямо на странице."""
    tiers = [('Start', 600, 290), ('Sales', 1200, 590), ('Business', 2200, 990)]
    product = {
        '@context': 'https://schema.org', '@type': 'Product',
        'name': cfg['name'], 'url': cfg['url'],
        'description': cfg['desc'],
        'category': 'AI sales assistant',
        'brand': {'@type': 'Brand', 'name': 'Prodigy LAB'},
        'offers': {
            '@type': 'AggregateOffer', 'priceCurrency': 'USD',
            'lowPrice': '600', 'highPrice': '2200', 'offerCount': len(tiers),
            'url': cfg['url'],
            'offers': [{
                '@type': 'Offer', 'name': f'ProdigyBot {n}', 'url': cfg['url'],
                'price': str(setup), 'priceCurrency': 'USD',
                'availability': 'https://schema.org/InStock',
                'description': f'Setup ${setup} plus ${mo} per month. Minimum term 3 months.',
            } for n, setup, mo in tiers],
        },
        'provider': {'@type': 'Organization', 'name': 'Prodigy LAB',
                     'legalName': FACTS['identity']['legalName'], 'url': f'{ORIGIN}/'},
    }
    crumbs = {
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Prodigy LAB', 'item': cfg['home']},
            {'@type': 'ListItem', 'position': 2, 'name': cfg['crumb'], 'item': cfg['url']}]}
    out = [product, crumbs]
    if faq:
        out.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q,
             'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
    return out


def replace_meta(html, name_attr, value):
    """Меняем content у meta вне зависимости от порядка атрибутов."""
    pat = re.compile(r'<meta[^>]*\b(?:name|property)="' + re.escape(name_attr) + r'"[^>]*>', re.I)
    m = pat.search(html)
    if not m:
        return html, False
    tag = m.group(0)
    new = re.sub(r'content="[^"]*"', lambda _: 'content="' + value.replace('\\', '\\\\') + '"', tag, count=1)
    if 'content=' not in tag:
        return html, False
    return html[:m.start()] + new + html[m.end():], True


def run():
    for rel, cfg in LANGS.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print(f'  пропуск (нет файла): {rel}')
            continue
        html = open(p, encoding='utf-8').read()

        faq = extract_faq(html, cfg['anchor'])

        html = re.sub(r'<title>.*?</title>', '<title>' + cfg['title'] + '</title>', html, count=1, flags=re.S)
        for attr in ('description', 'og:description'):
            html, _ = replace_meta(html, attr, cfg['desc'])
        html, _ = replace_meta(html, 'og:title', cfg['title'])

        block = MARK_S + '\n' + '\n'.join(
            '<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=1) + '\n</script>'
            for b in blocks(cfg, faq)) + '\n' + MARK_E
        rx = re.compile(re.escape(MARK_S) + r'[\s\S]*?' + re.escape(MARK_E))
        html = rx.sub(block, html) if rx.search(html) else html.replace('</head>', block + '\n</head>', 1)

        open(p, 'w', encoding='utf-8').write(html)
        print(f'  ✓ {rel:30} title={len(cfg["title"]):3} desc={len(cfg["desc"]):3} FAQ-пар={len(faq)}')


if __name__ == '__main__':
    run()
