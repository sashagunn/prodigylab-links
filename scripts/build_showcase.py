#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает публичную галерею примеров из SHOWCASE.json на пяти языках.

КАК ДОБАВИТЬ СЛЕДУЮЩИЙ ПРИМЕР
=============================
1. Демо уже лежит в preview/<slug>/ и открывается.
2. Снять обложку с живого демо (ширина 800, высота 500) и положить в
   showcase/covers/<slug>.jpg. Рисованных заглушек не ставить: на карточке
   должно быть то, что человек увидит, нажав «Попробовать».
3. Дописать запись в SHOWCASE.json. publication_status нового персонального
   демо — "draft": в галерее оно не появится, пока владелец не скажет.
4. `npm run showcase` — он же проверит каталог и откажется собирать, если
   id повторяется, нет обложки, нет демо или потерян перевод.
5. Главная и фильтры подхватят запись сами. Вторых списков нет.

Запуск: npm run showcase (входит в npm run all)
"""
import json
import os
import sys
import html as H

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_home import CSS, PHONE_SVG, PHONE_HREF, PHONE_TEXT, DIAG, PIXEL, ORIGIN, \
    LANGNAMES, PRIVACY, PRIVACY_TAG, SERVICE_HEAD, service_links
from home_content import L
from showcase_content import S, HOME, NICHE, SOLUTION

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, 'SHOWCASE.json')
OUT = {'en': 'showcase/index.html', 'ru': 'ru/showcase/index.html',
       'es': 'es/showcase/index.html', 'pt': 'pt/showcase/index.html',
       'de': 'de/showcase/index.html'}
PAGE_PATH = {'en': '/showcase/', 'ru': '/ru/showcase/', 'es': '/es/showcase/',
             'pt': '/pt/showcase/', 'de': '/de/showcase/'}
# Сколько карточек показывать сразу. Остальные — по кнопке: каталог будет
# расти, а страница не должна тянуть два десятка обложек на телефоне.
CHUNK = 9
ОБЯЗАТЕЛЬНЫЕ = ('id', 'slug', 'title', 'niche', 'solution_type', 'short_description',
                'demo_url', 'cover', 'project_type', 'language', 'featured',
                'sort_order', 'publication_status')
СТАТУСЫ = ('draft', 'review', 'published', 'retired')
ТИПЫ = ('concept', 'client_project')
ЯЗЫКИ = [c for c, _ in LANGNAMES]
e = H.escape


# ---------------------------------------------------------------- каталог
def загрузить() -> list[dict]:
    """Прочитать каталог и проверить его. Кривую запись лучше поймать здесь."""
    данные = json.load(open(CATALOG, encoding='utf-8'))
    items = данные['items']
    беды = []
    видели_id, видели_slug = set(), set()
    for i, it in enumerate(items):
        где = f"запись #{i + 1} ({it.get('slug') or it.get('id') or '?'})"
        нет = [к for к in ОБЯЗАТЕЛЬНЫЕ if к not in it]
        if нет:
            беды.append(f"{где}: нет полей {', '.join(нет)}")
            continue
        if it['id'] in видели_id:
            беды.append(f"{где}: id {it['id']} уже занят")
        if it['slug'] in видели_slug:
            беды.append(f"{где}: slug {it['slug']} уже занят")
        видели_id.add(it['id'])
        видели_slug.add(it['slug'])
        if it['publication_status'] not in СТАТУСЫ:
            беды.append(f"{где}: publication_status «{it['publication_status']}» не из {СТАТУСЫ}")
        if it['project_type'] not in ТИПЫ:
            беды.append(f"{где}: project_type «{it['project_type']}» не из {ТИПЫ}")
        for поле in ('title', 'short_description', 'cover_alt'):
            значение = it.get(поле)
            if поле == 'cover_alt' and значение is None:
                беды.append(f"{где}: нет cover_alt — картинка без подписи не пройдёт проверку")
                continue
            пропуски = [c for c in ЯЗЫКИ if not (значение or {}).get(c)]
            if пропуски:
                беды.append(f"{где}: {поле} без перевода на {', '.join(пропуски)}")
        # Ссылки проверяем по файлам, а не на глаз: битая карточка в галерее
        # хуже отсутствующей.
        демо = os.path.join(ROOT, it['demo_url'].strip('/'), 'index.html')
        if not os.path.exists(демо):
            беды.append(f"{где}: демо {it['demo_url']} не найдено ({демо})")
        обложка = os.path.join(ROOT, it['cover'].lstrip('/'))
        if not os.path.exists(обложка):
            беды.append(f"{где}: обложки {it['cover']} нет")
        # Истёкшее демо в галерее показывать нельзя.
        if os.path.exists(демо) and it['publication_status'] == 'published':
            разметка = open(демо, encoding='utf-8', errors='replace').read(4000)
            if 'name="pf-expires" content=""' not in разметка and 'pf-expires' in разметка:
                беды.append(f"{где}: у демо выставлен срок (pf-expires) — "
                            f"публиковать ссылку, которая погаснет, нельзя")
        if it['project_type'] == 'client_project':
            беды.append(f"{где}: client_project ставится только вручную после "
                        f"подтверждённого внедрения и разрешения показывать")
    if беды:
        print('Каталог не собран:')
        for б in беды:
            print('  ✗', б)
        sys.exit(1)
    return sorted(items, key=lambda x: (x['sort_order'], x['slug']))


def опубликованные(items) -> list[dict]:
    return [i for i in items if i['publication_status'] == 'published']


# ---------------------------------------------------------------- разметка
def ссылка_заявки(it: dict, code: str) -> str:
    """Существующий канал обращения, с меткой выбранного примера.

    Новой формы не заводим: /diagnostic уже читает utm-метки из адреса и
    кладёт их в заявку. utm_content — идентификатор примера.
    """
    return (f"{DIAG}{L[code]['scan_lang']}&amp;utm_source=showcase&amp;utm_medium=site"
            f"&amp;utm_campaign=preview_factory&amp;utm_content={e(it['slug'])}")


def карточка(it: dict, code: str, *, компактная: bool = False) -> str:
    t = S[code]
    название = it['title'][code]
    демо = it['demo_url']
    ниша = NICHE.get(it['niche'], {}).get(code, it['niche'])
    решение = SOLUTION.get(it['solution_type'], {}).get(code, it['solution_type'])
    метка = t['concept'] if it['project_type'] == 'concept' else t['client']
    пояснение = t['concept_note'] if it['project_type'] == 'concept' else t['client_note']
    aria = t['demo_aria'].format(title=название)
    низ = '' if компактная else (
        f'<p class="sc-note"><span class="sc-badge">{e(метка)}</span>{e(пояснение)}</p>'
        f'<div class="sc-acts">'
        f'<a class="btn" href="{демо}" target="_blank" rel="noopener" '
        f'aria-label="{e(aria)}">{e(t["demo"])}</a>'
        f'<a class="sc-ask" href="{ссылка_заявки(it, code)}" data-diag '
        f'data-example="{e(it["slug"])}">{e(t["similar"])} &rarr;</a>'
        f'</div>')
    если_компактная = (
        f'<p class="sc-note"><span class="sc-badge">{e(метка)}</span></p>'
        if компактная else '')
    return (
        f'<article class="sc-card" data-niche="{e(it["niche"])}" '
        f'data-solution="{e(it["solution_type"])}">'
        f'<a class="sc-shot" href="{демо}" target="_blank" rel="noopener" tabindex="-1" '
        f'aria-hidden="true">'
        f'<img src="{it["cover"]}" alt="{e(it["cover_alt"][code])}" loading="lazy" '
        f'decoding="async" width="800" height="500"></a>'
        f'<div class="sc-body">'
        f'<span class="sc-tags"><span class="mono">{e(ниша)}</span>'
        f'<span class="mono">{e(решение)}</span></span>'
        f'<h3><a href="{демо}" target="_blank" rel="noopener" aria-label="{e(aria)}">'
        f'{e(название)}<i aria-hidden="true">&#8599;</i></a></h3>'
        f'<p>{e(it["short_description"][code])}</p>'
        f'{если_компактная}{низ}'
        f'</div></article>')


def фильтры(items, code: str) -> str:
    """Фильтры только по существующим значениям.

    Группа не выводится, если значение одно (фильтровать нечего) или если
    она делит каталог ровно так же, как уже выведенная: две одинаковые
    полосы кнопок — это не выбор, а шум.
    """
    t = S[code]
    группы = (('niche', NICHE, t['filter_niche']), ('solution_type', SOLUTION, t['filter_solution']))
    разбиения, куски = [], []
    for поле, словарь, подпись in группы:
        значения = sorted({i[поле] for i in items})
        if len(значения) < 2:
            continue
        разбиение = frozenset(frozenset(i['slug'] for i in items if i[поле] == з) for з in значения)
        if разбиение in разбиения:
            continue
        разбиения.append(разбиение)
        кнопки = "".join(
            f'<button type="button" data-f="{поле}" data-v="{e(з)}" aria-pressed="false">'
            f'{e(словарь.get(з, {}).get(code, з))}</button>' for з in значения)
        куски.append(
            f'<div class="sc-fgroup" role="group" aria-label="{e(подпись)}">'
            f'<span class="mono">{e(подпись)}</span>'
            f'<button type="button" data-f="{поле}" data-v="" aria-pressed="true">'
            f'{e(t["filter_all"])}</button>{кнопки}</div>')
    return (f'<div class="sc-filters" id="sc-filters" hidden>{"".join(куски)}</div>'
            if куски else '')


# ------------------------------------------------------ блок на главной
def блок_для_главной(code: str) -> str:
    """Компактный блок с лучшими примерами. Импортируется build_home.py.

    Если опубликованного нет ни одного — блока нет вовсе: пустой раздел с
    обещаниями хуже отсутствующего.
    """
    items = опубликованные(загрузить())
    избранные = [i for i in items if i.get('featured')] or items
    избранные = избранные[:6]
    if not избранные:
        return ''
    h = HOME[code]
    t = S[code]
    сколько = (t['count_one'] if len(items) == 1 else t['count_many'].format(n=len(items)))
    карточки = "".join(карточка(i, code, компактная=True) for i in избранные)
    хвост = f'<p class="sc-soon">{e(t["soon"])}</p>' if len(items) < 3 else ''
    return f"""
