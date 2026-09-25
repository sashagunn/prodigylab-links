#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает новую главную на пяти языках из scripts/home_content.py.

CSS встроен в страницу намеренно: главная не зависит от сборки Tailwind,
поэтому её нельзя сломать забытым `npm run css`. Запуск: npm run home
"""
import os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from home_content import L, PHONE_HREF, PHONE_TEXT, WA, SCAN, DIAG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = 'https://prodigylab.studio'
PIXEL = '1713332936325081'
OUT = {'en': 'index.html', 'ru': 'ru/index.html', 'es': 'es/index.html',
       'pt': 'pt/index.html', 'de': 'de/index.html'}
# Порядок в переключателе: английский первым, он теперь базовый
LANGNAMES = [('en', 'EN'), ('ru', 'RU'), ('es', 'ES'), ('pt', 'PT'), ('de', 'DE')]


import json as _json
_F = _json.load(open(os.path.join(ROOT, 'BUSINESS_FACTS.json'), encoding='utf-8'))
SERVICE_HEAD = {'en': 'Services', 'ru': 'Специализированные услуги — на английском',
                'es': 'Servicios especializados — en inglés',
                'pt': 'Serviços especializados — em inglês',
                'de': 'Spezialisierte Leistungen — auf Englisch'}


def service_links(code: str) -> str:
    # Страницы услуг пока существуют только на английском. Молча уводить с
    # локальной версии на чужой язык нельзя — помечаем (EN) явно (ТЗ §8, вариант B).
    tag = '' if code == 'en' else ' (EN)'
    return "".join(
        f'<a href="/{s["slug"]}/" hreflang="en" style="font-size:12.5px;color:var(--ink3)">'
        f'{H.escape(s["name_en"])}{tag}</a>' for s in _F['services'])

# Политика: английская на корне, русская переведена. ES/PT/DE пока ведут на
# английскую и подписаны — юридический текст не переводится машинно (ТЗ §10).
PRIVACY = {'en': '/privacy/', 'ru': '/ru/privacy/', 'es': '/privacy/',
           'pt': '/privacy/', 'de': '/privacy/'}
PRIVACY_TAG = {'en': '', 'ru': '', 'es': ' (English)', 'pt': ' (English)', 'de': ' (English)'}

PHONE_SVG = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
 'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
 '19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 '
 '1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.1 9.9a16 16 0 0 0 6 6l1.26-1.26a2 2 0 0 1 2.11-.45c.9.34 1.85.57 '
 '2.81.7A2 2 0 0 1 22 16.92z"/></svg>')

CSS = """
:root{--ink:#121212;--ink2:#5C5C5A;--ink3:#8A8A86;--paper:#FBFBF9;--paper2:#F3F2EE;
--line:#E2E1DC;--accent:#1C7E84;--accent2:#0F4A4E}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:Geist,system-ui,-apple-system,sans-serif;
font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:clip}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px}
@media(min-width:768px){.wrap{padding:0 40px}}
.mono{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11px;letter-spacing:.18em;
text-transform:uppercase;color:var(--ink3)}
h1,h2,h3{margin:0;font-weight:600;letter-spacing:-.022em;line-height:1.13}
h1{font-size:clamp(30px,5.6vw,58px);letter-spacing:-.03em;line-height:1.08}
h2{font-size:clamp(25px,3.5vw,40px)}
h3{font-size:18.5px;letter-spacing:-.01em;line-height:1.32}
p{margin:0;color:var(--ink2)}a{color:inherit}
.lede{font-size:clamp(16.5px,1.9vw,20px);line-height:1.56;color:var(--ink2)}
nav{position:sticky;top:0;z-index:50;background:rgba(251,251,249,.88);
backdrop-filter:saturate(180%) blur(14px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;justify-content:space-between;height:66px;gap:10px}
.brand{display:flex;align-items:baseline;gap:6px;text-decoration:none;white-space:nowrap}
.brand b{font-weight:600;letter-spacing:-.02em;font-size:16.5px;color:var(--accent)}
.brand span{font-weight:300;font-size:16.5px;color:var(--ink)}
.nav-mid{display:none;gap:30px}@media(min-width:960px){.nav-mid{display:flex}}
.nav-mid a{font-size:14.5px;color:var(--ink2);text-decoration:none}
.nav-mid a:hover{color:var(--accent)}
.nav-right{display:flex;align-items:center;gap:2px}
.langs{display:none;gap:2px;margin-right:6px}@media(min-width:960px){.langs{display:flex}}
.langs a{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.1em;color:var(--ink3);
text-decoration:none;padding:8px 6px}
.langs a:hover,.langs a[aria-current]{color:var(--accent)}
.icon{width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center;
color:var(--ink);text-decoration:none;background:none;border:0;cursor:pointer}
.icon:hover{color:var(--accent)}
#burger{display:inline-flex}@media(min-width:960px){#burger{display:none}}
.btn{display:inline-flex;align-items:center;justify-content:center;background:var(--ink);color:#fff;
text-decoration:none;font-size:14px;font-weight:500;padding:13px 22px;border:1px solid var(--ink)}
.btn:hover{background:var(--accent2);border-color:var(--accent2)}
.btn-lg{padding:17px 28px;font-size:15px}
.btn-g{background:transparent;color:var(--ink);border:1px solid var(--line)}
.btn-g:hover{background:var(--paper2);border-color:var(--ink3);color:var(--ink)}
.nav-cta{display:none}@media(min-width:960px){.nav-cta{display:inline-flex;margin-left:8px}}
#mob{display:none;background:var(--paper);border-bottom:1px solid var(--line)}
#mob.open{display:block}
#mob a.ml{display:block;padding:15px 0;font-size:16.5px;text-decoration:none;border-top:1px solid var(--line)}
#mob .btn{width:100%;margin:16px 0 10px}
#mob .mlangs{display:flex;gap:14px;padding:14px 0 22px;border-top:1px solid var(--line)}
#mob .mlangs a{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.1em;
color:var(--ink3);text-decoration:none;padding:6px 2px}
.hero{padding:56px 0 52px;text-align:center}
@media(min-width:768px){.hero{padding:92px 0 80px}}
.avatar{width:92px;height:92px;border-radius:50%;object-fit:cover;border:1px solid var(--line);margin:0 auto 26px;display:block}
.hero h1{max-width:19ch;margin:20px auto 0}
.quote{font-size:15.5px;font-style:italic;color:var(--accent);margin:22px auto 0;max-width:40ch}
.hero .lede{max-width:56ch;margin:22px auto 0}
.cta-row{display:flex;flex-direction:column;gap:11px;margin:34px auto 0;max-width:520px}
@media(min-width:560px){.cta-row{flex-direction:row;justify-content:center}}
.hero .mono{margin-top:20px;display:block}
.sec{padding:62px 0}@media(min-width:768px){.sec{padding:100px 0}}
.alt{background:var(--paper2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.grid{display:grid;margin-top:40px;border-top:1px solid var(--line)}
@media(min-width:700px){.grid{grid-template-columns:1fr 1fr}}
@media(min-width:1020px){.grid{grid-template-columns:repeat(3,1fr)}}
.cell{padding:28px 0;border-bottom:1px solid var(--line);min-width:0}
@media(min-width:700px){.cell{padding:30px 30px 34px 0}
.cell:nth-child(2n){padding-left:30px;border-left:1px solid var(--line)}}
@media(min-width:1020px){.cell{padding:30px 28px 34px 0}
.cell:nth-child(2n){padding-left:0;border-left:0}
.cell:nth-child(3n+2),.cell:nth-child(3n){padding-left:28px;border-left:1px solid var(--line)}}
.cell .mono{display:block;margin-bottom:13px;color:var(--accent)}
.cell h3{margin-bottom:9px}.cell p{font-size:15.5px;line-height:1.57}
.cell ul{margin:13px 0 0;padding:0;list-style:none}
.cell li{font-size:14.5px;color:var(--ink3);padding-left:15px;position:relative;margin-top:7px}
.cell li:before{content:"";position:absolute;left:0;top:9px;width:5px;height:1px;background:var(--ink3)}
.steps{display:grid;margin-top:42px;border-top:1px solid var(--line)}
@media(min-width:880px){.steps{grid-template-columns:repeat(3,1fr)}}
.step{padding:28px 0;border-bottom:1px solid var(--line);min-width:0}
@media(min-width:880px){.step{padding:32px 34px 38px 0;border-bottom:0}
.step+.step{padding-left:34px;border-left:1px solid var(--line)}}
.step .n{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--accent);display:block;margin-bottom:15px}
.step h3{margin-bottom:9px}.step p{font-size:15.5px}
.who{display:grid;gap:32px;margin-top:40px}
@media(min-width:780px){.who{grid-template-columns:1.2fr 1fr;gap:60px}}
.who .min{min-width:0}
.note{border-left:2px solid var(--accent);padding:2px 0 2px 20px;margin-top:30px;max-width:62ch}
.note p+p{margin-top:11px}.note b{color:var(--ink);font-weight:600}
.facts{border-top:1px solid var(--line);margin-top:15px}
.fact{display:flex;justify-content:space-between;align-items:baseline;gap:18px;padding:15px 0;border-bottom:1px solid var(--line)}
.fact dt{font-size:14.5px;color:var(--ink2);margin:0}
.fact dd{margin:0;font-weight:600;font-size:15px;text-align:right}
.final{padding:66px 0 76px}@media(min-width:768px){.final{padding:100px 0 118px}}
.final h2{max-width:22ch}.final .lede{max-width:56ch;margin-top:18px}
.final .cta-row{margin-left:0;justify-content:flex-start}
footer{border-top:1px solid var(--line);padding:46px 0 56px}
.flinks{display:flex;flex-wrap:wrap;gap:4px 26px;margin:22px 0 24px}
.flinks a{font-size:14px;color:var(--ink2);text-decoration:none;padding:8px 0}
.flinks a:hover{color:var(--accent)}
.fmeta{font-size:12.5px;color:var(--ink3);line-height:1.75}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

def page(code):
    d = L[code]
    url = ORIGIN + d['home']
    scan = SCAN + d['scan_lang']
    diag = DIAG + d['scan_lang']
    e = H.escape
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{c}" href="{ORIGIN}{L[c]["home"]}">' for c, _ in LANGNAMES
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'
    langs = "".join(
        f'<a href="{L[c]["home"]}"{" aria-current=\"page\"" if c == code else ""}>{n}</a>'
        for c, n in LANGNAMES)
    navmid = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in d['nav'])
    mobls = "".join(f'<a class="ml" href="{h}">{e(t)}</a>' for h, t in d['nav'])
    def _cell(i, tag, h3, p, lis):
        extra = ''
        # §10: AI-проверка сайта остаётся, но как вторичный путь внутри
        # категории «Сайт и e-commerce», а не как главный CTA страницы
        if i == 5:
            extra = (f'<p style="margin-top:14px"><a href="{scan}" target="_blank" rel="noopener" '
                     f'style="font-size:14px;color:var(--accent);text-decoration:none;'
                     f'border-bottom:1px solid var(--accent)">{e(d["scan_secondary"])} &rarr;</a></p>')
        return (f'<div class="cell"><span class="mono">{e(tag)}</span><h3>{e(h3)}</h3><p>{e(p)}</p>'
                f'<ul>{"".join(f"<li>{e(li)}</li>" for li in lis)}</ul>{extra}</div>')
    cells = "".join(_cell(i, *pr) for i, pr in enumerate(d['problems']))
    steps = "".join(
        f'<div class="step"><span class="n">{i:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>'
        for i, (t, p) in enumerate(d['steps'], 1))
    facts = "".join(
        f'<div class="fact"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in d['facts'])

    return f"""<!DOCTYPE html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{'<meta name="msvalidate.01" content="F49FB5139071EDA53E1B8CC76652A8D8" />' if code=='ru' else ''}
<title>{e(d['title'])}</title>
<meta name="description" content="{e(d['desc'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="Prodigy LAB">
<meta property="og:title" content="{e(d['title'])}">
<meta property="og:description" content="{e(d['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:locale" content="{d['locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
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
  <div class="nav-mid">{navmid}</div>
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
  <a class="btn" href="{diag}" data-diag>{e(d['cta1'])}</a>
  <a class="ml" href="{PHONE_HREF}">{e(d['call'])} {PHONE_TEXT}</a>
  <div class="mlangs">{langs}</div>
 </div></div>
</nav>

<main>
<section class="hero">
 <div class="wrap">
  <img class="avatar" src="/assets/founder.jpg" alt="{e(d['photo_alt'])}" width="92" height="92">
  <span class="mono">{e(d['eyebrow'])}</span>
  <h1>{e(d['h1'])}</h1>
  <p class="quote">{e(d['quote'])}</p>
  <p class="lede">{e(d['lede'])}</p>
  <div class="cta-row">
   <a class="btn btn-lg" href="{diag}" data-diag>{e(d['cta1'])}</a>
   <a class="btn btn-lg btn-g" href="#problems">{e(d['cta2'])}</a>
  </div>
  <span class="mono">{e(d['note'])}</span>
 </div>
</section>

<section class="sec alt" id="problems">
 <div class="wrap">
  <span class="mono">{e(d['s1_eyebrow'])}</span>
  <h2 style="margin-top:18px;max-width:19ch">{e(d['s1_h2'])}</h2>
  <p class="lede" style="max-width:58ch;margin-top:18px">{e(d['s1_lede'])}</p>
  <div class="grid">{cells}</div>
 </div>
</section>

<section class="sec" id="how">
 <div class="wrap">
  <span class="mono">{e(d['s2_eyebrow'])}</span>
  <h2 style="margin-top:18px;max-width:20ch">{e(d['s2_h2'])}</h2>
  <div class="steps">{steps}</div>
 </div>
</section>

<section class="sec alt" id="who">
 <div class="wrap">
  <span class="mono">{e(d['s3_eyebrow'])}</span>
  <h2 style="margin-top:18px;max-width:22ch">{e(d['s3_h2'])}</h2>
  <div class="who">
   <div class="min">
    <p class="lede" style="max-width:none">{e(d['s3_p1'])}</p>
    <p style="margin-top:18px">{e(d['s3_p2'])}</p>
    <div class="note"><p><b>{e(d['no_title'])}.</b> {e(d['no_p1'])}</p><p>{e(d['no_p2'])}</p></div>
   </div>
   <div class="min">
    <span class="mono">{e(d['facts_title'])}</span>
    <dl class="facts">{facts}</dl>
    <p style="font-size:13.5px;color:var(--ink3);margin-top:16px;line-height:1.6">{e(d['remote'])}</p>
   </div>
  </div>
 </div>
</section>

<section class="final" id="diagnostic">
 <div class="wrap">
  <span class="mono">{e(d['final_eyebrow'])}</span>
  <h2 style="margin-top:18px">{e(d['final_h2'])}</h2>
  <p class="lede">{e(d['final_lede'])}</p>
  <div class="cta-row">
   <a class="btn btn-lg" href="{diag}" data-diag>{e(d['final_cta1'])}</a>
   <a class="btn btn-lg btn-g" href="{WA}" target="_blank" rel="noopener">{e(d['final_cta2'])}</a>
  </div>
  <span class="mono" style="display:block;margin-top:20px"><a href="{PHONE_HREF}" style="color:var(--accent);text-decoration:none">{e(d['call'])} {PHONE_TEXT}</a></span>
 </div>
</section>
</main>

<footer>
 <div class="wrap">
  <a class="brand" href="{d['home']}"><b>PRODIGY</b><span>LAB</span></a>
  <div class="flinks">
   {"".join(f'<a href="{h}">{e(t)}</a>' for h,t in d['nav'])}
   <a href="{PHONE_HREF}">{PHONE_TEXT}</a>
   <a href="{PRIVACY[code]}">{e(d['foot_priv'])}{PRIVACY_TAG[code]}</a>
  </div>
  <div style="border-top:1px solid var(--line);padding-top:18px">
   <span class="mono" style="display:block;margin-bottom:10px">{H.escape(SERVICE_HEAD[code])}</span>
   <div class="flinks" style="margin:0">{service_links(code)}</div>
  </div>
  <p class="fmeta">© 2026 Prodigy LAB · Platonaire LLC · California, USA<br>{e(d['foot_legal'])}</p>
 </div>
</footer>

<script>
// §14 — язык в каждом событии, чтобы канал считался по локали
window.PL_LANG="{code}";
window.plEvent=function(n,x){{var p=Object.assign({{page_language:"{code}",
 content_language:"{code}",destination_language:"{code}"}},x||{{}});
 if(typeof fbq==='function') fbq('trackCustom',n,p);
 (window.dataLayer=window.dataLayer||[]).push(Object.assign({{event:n}},p));}};
// Незаметная смена языка — это дефект, а не фича: помечаем его отдельно
(function(){{var nav=(navigator.language||'').slice(0,2);
 if(nav && nav!=="{code}" && !sessionStorage.getItem('pl_lang_choice')){{
  plEvent('language_mismatch_detected',{{browser_language:nav}});}}}})();
// UTM и реферер прокидываем в диагностику, иначе источник заявки теряется (ТЗ §8)
(function(){{var q=new URLSearchParams(location.search);
 document.querySelectorAll('a[data-diag]').forEach(function(a){{
  var u=new URL(a.href);
  ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid','gclid'].forEach(function(k){{
   if(q.get(k)) u.searchParams.set(k,q.get(k));}});
  u.searchParams.set('from', location.pathname);
  if(document.referrer) u.searchParams.set('ref', document.referrer.slice(0,200));
  a.href=u.toString();
  a.addEventListener('click',function(){{
   plEvent('localized_cta_clicked',{{destination:'diagnostic'}});
  }});}});}})();
document.querySelectorAll('.langs a,.mlangs a').forEach(function(a){{
 a.addEventListener('click',function(){{
  try{{sessionStorage.setItem('pl_lang_choice','1');}}catch(e){{}}
  plEvent('language_selected',{{to:(a.getAttribute('href')||'').replace(/\//g,'')||'en'}});}});}});
function tg(b){{var m=document.getElementById('mob');
 var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');}}
document.querySelectorAll('#mob a').forEach(function(a){{a.addEventListener('click',function(){{
 document.getElementById('mob').classList.remove('open');
 document.getElementById('burger').setAttribute('aria-expanded','false');}});}});
</script>
<script>
 (function (d, t) {{
  var B="https://chat.prodigylab.studio";var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
  g.src=B+"/packs/js/sdk.js";g.defer=true;g.async=true;s.parentNode.insertBefore(g,s);
  g.onload=function(){{window.chatwootSettings=window.chatwootSettings||{{}};
   window.chatwootSettings.locale="{code}";
   window.chatwootSDK.run({{websiteToken:"J1xMPSabyx7EfRVPrmZEMLYB",baseUrl:B}});
   // Бот должен говорить на языке страницы ещё ДО первой реплики,
   // и знать, откуда человек пришёл (ТЗ §11).
   window.addEventListener('chatwoot:ready',function(){{
    try{{
     window.$chatwoot.setLocale("{code}");
     var q=new URLSearchParams(location.search);
     window.$chatwoot.setCustomAttributes({{
      ui_language:"{code}", page_language:"{code}", page_url:location.href,
      from_page:document.referrer||"", utm_source:q.get('utm_source')||"",
      utm_medium:q.get('utm_medium')||"", utm_campaign:q.get('utm_campaign')||"",
      problem_category:(location.hash||"").replace('#','')
     }});
     if(typeof fbq==='function') fbq('trackCustom','bot_opened',{{page_language:"{code}"}});
    }}catch(e){{}}
   }});}};
 }})(document,"script");
</script>
</body>
</html>"""

if __name__ == '__main__':
    for code, rel in OUT.items():
        p = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        html = page(code)
        open(p, 'w', encoding='utf-8').write(html)
        print(f"  ✓ {rel:16} {len(html)//1024} KB  ({code})")
    print("Главная пересобрана на 5 языках")