<section class="sc-home" id="work">
 <div class="wrap">
  <span class="mono">{e(h['eyebrow'])}</span>
  <h2>{e(h['h2'])}</h2>
  <p class="sc-lead">{e(h['lead'])} <span class="sc-count">{e(сколько)}</span></p>
  <div class="sc-grid">{карточки}</div>
  {хвост}
  <p class="sc-all"><a class="btn" href="{PAGE_PATH[code]}">{e(h['all'])} &rarr;</a></p>
 </div>
</section>"""


# ---------------------------------------------------------------- страница
EXTRA_CSS = """
.sc-filters{display:flex;flex-wrap:wrap;gap:22px;margin:0 0 30px}
.sc-filters[hidden]{display:none!important}
.sc-fgroup{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.sc-fgroup .mono{color:var(--ink2);margin-right:4px}
.sc-fgroup button{font:inherit;font-size:14px;line-height:1;padding:9px 14px;cursor:pointer;
background:transparent;color:var(--ink2);border:1px solid var(--line);border-radius:999px;
transition:border-color .15s,color .15s,background .15s}
.sc-fgroup button:hover{border-color:var(--accent);color:var(--accent)}
.sc-fgroup button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.sc-fgroup button:focus-visible,.sc-card a:focus-visible,.sc-more:focus-visible{
outline:2px solid var(--accent);outline-offset:3px}
.sc-grid{display:grid;gap:26px;grid-template-columns:1fr}
@media(min-width:720px){.sc-grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1040px){.sc-grid{grid-template-columns:repeat(3,1fr)}}
.sc-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);
border-radius:4px;overflow:hidden}
.sc-card[hidden]{display:none!important}
.sc-shot{display:block;background:var(--paper2);line-height:0;border-bottom:1px solid var(--line)}
.sc-shot img{width:100%;height:auto;aspect-ratio:8/5;object-fit:cover}
.sc-body{padding:20px 20px 22px;display:flex;flex-direction:column;gap:10px;flex:1}
.sc-tags{display:flex;flex-wrap:wrap;gap:10px}
.sc-tags .mono{color:var(--ink2)}
.sc-tags .mono + .mono::before{content:"·";margin-right:10px;color:var(--line)}
.sc-card h3{margin:0;font-size:21px;line-height:1.25;font-weight:600;letter-spacing:-.01em}
.sc-card h3 a{color:var(--ink);text-decoration:none}
.sc-card h3 a:hover{color:var(--accent)}
.sc-card h3 i{font-style:normal;margin-left:6px;color:var(--ink3);font-size:15px}
.sc-card p{margin:0;font-size:15px;line-height:1.55;color:var(--ink2)}
.sc-note{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;font-size:13px!important;
color:var(--ink2)!important;margin-top:auto!important;padding-top:4px}
.sc-badge{display:inline-block;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10px;
letter-spacing:.14em;text-transform:uppercase;padding:4px 8px;border:1px solid var(--line);
border-radius:3px;color:var(--ink2);white-space:nowrap}
.sc-acts{display:flex;flex-wrap:wrap;align-items:center;gap:14px;padding-top:6px}
.sc-ask{font-size:14px;color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}
.sc-ask:hover{border-bottom-color:var(--accent)}
.sc-empty{margin:0;padding:40px 0;color:var(--ink2)}
.sc-reset{font:inherit;font-size:15px;margin-left:10px;padding:0;cursor:pointer;background:none;
border:0;color:var(--accent);border-bottom:1px solid var(--accent)}
.sc-reset:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.sc-empty[hidden]{display:none!important}
.sc-more{display:inline-block;margin-top:30px;font:inherit;font-size:15px;padding:13px 26px;
cursor:pointer;background:transparent;color:var(--ink);border:1px solid var(--line);border-radius:3px}
.sc-more:hover{border-color:var(--accent);color:var(--accent)}
.sc-more[hidden]{display:none!important}
.sc-head{padding:74px 0 34px}
.sc-head h1{font-size:clamp(34px,6vw,58px);line-height:1.05;letter-spacing:-.03em;margin:14px 0 0}
.sc-head .sc-lead{max-width:640px;font-size:18px;color:var(--ink2);margin:18px 0 0}
.sc-count{color:var(--ink2)}
.sc-home{padding:72px 0;border-top:1px solid var(--line);background:var(--paper2)}
.sc-home h2{font-size:clamp(26px,4vw,40px);line-height:1.1;letter-spacing:-.025em;margin:12px 0 0}
.sc-home .sc-lead{max-width:600px;color:var(--ink2);margin:14px 0 30px}
.sc-home .sc-card{background:var(--paper)}
.sc-soon{margin:24px 0 0;font-size:14px;color:var(--ink2)}
.sc-all{margin:30px 0 0}
"""

JS = """
(function(){
 var корень=document.getElementById('sc-list'); if(!корень) return;
 var карточки=[].slice.call(корень.querySelectorAll('.sc-card'));
 var пусто=document.getElementById('sc-empty');
 var ещё=document.getElementById('sc-more');
 var полоса=document.getElementById('sc-filters');
 var ШАГ=%d, показано=ШАГ, выбор={};
 if(полоса) полоса.hidden=false;
 function подходит(к){
  for(var поле in выбор){ if(выбор[поле] && к.getAttribute('data-'+поле)!==выбор[поле]) return false; }
  return true;
 }
 function показать(){
  var видимых=0, всего=0;
  карточки.forEach(function(к){
   if(!подходит(к)){ к.hidden=true; return; }
   всего++;
   var надо=всего<=показано;
   к.hidden=!надо;
   if(надо) видимых++;
  });
  if(пусто) пусто.hidden=всего>0;
  if(ещё) ещё.hidden=всего<=показано;
 }
 if(полоса){
  полоса.addEventListener('click',function(ev){
   var б=ev.target.closest('button'); if(!б) return;
   var поле=б.getAttribute('data-f'), значение=б.getAttribute('data-v');
   выбор[поле==='solution_type'?'solution':'niche']=значение;
   [].forEach.call(полоса.querySelectorAll('button[data-f="'+поле+'"]'),function(д){
    д.setAttribute('aria-pressed', д===б?'true':'false');
   });
   показано=ШАГ; показать();
  });
 }
 if(ещё) ещё.addEventListener('click',function(){ показано+=ШАГ; показать(); });
 var сброс=document.getElementById('sc-reset');
 if(сброс) сброс.addEventListener('click',function(){
  выбор={}; показано=ШАГ;
  if(полоса) [].forEach.call(полоса.querySelectorAll('button'),function(б){
   б.setAttribute('aria-pressed', б.getAttribute('data-v')===''?'true':'false');
  });
  показать();
  var первая=корень.querySelector('.sc-card:not([hidden]) h3 a'); if(первая) первая.focus();
 });
 показать();
})();
"""


def страница(code: str, items) -> str:
    t = S[code]
    d = L[code]
    публичные = опубликованные(items)
    url = ORIGIN + PAGE_PATH[code]
    diag = DIAG + d['scan_lang']
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{c}" href="{ORIGIN}{PAGE_PATH[c]}">' for c in ЯЗЫКИ
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{ORIGIN}/showcase/">'
    langs = "".join(
        f'<a href="{PAGE_PATH[c]}"{" aria-current=\"page\"" if c == code else ""}>{n}</a>'
        for c, n in LANGNAMES)
    # Пункты меню главной — якоря: со страницы галереи они должны вести на
    # главную нужного языка, а не в никуда.
    def домой(h):
        return (d['home'].rstrip('/') + '/' + h) if h.startswith('#') else h
    navmid = "".join(f'<a href="{домой(h)}">{e(x)}</a>' for h, x in d['nav'])
    mobls = "".join(f'<a class="ml" href="{домой(h)}">{e(x)}</a>' for h, x in d['nav'])
    сколько = (t['count_one'] if len(публичные) == 1
               else t['count_many'].format(n=len(публичные)))
    карточки = "".join(карточка(i, code) for i in публичные)
    хлебные = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Prodigy LAB",
             "item": ORIGIN + d['home']},
            {"@type": "ListItem", "position": 2, "name": t['h1'], "item": url},
        ]}
    список = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": t['h1'], "numberOfItems": len(публичные),
        "itemListElement": [
            {"@type": "ListItem", "position": n, "name": i['title'][code],
             "url": ORIGIN + i['demo_url']}
            for n, i in enumerate(публичные, 1)],
    }
    return f"""<!DOCTYPE html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="Prodigy LAB">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:locale" content="{d['locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA_CSS}</style>
<script type="application/ld+json">
{json.dumps(хлебные, ensure_ascii=False, indent=1)}
</script>
<script type="application/ld+json">
{json.dumps(список, ensure_ascii=False, indent=1)}
</script>
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','{PIXEL}');fbq('track','PageView');
</script>
<noscript><img alt="" height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={PIXEL}&ev=PageView&noscript=1"/></noscript>
<script src="/assets/ai-referrals.js" defer></script>
</head>
<body>

<nav>
 <div class="wrap nav-in">
  <a class="brand" href="{d['home']}"><b>PRODIGY</b><span>LAB</span></a>
  <div class="nav-mid">{navmid}<a href="{PAGE_PATH[code]}" aria-current="page">{e(t['nav'])}</a></div>
  <div class="nav-right">
   <div class="langs">{langs}</div>
   <a class="icon" href="{PHONE_HREF}" aria-label="{e(d['call'])} {PHONE_TEXT}" title="{PHONE_TEXT}">{PHONE_SVG}</a>
   <button id="burger" class="icon" aria-label="Menu" aria-expanded="false" onclick="tg(this)">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 7h18M3 12h18M3 17h18"/></svg>
   </button>
   <a class="btn nav-cta" href="{diag}" data-diag>{e(d['cta1'])}</a>
  </div>
 </div>
 <div id="mob"><div class="wrap">{mobls}
  <a class="ml" href="{PAGE_PATH[code]}">{e(t['nav'])}</a>
  <a class="btn" href="{diag}" data-diag>{e(d['cta1'])}</a>
  <a class="ml" href="{PHONE_HREF}">{e(d['call'])} {PHONE_TEXT}</a>
  <div class="mlangs">{langs}</div>
 </div></div>
</nav>

<main>
<section class="sc-head">
 <div class="wrap">
  <span class="mono">PREVIEW FACTORY</span>
  <h1>{e(t['h1'])}</h1>
  <p class="sc-lead">{e(t['lead'])} <span class="sc-count">{e(сколько)}</span></p>
 </div>
</section>

<section style="padding:0 0 80px">
 <div class="wrap">
  {фильтры(публичные, code)}
  <div class="sc-grid" id="sc-list" aria-live="polite">{карточки}</div>
  <p class="sc-empty" id="sc-empty" hidden>{e(t['empty'])}<button type="button" class="sc-reset" id="sc-reset">{e(t['reset'])}</button></p>
  <button type="button" class="sc-more" id="sc-more" hidden>{e(t['more'])}</button>
 </div>
</section>
</main>

<footer>
 <div class="wrap">
  <a class="brand" href="{d['home']}"><b>PRODIGY</b><span>LAB</span></a>
  <div class="flinks">
   <a href="{d['home']}">{e(t['footer_back'])}</a>
   <a href="{PAGE_PATH[code]}">{e(t['nav'])}</a>
   <a href="{PHONE_HREF}">{PHONE_TEXT}</a>
   <a href="{PRIVACY[code]}">{e(d['foot_priv'])}{PRIVACY_TAG[code]}</a>
  </div>
  <div style="border-top:1px solid var(--line);padding-top:18px">
   <span class="mono" style="display:block;margin-bottom:10px">{e(SERVICE_HEAD[code])}</span>
   <div class="flinks" style="margin:0">{service_links(code)}</div>
  </div>
  <p class="fmeta">© 2026 Prodigy LAB · Platonaire LLC · California, USA<br>{e(d['foot_legal'])}</p>
 </div>
</footer>

<script>
function tg(b){{var m=document.getElementById('mob');var o=b.getAttribute('aria-expanded')==='true';
b.setAttribute('aria-expanded',String(!o));m.classList.toggle('open',!o);}}
{JS % CHUNK}
</script>
</body>
</html>"""


if __name__ == '__main__':
    items = загрузить()
    публичные = опубликованные(items)
    for code, rel in OUT.items():
        p = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        html = страница(code, items)
        open(p, 'w', encoding='utf-8').write(html)
        print(f"  ✓ {rel:26} {len(html) // 1024} KB  ({code})")
    скрытые = len(items) - len(публичные)
    print(f"Галерея собрана: показывается {len(публичные)}, "
          f"в каталоге ещё {скрытые} неопубликованных")
