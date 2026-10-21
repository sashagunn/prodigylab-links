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

# Порядок карточек на главной = порядок девяти слоёв Jev/Copilot. Связь именно
# позиционная, потому что в home_content карточки лежат списком без ключей;
# тест в scripts/check-i18n.py следит, чтобы их осталось девять.
LAYER_BY_INDEX = ('payments', 'banking', 'business_funding', 'growth',
                  'operations', 'infrastructure', 'accounting_tax',
                  'fulfillment_logistics', 'digital_presence')
ORIGIN = 'https://prodigylab.studio'
DECIDE = 'https://scan.prodigylab.studio/api/jev/decide'
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


КОРЕНЬ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

НОВОЕ_CSS = """/* Прототип новой главной Prodigy LAB — фотографическая версия.
   Палитра действующая, с боевого сайта. Шрифты с запасом: без Google
   страница остаётся читаемой на системных. */
:root{
  --paper:#FBFBF9; --paper2:#F3F2EE; --ink:#121212; --ink2:#5C5C5A;
  --ink3:#8A8A86; --line:#E2E1DC; --accent:#1C7E84; --accent2:#0F4A4E;
  --accent-soft:#E3F0F0; --graphite:#0F1722; --graphite2:#16222A;
  --on-dark:#E8ECEF; --on-dark2:#95A3B3;
  --sans:Geist,system-ui,-apple-system,"Segoe UI",sans-serif;
  --serif:'Instrument Serif',Georgia,'Times New Roman',serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,monospace;
  --wrap:1280px; --gut:clamp(20px,4vw,56px);
  --r:18px;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:17px;line-height:1.55;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit}
button{font:inherit;color:inherit}
h1,h2,h3{margin:0;font-weight:700;letter-spacing:-.03em;line-height:1.06}
p{margin:0}
ul,ol{margin:0;padding:0;list-style:none}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 var(--gut)}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.eyebrow,.tag{font-family:var(--mono);font-size:10.5px;letter-spacing:.17em;
  text-transform:uppercase;color:var(--ink3)}
.em{font-family:var(--serif);font-style:italic;font-weight:400;color:var(--accent);
  letter-spacing:-.01em}

/* ------------------------------------------------------------------ шапка */
.top{position:sticky;top:0;z-index:60;background:rgba(251,251,249,.88);
  backdrop-filter:saturate(1.5) blur(10px);border-bottom:1px solid var(--line)}
.top-in{display:flex;align-items:center;gap:28px;height:62px;
  max-width:var(--wrap);margin:0 auto;padding:0 var(--gut)}
.mark{font-weight:800;letter-spacing:-.02em;font-size:18px;text-decoration:none}
.mark i{color:var(--accent);font-style:normal}
.top-nav{display:flex;gap:26px;font-size:14px;color:var(--ink2)}
.top-nav a{text-decoration:none}
.top-nav a:hover{color:var(--ink)}
.top-r{margin-left:auto;display:flex;align-items:center;gap:10px}
.langs{display:flex;gap:2px}
.langs button{background:none;border:0;padding:5px 7px;cursor:pointer;
  font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--ink3)}
.langs button[aria-current="true"]{color:var(--ink);font-weight:500;
  box-shadow:inset 0 -1px 0 var(--ink)}

/* ----------------------------------------------------------- первый экран */
#hm-hero{position:relative;padding:clamp(22px,3.4vh,44px) 0 clamp(40px,5vw,72px);
  overflow:hidden}
/* Фотография живёт за правой половиной и мягко растворяется влево. */
.hero-ph{position:absolute;inset:0 0 0 38%;background-size:cover;
  background-position:center;opacity:0;transition:opacity .7s ease}
.hero-ph.on{opacity:1}
.hero-ph:after{content:"";position:absolute;inset:0;
  background:linear-gradient(90deg,var(--paper) 0%,rgba(251,251,249,.72) 26%,
    rgba(251,251,249,.10) 62%,rgba(15,23,34,.22) 100%)}
.hero-in{position:relative;z-index:2;max-width:var(--wrap);margin:0 auto;
  padding:0 var(--gut);display:grid;grid-template-columns:minmax(0,50fr) minmax(0,50fr);
  gap:clamp(22px,3vw,54px);align-items:center}
.hero-l{max-width:620px}
h1#h1{font-size:clamp(34px,4.1vw,58px);margin:12px 0 0;letter-spacing:-.035em;max-width:16ch}
h1#h1 .ln{display:block;overflow:hidden}
h1#h1 .ln>span{display:block;transform:translateY(110%);opacity:0;
  transition:transform .85s cubic-bezier(.25,.6,.25,1),opacity .85s ease}
h1#h1 .ln>span.in{transform:none;opacity:1}
.hm-lede{margin-top:16px;color:var(--ink2);font-size:18px;max-width:40ch}

/* панель разговора */
.talk{margin-top:22px;background:rgba(255,255,255,.92);backdrop-filter:blur(6px);
  border:1px solid var(--line);border-radius:var(--r);
  box-shadow:0 2px 2px rgba(18,18,18,.02),0 26px 60px -40px rgba(18,18,18,.55)}
.talk-h{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:11px 16px;border-bottom:1px solid var(--line)}
.talk-n{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink3)}
.lang{position:relative}
#lang-btn{background:none;border:1px solid var(--line);border-radius:999px;
  padding:5px 12px;font-size:12.5px;cursor:pointer;color:var(--ink2)}
#lang-btn:hover{border-color:var(--ink3)}
#lang-list{position:absolute;right:0;top:calc(100% + 6px);background:#fff;
  border:1px solid var(--line);border-radius:12px;padding:5px;min-width:155px;
  z-index:30;box-shadow:0 24px 50px -28px rgba(18,18,18,.5)}
#lang-list button{display:block;width:100%;text-align:left;background:none;
  border:0;padding:8px 11px;font-size:14px;cursor:pointer;border-radius:8px}
#lang-list button:hover{background:var(--paper2)}
#lang-list button[aria-current="true"]{color:var(--accent)}
/* Пустая лента держит высоту и подсказывает, с чего начать. */
.stream{min-height:150px;max-height:min(38vh,360px);overflow:auto;padding:14px 16px;
  display:flex;flex-direction:column;justify-content:flex-end;gap:9px;scrollbar-width:thin}
.m{font-size:15px;line-height:1.5;border-radius:16px;padding:10px 14px;max-width:92%}
.m>b{display:block;font-family:var(--mono);font-size:9px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink3);font-weight:400;margin-bottom:3px}
.m-bot{background:var(--accent-soft);border:1px solid #CFE3E3;align-self:flex-start;
  border-bottom-left-radius:5px}
.m-you{background:#fff;border:1px solid var(--line);align-self:flex-end;
  border-bottom-right-radius:5px}
.m-note{align-self:flex-start;font-size:13px;color:var(--ink2);background:none;
  border-left:2px solid var(--line);border-radius:0;padding:2px 0 2px 10px}
.m-err{align-self:flex-start;font-size:13px;color:#8A3A1C;background:#FBF0E9}
.wait{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--ink3);
  font-family:var(--mono);letter-spacing:.05em}
.wait i{width:6px;height:6px;border-radius:50%;background:var(--accent);
  animation:pulse 1s infinite ease-in-out}
@keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}
.tr{display:inline-block;margin:6px 8px 0 0;background:none;border:1px solid var(--line);
  border-radius:999px;padding:5px 12px;font-size:12.5px;cursor:pointer;color:var(--ink2)}
.tr:hover{border-color:var(--ink3)}
/* Ряд подсказок держит высоту: иначе появление вариантов сдвигает ввод. */
.sugg{display:flex;flex-wrap:wrap;gap:7px;padding:0 16px;min-height:40px;
  align-content:flex-start}
.sugg button{background:#fff;border:1px solid var(--line);border-radius:999px;
  padding:8px 14px;font-size:14px;cursor:pointer}
.sugg button:hover{border-color:var(--accent);color:var(--accent2)}
#ask{display:flex;gap:8px;padding:14px 16px;align-items:center}
#ask-i{flex:1;min-width:0;border:1px solid var(--line);border-radius:999px;
  padding:14px 18px;font-size:16px;background:#fff}
#ask-i:focus{outline:2px solid var(--accent);outline-offset:-1px;border-color:transparent}
#ask-b{width:46px;height:46px;border:0;border-radius:50%;background:var(--accent);
  color:#fff;font-size:17px;cursor:pointer;flex:none;transition:transform .15s}
#ask-b:hover{background:var(--accent2);transform:scale(1.05)}
#ask-b:disabled{opacity:.5}

.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:14px}
.chips button{background:rgba(255,255,255,.9);border:1px solid var(--line);
  border-radius:999px;padding:9px 15px;font-size:14px;cursor:pointer}
.chips button:hover{border-color:var(--ink)}
.chips button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.chips .near button{color:var(--ink2)}
.tail{display:flex;gap:18px;align-items:center;margin-top:14px;font-size:13.5px}
.tail button{background:none;border:0;padding:0;cursor:pointer;color:var(--ink2);
  text-decoration:underline;text-underline-offset:3px}
.tail a{color:var(--accent2);text-decoration:underline;text-underline-offset:3px}

/* правая колонка: трекер + макет устройства */
.hero-r{display:flex;flex-direction:column;align-items:center;gap:16px}
.steps{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;
  background:rgba(255,255,255,.92);border:1px solid var(--line);border-radius:999px;
  padding:7px 10px;box-shadow:0 14px 34px -26px rgba(18,18,18,.6);max-width:100%}
.hm-step{display:flex;align-items:center;gap:7px;padding:3px 9px;border-radius:999px;
  max-width:260px}
.hm-step .hm-mono{font-family:var(--mono);font-size:9px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink3);white-space:nowrap}
.hm-step .hm-mono i{font-style:normal;color:var(--accent)}
.hm-step p{font-size:12.5px;color:var(--ink);overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap;max-width:180px}
.hm-step p.dim{color:var(--ink3)}
.hm-step.live{background:var(--accent-soft)}
.hm-step.done .hm-mono i{color:var(--accent2)}

#hm-scene{width:100%;perspective:1400px}

/* макет браузера с настоящим снимком демо */
.shot{position:relative;width:100%}
.shot-win{border-radius:14px;overflow:hidden;background:var(--graphite2);
  border:1px solid rgba(15,23,34,.16);
  box-shadow:0 40px 80px -40px rgba(15,23,34,.65);
  transform:translate3d(var(--dx,0),var(--dy,0),0);transition:transform .9s cubic-bezier(.25,.6,.25,1)}
.shot-bar{display:flex;align-items:center;gap:8px;padding:9px 12px;
  background:#242B31;border-bottom:1px solid rgba(255,255,255,.08)}
.shot-bar i{width:9px;height:9px;border-radius:50%;background:#4A535B;display:block}
.shot-bar span{margin-left:auto;margin-right:auto;font-family:var(--mono);
  font-size:10.5px;color:#9AA4AD}
.shot-win img{width:100%;display:block;aspect-ratio:1440/900;object-fit:cover;
  object-position:top}
.shot-phone{position:absolute;right:-8px;bottom:-26px;width:190px;
  border-radius:26px;padding:7px;background:#0B0F14;
  border:2px solid rgba(255,255,255,.12);
  box-shadow:0 36px 60px -30px rgba(15,23,34,.8);z-index:3}
.shot-phone img{width:100%;border-radius:20px;aspect-ratio:390/720;object-fit:cover;
  object-position:top}
.shot-cap{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:16px;
  font-size:13.5px;color:var(--ink2)}
.shot-cap .tag{background:rgba(255,255,255,.85);border:1px solid var(--line);
  padding:4px 9px;border-radius:999px}
.shot-dev{display:inline-flex;gap:4px;background:rgba(255,255,255,.9);
  border:1px solid var(--line);border-radius:999px;padding:3px}
.shot-dev button{background:none;border:0;border-radius:999px;padding:5px 12px;
  font-size:12px;cursor:pointer;color:var(--ink2)}
.shot-dev button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.shot-go{color:var(--accent2);text-decoration:underline;text-underline-offset:3px;
  font-size:13.5px;margin-left:auto}

/* схема разбора вместо снимка, когда опубликованного примера нет */
.scheme{width:100%;background:rgba(255,255,255,.94);border:1px solid var(--line);
  border-radius:var(--r);padding:clamp(16px,2vw,24px);
  box-shadow:0 30px 70px -45px rgba(18,18,18,.6)}
.scheme-h{display:flex;align-items:center;justify-content:space-between;gap:12px;
  margin-bottom:14px}
.scheme-sw{display:inline-flex;gap:4px;background:var(--paper2);border-radius:999px;padding:3px}
.scheme-sw button{background:none;border:0;border-radius:999px;padding:6px 13px;
  font-size:12px;cursor:pointer;color:var(--ink2)}
.scheme-sw button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.scheme-l{display:grid;gap:8px}
.nd{display:grid;grid-template-columns:30px 1fr;gap:10px;align-items:start;
  padding:11px 12px;border-radius:12px;background:var(--paper2);
  transition:background .3s,opacity .3s}
.nd-n{font-family:var(--mono);font-size:10px;color:var(--ink3);padding-top:3px}
.nd b{display:block;font-size:15.5px;font-weight:600}
.nd-p{display:block;color:var(--ink2);font-size:13.5px;margin-top:2px}
.scheme[data-mode="b"] .nd[data-i="1"],.scheme[data-mode="b"] .nd[data-i="2"]{opacity:.35}
.scheme[data-mode="b"] .nd[data-i="3"]{background:var(--accent-soft);
  box-shadow:inset 3px 0 0 var(--accent)}
.scheme-need{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin-top:14px}
.scheme-need span{font-family:var(--mono);font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink3)}
.scheme-need ul{display:flex;flex-wrap:wrap;gap:6px}
.scheme-need li{border:1px solid var(--line);border-radius:999px;padding:5px 11px;
  font-size:12.5px;background:#fff}
.scheme-note{margin-top:12px;font-size:12.5px;color:var(--ink3)}

/* ------------------------------------------------- адаптивный тёмный раздел */
#pf{position:relative;background:var(--graphite);color:var(--on-dark);
  padding:clamp(54px,7vw,104px) 0;overflow:hidden}
.pf-ph{position:absolute;inset:-160px 0;background-size:cover;background-position:center;
  z-index:0;pointer-events:none}
.pf-ph:after{content:"";position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(15,23,34,.97) 8%,rgba(15,23,34,.74) 42%,
    rgba(15,23,34,.52) 70%,rgba(15,23,34,.72) 100%)}
#pf:after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,rgba(15,23,34,.35),rgba(15,23,34,0) 20%,rgba(15,23,34,.35))}
.pf-in{position:relative;z-index:2;max-width:var(--wrap);margin:0 auto;padding:0 var(--gut)}
.pf-v{position:relative;display:grid;grid-template-columns:minmax(0,42fr) minmax(0,58fr);
  gap:clamp(24px,3.4vw,64px);align-items:start}
.pf-l{position:sticky;top:90px;z-index:2}
.pf-r{z-index:2}
.pf-r{display:grid;gap:clamp(16px,2vw,26px)}
.pf-eyebrow{font-family:var(--mono);font-size:10.5px;letter-spacing:.17em;
  text-transform:uppercase;color:var(--on-dark2)}
.pf-h{font-size:clamp(30px,3.6vw,52px);margin:14px 0 0;max-width:15ch;color:#fff}
.pf-lede{margin-top:16px;color:var(--on-dark2);font-size:16.5px;max-width:46ch}
.pf-anchor{display:block;height:0}
.pf-cta{margin-top:26px;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.pf-main{background:var(--accent);color:#fff;border:0;border-radius:999px;
  padding:15px 26px;font-size:15.5px;cursor:pointer;transition:transform .15s}
.pf-main:hover{background:#23919A;transform:translateX(2px)}
.pf-cta a{color:var(--on-dark2);text-decoration:underline;text-underline-offset:4px;
  font-size:14.5px}
.pf-note{margin-top:16px;color:var(--on-dark2);font-size:13px}
/* правая карточка раздела — светлая, на ней шаги и границы */
.pf-card{background:#FCFCFA;color:var(--ink);border-radius:var(--r);
  padding:clamp(20px,2.4vw,32px);box-shadow:0 50px 90px -50px rgba(0,0,0,.8)}
.pf-card-min{padding:clamp(16px,1.8vw,22px)}
.pf-card-h{display:flex;align-items:center;justify-content:space-between;gap:14px;
  padding-bottom:14px;border-bottom:1px solid var(--line)}
.pf-card-h h3{font-size:17px}
.pf-card-h .tag{background:var(--accent-soft);color:var(--accent2);padding:5px 10px;
  border-radius:999px}
.pf-steps{margin-top:18px;display:grid;gap:10px}
.pf-steps li{display:grid;grid-template-columns:30px 1fr;gap:10px;align-items:start}
.pf-steps b{font-family:var(--mono);font-size:10px;color:var(--ink3);padding-top:4px}
.pf-steps h3{font-size:16px}
.pf-steps p{margin-top:2px;color:var(--ink2);font-size:13.5px}
.pf-two{margin-top:20px;padding-top:16px;border-top:1px solid var(--line);
  display:grid;gap:14px}
.pf-two h3{font-family:var(--mono);font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink3);font-weight:400}
.pf-need ul{display:flex;flex-wrap:wrap;gap:7px;margin-top:9px}
.pf-need li{border:1px solid var(--line);border-radius:999px;padding:6px 11px;font-size:13px}
.pf-lim p{margin-top:9px;color:var(--ink2);font-size:13.5px}
#pf-switch{position:fixed;left:50%;transform:translateX(-50%);bottom:18px;z-index:55;display:none}
#pf-switch[data-on="1"]{display:block}
#pf-switch button{background:var(--ink);color:var(--paper);border:0;border-radius:999px;
  padding:12px 22px;font-size:14px;cursor:pointer;box-shadow:0 18px 40px -20px rgba(0,0,0,.7)}

/* ------------------------------------------------------------------ работы */
.band-works{padding:clamp(56px,7vw,104px) 0;background:var(--paper)}
.wk-h{max-width:var(--wrap);margin:0 auto;padding:0 var(--gut)}
.wk-h h2{font-size:clamp(30px,3.8vw,54px);max-width:18ch}
.wk-h p{margin-top:14px;color:var(--ink2);max-width:56ch;font-size:16.5px}
.wk-grid{max-width:var(--wrap);margin:clamp(28px,3.4vw,52px) auto 0;padding:0 var(--gut);
  display:grid;grid-template-columns:1fr 1fr;gap:clamp(18px,2.4vw,34px)}
.wk{display:flex;flex-direction:column}
.wk-card{position:relative;border-radius:var(--r);overflow:hidden;min-height:440px;
  display:flex;flex-direction:column;justify-content:space-between;padding:20px;
  background-size:cover;background-position:center;isolation:isolate}
.wk-card:before{content:"";position:absolute;inset:0;z-index:0;
  background:linear-gradient(180deg,rgba(10,14,20,.55) 0%,rgba(10,14,20,.25) 40%,rgba(10,14,20,.78) 100%)}
.wk-top{position:relative;z-index:2;display:flex;align-items:center;
  justify-content:space-between;gap:10px;color:#fff}
.wk-name{font-size:14px;font-weight:600;letter-spacing:-.01em}
.wk-tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;
  background:rgba(0,0,0,.42);backdrop-filter:blur(4px);padding:5px 9px;border-radius:999px;color:#fff}
.wk-inset{position:relative;z-index:2;align-self:flex-end;width:min(100%,330px);
  border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,.3);
  box-shadow:0 30px 60px -30px rgba(0,0,0,.9);margin-top:24px}
.wk-inset img{width:100%;height:auto;display:block}
.wk[data-dev="d"] .wk-inset img{aspect-ratio:16/10;object-fit:cover;object-position:top}
.wk[data-dev="p"] .wk-inset{width:min(60%,210px)}
.wk[data-dev="p"] .wk-inset img{aspect-ratio:390/700;object-fit:cover;object-position:top}
.wk-body{padding:16px 2px 0}
.wk-body h3{font-size:20px}
.wk-body dl{margin:12px 0 0;display:grid;gap:10px}
.wk-body dt{font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink3)}
.wk-body dd{margin:3px 0 0;font-size:14.5px;color:var(--ink2)}
.wk-links{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:16px}
.wk-go{display:inline-flex;align-items:center;gap:9px;background:var(--ink);color:var(--paper);
  text-decoration:none;border-radius:999px;padding:12px 20px;font-size:14.5px}
.wk-go:hover{background:var(--accent2)}
.wk-sec{color:var(--ink2);text-decoration:underline;text-underline-offset:4px;font-size:13.5px}
.wk-dev{display:inline-flex;gap:4px;background:rgba(255,255,255,.92);
  border-radius:999px;padding:3px;position:relative;z-index:2;align-self:flex-start;
  margin-top:14px}
.wk-dev button{background:none;border:0;border-radius:999px;padding:5px 11px;
  font-size:11.5px;cursor:pointer;color:var(--ink2)}
.wk-dev button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}

/* ------------------------------------------------------ девять направлений */
.band-layers{padding:clamp(48px,6vw,88px) 0;background:var(--paper2);
  border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.lay-h h2{font-size:clamp(28px,3.4vw,46px)}
.lay-h p{margin-top:12px;color:var(--ink2);max-width:52ch;font-size:16px}
#layers{display:flex;flex-wrap:wrap;gap:9px;margin-top:24px}
#layers button{background:#fff;border:1px solid var(--line);border-radius:999px;
  padding:11px 18px;cursor:pointer;font-size:14.5px;transition:transform .15s}
#layers button:hover{border-color:var(--ink);transform:translateY(-1px)}
#layers button span{display:none}
#layers-picked{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:24px}
#layers-name{font-weight:600}
#layers-change{background:#fff;border:1px solid var(--line);border-radius:999px;
  padding:7px 14px;font-size:13px;cursor:pointer}

/* ------------------------------------------------------------------ кто мы */
.band-who{padding:clamp(48px,6vw,88px) 0}
.who{max-width:var(--wrap);margin:0 auto;padding:0 var(--gut);
  display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(20px,3vw,44px);align-items:start}
.who-face{width:96px;height:96px;border-radius:14px;object-fit:cover;filter:grayscale(1)}
.who-role{font-family:var(--mono);font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink3);margin-bottom:10px}
.who h2{font-size:clamp(24px,2.6vw,36px);max-width:22ch}
.who p{margin-top:14px;color:var(--ink2);max-width:60ch;font-size:16px}
.facts{display:flex;flex-wrap:wrap;gap:0;margin-top:24px;border-top:1px solid var(--line)}
.facts div{padding:13px 24px 13px 0;margin-right:24px;border-right:1px solid var(--line)}
.facts div:last-child{border-right:0}
.facts dt{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink3)}
.facts dd{margin:3px 0 0;font-weight:600;font-size:15px}

/* ------------------------------------------------------------------- финал */
.band-final{position:relative;background:var(--graphite);color:var(--on-dark);
  padding:clamp(60px,8vw,118px) 0;overflow:hidden}
.fin-ph{position:absolute;inset:0;background-size:cover;background-position:center;
  opacity:.3;transition:opacity .7s}
.band-final:after{content:"";position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(15,23,34,.95) 30%,rgba(15,23,34,.55) 100%)}
.fin-in{position:relative;z-index:2;max-width:var(--wrap);margin:0 auto;padding:0 var(--gut)}
.fin-in .eyebrow{color:var(--on-dark2)}
.fin-in h2{font-size:clamp(32px,4.6vw,66px);margin-top:14px;max-width:16ch;color:#fff}
.fin-in p.lede{margin-top:18px;color:var(--on-dark2);max-width:54ch;font-size:16.5px}
.fin-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}
.fin-row button,.fin-row a{border-radius:999px;padding:16px 28px;font-size:16px;
  text-decoration:none;cursor:pointer;border:1px solid transparent}
#fin-talk{background:var(--accent);color:#fff;border:0}
#fin-talk:hover{background:#23919A}
.fin-alt{border-color:rgba(255,255,255,.32)!important;color:var(--on-dark)}
.fin-alt:hover{border-color:#fff!important}
#fin-state{margin-top:16px;font-size:15px;color:#9FD4C4}
.fin-scan{margin-top:clamp(28px,3.4vw,48px);padding-top:22px;
  border-top:1px solid rgba(255,255,255,.16);display:flex;flex-wrap:wrap;gap:16px;
  align-items:center;justify-content:space-between}
.fin-scan p{color:var(--on-dark2);font-size:15px;max-width:52ch}
.fin-scan a{color:#fff;text-decoration:underline;text-underline-offset:4px;font-size:15px}

/* ------------------------------------------------------------------ подвал */
.foot{padding:30px 0 42px;background:var(--paper)}
.foot-in{max-width:var(--wrap);margin:0 auto;padding:0 var(--gut);
  display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:center}
.foot-mark{display:flex;align-items:center;gap:12px;font-weight:800;font-size:18px}
.foot-mark i{color:var(--accent);font-style:normal}
.foot-mark img{width:36px;height:36px;object-fit:contain}
.foot-r{display:flex;flex-wrap:wrap;gap:18px;align-items:center;
  font-size:13.5px;color:var(--ink2)}
.foot-r a{text-decoration:none}
.foot-r a:hover{color:var(--ink)}
.foot-legal{max-width:var(--wrap);margin:18px auto 0;padding:0 var(--gut);
  color:var(--ink3);font-size:12.5px}

/* ------------------------------------------------------ закреплённая полоса */
#sn-sticky{position:fixed;left:0;right:0;bottom:0;z-index:50;background:#fff;
  border-top:1px solid var(--line);padding:10px 16px;display:none;gap:12px;
  align-items:center;justify-content:space-between}
#sn-sticky a{background:var(--ink);color:var(--paper);text-decoration:none;
  border-radius:999px;padding:11px 18px;font-size:14px;white-space:nowrap}
#sn-sticky span{font-size:13px;color:var(--ink2)}
#sn-sticky[data-off="1"]{display:none!important}

/* --------------------------------------------------------- заявка в потоке */
.fin{background:#fff;border:1px solid var(--accent);border-radius:16px;padding:16px;
  align-self:stretch;max-width:100%}
.fin h3{font-size:16.5px}
.fin ul{margin:10px 0 0;display:grid;gap:5px}
.fin li{font-size:14px;color:var(--ink2);padding-left:14px;position:relative}
.fin li:before{content:"";position:absolute;left:0;top:9px;width:5px;height:5px;
  border-radius:50%;background:var(--line)}
.fin .edit{background:none;border:0;padding:0;color:var(--accent2);cursor:pointer;
  text-decoration:underline;text-underline-offset:3px;font-size:13.5px}
.fin .next{background:var(--accent-soft);border-left:2px solid var(--accent);
  padding:11px 13px;font-size:14.5px;margin-bottom:14px;border-radius:0 10px 10px 0}
.fin label{display:block;font-size:12.5px;color:var(--ink2);margin:12px 0 6px}
.fin input{width:100%;border:1px solid var(--line);border-radius:12px;padding:11px 13px;font-size:15px}
.fin input:focus{outline:2px solid var(--accent);outline-offset:-1px}
.fin .ways{display:flex;flex-wrap:wrap;gap:7px}
.fin .ways button{background:#fff;border:1px solid var(--line);border-radius:999px;
  padding:9px 14px;font-size:14px;cursor:pointer}
.fin .ways button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.fin .row{display:flex;gap:12px;align-items:center;margin-top:16px;flex-wrap:wrap}
.hm-go{background:var(--ink);color:var(--paper);border:0;border-radius:999px;
  padding:13px 22px;font-size:15px;cursor:pointer}
.hm-go:hover{background:var(--accent2)}
.fin .ok b{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--accent2);margin-bottom:6px;font-weight:400}
.fin .err{margin-top:10px;color:#8A3A1C;font-size:13.5px}

/* ------------------------------------------------------------- проявление */
.rise{opacity:0;transform:translateY(6px);
  transition:opacity .9s cubic-bezier(.25,.6,.25,1),transform .9s cubic-bezier(.25,.6,.25,1)}
.rise.seen{opacity:1;transform:none}


/* ----------------------------------------------------------------- планшет */
@media (max-width:1080px){
  .hero-in{grid-template-columns:1fr;gap:26px}
  .hero-ph{inset:0;opacity:.18}
  .hero-ph:after{background:linear-gradient(180deg,rgba(251,251,249,.92),rgba(251,251,249,.78))}
  .hero-l{max-width:none}
  .pf-v{grid-template-columns:1fr}
  .wk-grid{grid-template-columns:1fr}
  .shot-phone{width:150px;right:-4px;bottom:-18px}
}

/* ----------------------------------------------------------------- телефон */
@media (max-width:700px){
  body{font-size:16px}
  .top-nav{display:none}
  h1#h1{font-size:clamp(30px,8.4vw,40px)}
  .hm-lede{font-size:15.5px;margin-top:12px}
  .talk{margin-top:16px}
  .stream{max-height:36vh}
  .steps{border-radius:16px;flex-direction:column;align-items:stretch;padding:8px}
  .hm-step{max-width:none}
  .hm-step p{max-width:none;white-space:normal;font-size:13px}
  .shot-phone{display:none}
  .wk-card{min-height:360px}
  .who{grid-template-columns:1fr}
  .facts div{border-right:0;padding:10px 0;margin-right:0;width:100%;
    display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid var(--line)}
  .facts dd{margin:0}
  .fin-scan{flex-direction:column;align-items:flex-start}
  #sn-sticky{display:flex}
  html.hm-on #sn-sticky{display:none}
}

@media (prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important}
  html{scroll-behavior:auto}
  h1#h1 .ln>span{transform:none;opacity:1}
  .rise{opacity:1!important;transform:none!important}
  .shot-win{transform:none!important}
}


/* ---------------------------------------- визуальные модели разбора в полосе */
.pf-visual{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);
  border-radius:var(--r);padding:clamp(18px,2.2vw,28px);backdrop-filter:blur(3px)}
.pf-visual .pf-eyebrow{color:var(--on-dark2)}
.pf-visual .pf-note{margin-top:14px;font-size:12.5px;color:var(--on-dark2)}

/* ветвление: откуда может идти причина */
.tree{margin-top:16px;display:grid;gap:12px;justify-items:center;text-align:center}
.tree-top{background:var(--graphite2);border:1px solid rgba(255,255,255,.18);
  border-radius:12px;padding:12px 18px;font-weight:600;color:#fff;max-width:36ch}
.tree-br{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
  gap:10px;width:100%;position:relative;padding-top:18px}
.tree-br:before{content:"";position:absolute;top:0;left:50%;width:1px;height:18px;
  background:rgba(255,255,255,.28)}
.br{position:relative;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.16);
  border-radius:12px;padding:12px;font-size:13.5px;color:var(--on-dark);text-align:left}
.br:before{content:"";position:absolute;top:-18px;left:50%;width:1px;height:18px;
  background:rgba(255,255,255,.28)}
.br-n{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;
  color:var(--on-dark2);margin-bottom:5px}
.tree-end{margin-top:6px;background:var(--accent);color:#fff;border-radius:12px;
  padding:12px 18px;font-weight:600;max-width:42ch}
.tree-end span{display:block;font-weight:400;font-size:13px;opacity:.9;margin-top:3px}

/* поток: путь заявки, с переключателем «вручную / после автоматизации» */
.flow-h{display:flex;justify-content:flex-end;margin-top:14px}
.flow .scheme-sw{background:rgba(255,255,255,.08)}
.flow .scheme-sw button{color:var(--on-dark2)}
.flow .scheme-sw button[aria-pressed="true"]{background:#fff;color:var(--graphite)}
.flow-l{margin-top:14px;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.fl{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.16);
  border-radius:12px;padding:13px;transition:opacity .3s,background .3s}
.fl b{display:block;font-size:14.5px;color:#fff}
.fl span{display:block;font-size:12.5px;color:var(--on-dark2);margin-top:3px}
.flow[data-mode="b"] .fl[data-i="1"],.flow[data-mode="b"] .fl[data-i="2"]{opacity:.32}
.flow[data-mode="b"] .fl[data-i="3"]{background:rgba(28,126,132,.3);border-color:var(--accent)}

/* опись: что собираем */
.chk{margin-top:14px}
.chk ul{display:grid;gap:8px}
.chk li{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:11px 13px;
  font-size:13.5px;color:var(--on-dark)}
.chk li:before{content:"";width:16px;height:16px;border-radius:4px;flex:none;
  border:1px solid var(--accent);background:rgba(28,126,132,.35)}

/* собрано по словам клиента */
.pf-known{background:rgba(28,126,132,.14);border:1px solid rgba(28,126,132,.45);
  border-radius:var(--r);padding:clamp(16px,2vw,24px)}
.pf-known .pf-eyebrow{color:#9FD4C4}
.pf-known ul{margin-top:12px;display:flex;flex-wrap:wrap;gap:7px}
.pf-known li{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);
  border-radius:999px;padding:6px 12px;font-size:13px;color:var(--on-dark)}
.pf-next{margin-top:14px;font-size:15px;color:#fff}

@media (max-width:1080px){
  .pf-l{position:static}
}

/* ===================================================== иллюстрация и моушн */
/* Иллюстрация направления: лёгкое дыхание и глубина от курсора. Это
   отвечает на присутствие человека, а не крутится само по себе. */
.ill{margin:0;width:100%}
.ill-img{border-radius:var(--r);overflow:hidden;background:var(--paper2);
  border:1px solid var(--line);box-shadow:0 40px 80px -46px rgba(15,23,34,.55);
  transform:translate3d(var(--dx,0),var(--dy,0),0);transition:transform .9s cubic-bezier(.25,.6,.25,1)}
.ill-img img{width:100%;display:block;aspect-ratio:3/2;object-fit:cover;
  animation:дыхание 14s ease-in-out infinite}
@keyframes дыхание{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-4px) scale(1.006)}}
.ill figcaption{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:14px;
  font-size:14px;color:var(--ink2)}
.ill figcaption .tag{background:rgba(255,255,255,.85);border:1px solid var(--line);
  padding:4px 9px;border-radius:999px}

/* ветвление: линии прорисовываются при появлении */
.tree-br:before{transform-origin:top;transform:scaleY(0);
  transition:transform .8s cubic-bezier(.25,.6,.25,1) .05s}
.br:before{transform-origin:top;transform:scaleY(0);
  transition:transform .7s cubic-bezier(.25,.6,.25,1)}
.pf-visual.seen .tree-br:before{transform:scaleY(1)}
.pf-visual.seen .br:before{transform:scaleY(1)}
.pf-visual.seen .br:nth-child(1):before{transition-delay:.26s}
.pf-visual.seen .br:nth-child(2):before{transition-delay:.34s}
.pf-visual.seen .br:nth-child(3):before{transition-delay:.42s}
.pf-visual .br,.pf-visual .tree-end,.pf-visual .fl,.pf-visual .chk li{
  opacity:0;transform:translateY(5px);
  transition:opacity .8s ease,transform .8s cubic-bezier(.25,.6,.25,1)}
.pf-visual.seen .br,.pf-visual.seen .tree-end,
.pf-visual.seen .fl,.pf-visual.seen .chk li{opacity:1;transform:none}
.pf-visual.seen .br:nth-child(1){transition-delay:.3s}
.pf-visual.seen .br:nth-child(2){transition-delay:.38s}
.pf-visual.seen .br:nth-child(3){transition-delay:.46s}
.pf-visual.seen .tree-end{transition-delay:.56s}
.pf-visual.seen .fl:nth-child(1){transition-delay:.06s}
.pf-visual.seen .fl:nth-child(2){transition-delay:.14s}
.pf-visual.seen .fl:nth-child(3){transition-delay:.22s}
.pf-visual.seen .fl:nth-child(4){transition-delay:.3s}
.pf-visual.seen .chk li:nth-child(1){transition-delay:.06s}
.pf-visual.seen .chk li:nth-child(2){transition-delay:.14s}
.pf-visual.seen .chk li:nth-child(3){transition-delay:.22s}

/* поток: после переключения по пути идёт сигнал */
.flow-l{position:relative}
.flow-l:after{content:"";position:absolute;left:0;top:50%;width:10px;height:10px;
  border-radius:50%;background:var(--accent);box-shadow:0 0 0 6px rgba(28,126,132,.22);
  opacity:0}
.flow[data-mode="b"] .flow-l:after{opacity:1;animation:сигнал 4.5s ease-in-out infinite}
@keyframes сигнал{0%{left:0;opacity:0}15%{opacity:.85}85%{opacity:.85}100%{left:calc(100% - 10px);opacity:0}}

@media (prefers-reduced-motion:reduce){
  .ill-img img{animation:none}
  .flow[data-mode="b"] .flow-l:after{animation:none;opacity:0}
  .pf-visual .br,.pf-visual .tree-end,.pf-visual .fl,.pf-visual .chk li{
    opacity:1!important;transform:none!important}
  .tree-br:before,.br:before{transform:scaleY(1)!important}
}
  opacity:1!important;transform:none!important}
.ill-wide{margin-top:14px;border-radius:14px;overflow:hidden;
  border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.05)}
.ill-wide img{width:100%;display:block;aspect-ratio:3/2;object-fit:cover}

/* ======================================================= единый тон и плавность */
/* 1. Фотография и трёхмерная сцена жили в разных мирах: снимок тёплый и
   контрастный, сцена — бледная. Приглушаем снимок и уводим его в тон бренда,
   чтобы они читались одной страницей. */
.hero-ph,.pf-ph,.fin-ph{filter:saturate(.72) contrast(1.02) brightness(1.02)}
.hero-ph .ph-l,.pf-ph .ph-l,.fin-ph .ph-l{position:absolute;inset:0;
  background-size:cover;background-position:center;opacity:0;
  transition:opacity 1.6s cubic-bezier(.25,.6,.25,1)}
.hero-ph .ph-l.on,.pf-ph .ph-l.on,.fin-ph .ph-l.on{opacity:1}
.pf-ph:before{content:"";position:absolute;inset:0;z-index:1;
  background:radial-gradient(120% 90% at 78% 40%,rgba(28,126,132,.22),transparent 60%)}

/* 2. Смена раздела и сцены больше не рывком: новое содержимое проявляется. */
@keyframes всплыть{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
@keyframes проявить{from{opacity:0}to{opacity:1}}
.pf-v{animation:всплыть .9s cubic-bezier(.25,.6,.25,1) both}
#hm-scene>*{animation:всплыть .8s cubic-bezier(.25,.6,.25,1) both}
.hm-step p{transition:opacity .45s ease}
.hm-step p.upd{opacity:0}
.m{animation:всплыть .45s cubic-bezier(.25,.6,.25,1) both}
.sugg button{animation:проявить .5s ease both}

/* 3. Полоса направлений: девять сцен вместо девяти слов. */
#layers{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px}
#layers button{display:flex;flex-direction:column;gap:0;padding:0;overflow:hidden;
  border-radius:14px;background:#fff;text-align:left}
#layers button .ly-ph{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;
  background:var(--paper2);transition:transform .5s cubic-bezier(.2,.7,.2,1)}
#layers button:hover .ly-ph{transform:scale(1.04)}
#layers button b{display:block;padding:12px 14px 6px;font-weight:600;font-size:15px}
#layers button span{display:block;padding:0 14px 14px;font-size:13px;color:var(--ink2)}
#layers button:hover{box-shadow:0 20px 40px -28px rgba(18,18,18,.5)}

/* 4. Финал: справа сцена, а не пустое поле. */
.fin-in{display:grid;grid-template-columns:minmax(0,54fr) minmax(0,46fr);
  gap:clamp(24px,3.4vw,64px);align-items:center}
.fin-l{min-width:0}
.fin-r{min-width:0}
.fin-ill{border-radius:var(--r);overflow:hidden;background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.14)}
.fin-ill img{width:100%;height:auto;display:block;aspect-ratio:3/2;object-fit:cover;
  transition:opacity .5s ease}
.fin-cap{margin-top:12px;font-size:13px;color:var(--on-dark2)}

/* 5. Границы в карточке работы — по запросу, а не стеной. */
.wk-body details{margin-top:10px}
.wk-body summary{cursor:pointer;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--ink3);list-style:none}
.wk-body summary::-webkit-details-marker{display:none}
.wk-body summary:after{content:" +";color:var(--ink3)}
.wk-body details[open] summary:after{content:" \\2212"}
.wk-body details p{margin-top:8px;font-size:14px;color:var(--ink2)}

@media (max-width:1080px){
  .fin-in{grid-template-columns:1fr}
}
@media (max-width:700px){
  #layers{grid-template-columns:1fr 1fr;gap:10px}
  #layers button b{font-size:14px;padding:10px 12px 4px}
  #layers button span{display:none}
}
@media (prefers-reduced-motion:reduce){
  .pf-v,#hm-scene>*,.m,.sugg button{animation:none}
  .hero-ph .ph-l,.pf-ph .ph-l,.fin-ph .ph-l{transition:none}
  #layers button .ly-ph{transition:none}
}

/* свёрнутые списки в полосе на телефоне */
.pf-two-d{margin-top:16px;border-top:1px solid var(--line);padding-top:12px}
.pf-two-d>summary{cursor:pointer;list-style:none;font-family:var(--mono);font-size:10px;
  letter-spacing:.16em;text-transform:uppercase;color:var(--ink3)}
.pf-two-d>summary::-webkit-details-marker{display:none}
.pf-two-d>summary:after{content:" +";color:var(--ink3)}
.pf-two-d[open]>summary:after{content:" \\2212"}
.pf-two-d .pf-two{margin-top:12px;padding-top:0;border-top:0}

/* ============================================== смена без рывка */
/* Сцена первого экрана: старая гаснет, новая проявляется на её месте. */
#hm-scene{position:relative}
#hm-scene>.уходит{opacity:1;transition:opacity .6s ease}
#hm-scene>.сц-новая{position:absolute;inset:0;opacity:0;
  transition:opacity .6s ease}
#hm-scene>.сц-новая.on{opacity:1}
#hm-scene>.сц-новая~.уходит,#hm-scene>.уходит{opacity:.001}
#hm-scene>.сц-новая>*{animation:none}

/* Полоса под задачу: высоту ведём плавно, поэтому содержимое не прыгает.
   Обрезаем только на время перехода — иначе карточка не помещается. */
.pf-in.ведём{overflow:hidden}

/* Сетка направлений остаётся на месте: выбранное помечено, остальные тише. */
#layers[data-picked] button{opacity:.45;transition:opacity .7s ease,
  box-shadow .5s ease,transform .5s ease}
#layers[data-picked] button[aria-pressed="true"]{opacity:1;
  box-shadow:0 0 0 2px var(--accent),0 24px 44px -30px rgba(18,18,18,.55)}
#layers[data-picked] button:hover{opacity:.85}
#layers-picked{margin-top:18px}

/* Высоты, которые раньше не совпадали между состояниями */
/* Сцена первого экрана: один и тот же размер и под иллюстрацию, и под снимок
   работы, и под схему — иначе первый экран прыгает при смене задачи. */
#hm-scene{min-height:clamp(300px,34vw,440px)}
#hm-scene>*{height:100%}
.ill,.shot,.scheme{height:100%;display:flex;flex-direction:column}
.ill-img,.shot-win{flex:1;min-height:0}
.ill-img img,.shot-win img{height:100%;object-fit:cover}
.scheme{overflow:auto}
/* Карточка работы: одинаковая высота на компьютере и телефоне в обоих режимах */
.wk-card{min-height:clamp(380px,30vw,460px)}
@media (max-width:1080px){
  #hm-scene{min-height:300px}
}
@media (max-width:700px){
  #hm-scene{min-height:240px}
  .stream{min-height:118px}
}

.stream:empty:before{content:attr(data-hint);display:block;margin:auto 0 2px;
  font-size:14.5px;color:var(--ink3);line-height:1.5;max-width:30ch}

/* Карточка работы: один размер в обоих режимах, иначе две карточки в ряду
   расходятся по высоте, а при переключении устройства страница прыгает. */
.wk-card{height:clamp(380px,30vw,460px);min-height:0}
.wk-inset{max-height:64%;margin-top:auto}
.wk-inset img{height:100%;object-fit:cover;object-position:top}
.wk[data-dev="d"] .wk-inset{width:min(100%,330px)}
.wk[data-dev="d"] .wk-inset img{aspect-ratio:auto}
.wk[data-dev="p"] .wk-inset{width:min(46%,190px)}
.wk[data-dev="p"] .wk-inset img{aspect-ratio:auto}
@media (max-width:700px){
  .wk-card{height:clamp(320px,72vw,400px)}
}

/* ============================================ сайты, которые мы собрали */
.band-clients{padding:clamp(48px,6vw,86px) 0;background:var(--paper)}
.band-clients h2{font-size:clamp(26px,3vw,42px);margin-top:14px;max-width:20ch}
.cl-lede{margin-top:14px;color:var(--ink2);max-width:58ch;font-size:16px}
.cl-grid{margin-top:clamp(24px,3vw,40px);display:grid;
  grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:clamp(14px,1.6vw,22px)}
.cl{text-decoration:none;display:block}
.cl-shot{display:block;border-radius:14px;overflow:hidden;border:1px solid var(--line);
  background:var(--paper2)}
.cl-shot img{width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;object-position:top;
  transition:transform .8s cubic-bezier(.25,.6,.25,1)}
.cl:hover .cl-shot img{transform:scale(1.03)}
.cl-nm{display:flex;align-items:center;gap:6px;margin-top:10px;font-size:14.5px;
  font-weight:500}
.cl-nm i{font-style:normal;color:var(--ink3);font-size:12px}
.cl:hover .cl-nm{color:var(--accent2)}
@media (max-width:700px){
  .cl-grid{grid-template-columns:1fr 1fr;gap:12px}
  .cl-nm{font-size:13px}
}
"""


СВОЁ_РАБОТЫ = {'ru': {'eyebrow': 'Работы студии',
        'h': 'Два концепта, которые можно открыть и потрогать',
        'lede': 'Это наши собственные сборки, а не заказы клиентов. Поэтому их можно показывать '
                'целиком — и поэтому мы не приписываем им чужих результатов.',
        'desk': 'Компьютер',
        'phone': 'Телефон',
        'work': 'Что это за работа',
        'layers_lede': 'Помогаем решить разные задачи бизнеса и соединить их в понятный '
                       'следующий шаг.',
        'trust_role': 'Основатель, Prodigy LAB',
        'scan_line': 'Есть сайт? Бесплатная AI-проверка одной страницы — без доступов и без '
                     'звонка.',
        'scan_cta': 'Проверить сайт',
        'nav_solutions': 'Решения',
        'nav_works': 'Работы',
        'nav_about': 'О нас'},
 'en': {'eyebrow': 'Studio work',
        'h': 'Two concepts you can open and use',
        'lede': 'These are our own builds, not client orders. That is why we can show them in '
                'full — and why we do not attach anyone else’s results to them.',
        'desk': 'Desktop',
        'phone': 'Phone',
        'work': 'About this work',
        'layers_lede': 'We work through different business problems and connect them into one '
                       'clear next step.',
        'trust_role': 'Founder, Prodigy LAB',
        'scan_line': 'Have a site? A free AI check of one page — no access, no call.',
        'scan_cta': 'Check the site',
        'nav_solutions': 'Solutions',
        'nav_works': 'Work',
        'nav_about': 'About'},
 'es': {'eyebrow': 'Trabajo del estudio',
        'h': 'Dos conceptos que puede abrir y usar',
        'lede': 'Son construcciones propias, no encargos de clientes. Por eso podemos mostrarlas '
                'enteras y por eso no les atribuimos resultados ajenos.',
        'desk': 'Ordenador',
        'phone': 'Móvil',
        'work': 'Sobre este trabajo',
        'layers_lede': 'Resolvemos distintas tareas del negocio y las unimos en un siguiente '
                       'paso claro.',
        'trust_role': 'Fundador, Prodigy LAB',
        'scan_line': '¿Tiene sitio web? Revisión AI gratuita de una página: sin accesos y sin '
                     'llamada.',
        'scan_cta': 'Revisar el sitio',
        'nav_solutions': 'Soluciones',
        'nav_works': 'Trabajos',
        'nav_about': 'Nosotros'},
 'pt': {'eyebrow': 'Trabalho do estúdio',
        'h': 'Dois conceitos que você pode abrir e usar',
        'lede': 'São construções nossas, não pedidos de clientes. Por isso podemos mostrá-las '
                'inteiras e por isso não atribuímos a elas resultados alheios.',
        'desk': 'Computador',
        'phone': 'Celular',
        'work': 'Sobre este trabalho',
        'layers_lede': 'Resolvemos diferentes tarefas do negócio e as unimos em um próximo passo '
                       'claro.',
        'trust_role': 'Fundador, Prodigy LAB',
        'scan_line': 'Tem site? Verificação AI gratuita de uma página — sem acessos e sem '
                     'ligação.',
        'scan_cta': 'Verificar o site',
        'nav_solutions': 'Soluções',
        'nav_works': 'Trabalhos',
        'nav_about': 'Sobre nós'},
 'de': {'eyebrow': 'Studio-Arbeit',
        'h': 'Zwei Konzepte, die Sie öffnen und benutzen können',
        'lede': 'Das sind eigene Arbeiten, keine Kundenaufträge. Deshalb können wir sie ganz '
                'zeigen — und deshalb schreiben wir ihnen keine fremden Ergebnisse zu.',
        'desk': 'Computer',
        'phone': 'Telefon',
        'work': 'Über diese Arbeit',
        'layers_lede': 'Wir arbeiten verschiedene Aufgaben des Geschäfts durch und führen sie zu '
                       'einem klaren nächsten Schritt zusammen.',
        'trust_role': 'Gründer, Prodigy LAB',
        'scan_line': 'Website vorhanden? Kostenlose AI-Prüfung einer Seite — ohne Zugänge, ohne '
                     'Anruf.',
        'scan_cta': 'Website prüfen',
        'nav_solutions': 'Lösungen',
        'nav_works': 'Arbeiten',
        'nav_about': 'Über uns'}}


# Работы студии: два отобранных концепта. Тексты — те же, что на страницах
# работ; результатов здесь нет и не будет, пока их нечем подтвердить.
РАБОТЫ_ФОТО = {'neighborhood-fence': ('fence-1', 'fence'),
               'saeng-thai-house': ('food-1', 'thai')}


def кратко(текст: str) -> str:
    """Первое предложение целиком: подпись на карточке короткая, полный
    разбор остаётся на странице работы."""
    т = текст.strip()
    for i, ch in enumerate(т):
        if ch in '.!?' and i > 50 and (i + 1 >= len(т) or т[i + 1] == ' '):
            return т[:i + 1]
    return т


def блок_клиентов(code: str) -> str:
    """Сайты, которые мы собрали и ведём.

    Здесь только снимок, имя и ссылка: подтверждённых формулировок вклада
    по каждому проекту у нас нет, и приписывать результаты мы не будем.
    """
    import html as _h
    e = _h.escape
    d = L[code]
    карточки = "".join(
        f'<a class="cl" href="{u}" target="_blank" rel="noopener">'
        f'<span class="cl-shot"><img src="{i}" alt="{e(n)} \u2014 {e(d["cases_alt"])}" '
        f'width="600" height="600" loading="lazy" decoding="async"></span>'
        f'<span class="cl-nm">{e(n)}<i>&#8599;</i></span></a>'
        for n, u, i in CLIENTS)
    return (f'<section class="band-clients" id="clients"><div class="wrap">'
            f'<p class="eyebrow">{e(d["cases_eyebrow"])}</p>'
            f'<h2>{e(d["cases_h2"])}</h2>'
            f'<p class="cl-lede">{e(d["cases_lede"])}</p>'
            f'<div class="cl-grid">{карточки}</div></div></section>')


def блок_работ(code: str) -> str:
    import json as _json
    import os as _os
    import html as _h
    import build_work as BW
    e = _h.escape
    каталог = {i['slug']: i for i in _json.load(
        open(_os.path.join(КОРЕНЬ, 'SHOWCASE.json'), encoding='utf-8'))['items']}
    П = BW.ПОДПИСИ[code]
    С = СВОЁ_РАБОТЫ[code]
    карточки = []
    for slug in ('neighborhood-fence', 'saeng-thai-house'):
        if slug not in BW.ТЕКСТЫ or slug not in каталог:
            continue
        t = BW.ТЕКСТЫ[slug][code]
        фото, снимок = РАБОТЫ_ФОТО[slug]
        наз = каталог[slug]['title'][code]
        карточки.append(
            f'<article class="wk" data-dev="d">'
            f'<div class="wk-card" style="background-image:url(/assets/ph/{фото}.jpg)">'
            f'<div class="wk-top"><span class="wk-name">{e(наз)}</span>'
            f'<span class="wk-tag">{e(П["concept"])}</span></div>'
            f'<div class="wk-inset"><img src="/assets/demo/{снимок}-desk.jpg" '
            f'data-desk="/assets/demo/{снимок}-desk.jpg" '
            f'data-phone="/assets/demo/{снимок}-phone.jpg" alt="{e(наз)}" '
            f'width="1400" height="972" loading="lazy" decoding="async"></div>'
            f'<div class="wk-dev">'
            f'<button type="button" data-dev="d" aria-pressed="true">{e(С["desk"])}</button>'
            f'<button type="button" data-dev="p" aria-pressed="false">{e(С["phone"])}</button>'
            f'</div></div>'
            f'<div class="wk-body"><dl>'
            f'<dt>{e(П["task"])}</dt><dd>{e(кратко(t["task"]))}</dd>'
            f'<dt>{e(П["done"])}</dt><dd>{e(кратко(t["done"]))}</dd>'
            f'</dl>'
            f'<details><summary>{e(П["limits"])}</summary>'
            f'<p>{e(t["limits"])}</p></details>'
            f'<div class="wk-links">'
            f'<a class="wk-go" href="/preview/{slug}/">{e(П["demo"])} &rarr;</a>'
            f'<a class="wk-sec" href="{BW.ПУТЬ[code]}{slug}/">{e(С["work"])}</a>'
            f'</div></div></article>')
    if not карточки:
        return ''
    return (f'<section id="works" class="band-works">'
            f'<div class="wk-h"><p class="eyebrow">{e(С["eyebrow"])}</p>'
            f'<h2>{e(С["h"])}</h2><p>{e(С["lede"])}</p></div>'
            f'<div class="wk-grid">{"".join(карточки)}</div></section>')


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

# Третьим идёт снимок самого сайта. Это настоящие кадры их витрин, снятые с
# живых страниц, а не стоковые картинки: блок называется «Доказательства», и
# подставлять туда выдуманное было бы странно.
CLIENTS = (("HealthHustle Academy", "https://healthhustleacademy.com", "/cases/hha.jpg"),
           ("Set4Pets", "https://set4pets.com", "/cases/set4pets.jpg"),
           ("Petalia", "https://petaliashop.com", "/cases/petalia.jpg"),
           ("KONDRA", "https://kondrabags.com", "/cases/kondra.jpg"),
           ("Nixe Beauty", "https://nixe.beauty", "/cases/nixe.jpg"),
           ("Sasha Gun Photography", "https://sashagun.com", "/cases/sashagun.jpg"))

WA_SVG = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
 'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
 '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-3.9-.9L3 20.5l1.6-4.7A8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/>'
 '</svg>')

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
/* Языки видны на любой ширине: спрятанные в бургер, они не давали понять,
   что у сайта вообще есть другие языки. */
.langs{display:flex;gap:0;margin-right:4px}
.langs a{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.08em;color:var(--ink3);
text-decoration:none;padding:8px 4px}
@media(min-width:600px){.langs{gap:2px;margin-right:6px}.langs a{padding:8px 6px;letter-spacing:.1em}}
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
.hero h1,.hero .h1-like{max-width:19ch;margin:20px auto 0}
/* Пониженный заголовок главной: он идёт вторым после первого
   экрана, поэтому крупнее подзаголовка, но меньше h1. На других
   страницах с этим CSS заголовок остаётся прежним. */
.hero .h1-like{font-size:clamp(26px,4.4vw,44px);letter-spacing:-.03em;line-height:1.1}
/* Короткий блок доверия: лицо, компетенции и настоящие работы рядом, без
   длинного оправдания на половину экрана. */
.who2{display:grid;gap:30px;margin-top:22px;text-align:left}
@media(min-width:860px){.who2{grid-template-columns:1.35fr 1fr;gap:1px;
 background:var(--line);border:1px solid var(--line)}
 .who2>div{background:var(--paper2);padding:30px 28px 34px}}
.who2-mark{display:block;width:84px;height:auto;margin:0 0 20px}
@media(min-width:860px){.who2-mark{width:96px}}
.who2 h2{font-size:clamp(24px,3.2vw,36px)}
.fin-state{margin-top:22px;font-size:15.5px;color:var(--ink2)}
.fin-state[hidden]{display:none}
/* Закреплённая кнопка проверки сайта не висит над полем помощника и не
   предлагается тому, чья задача не про сайт. */
.hm-on #sn-sticky,#sn-sticky[data-off="1"]{display:none!important}
.quote{font-size:15.5px;font-style:italic;color:var(--accent);margin:22px auto 0;max-width:40ch}
.hero .lede{max-width:56ch;margin:22px auto 0}
.cta-row{display:flex;flex-direction:column;gap:11px;margin:34px auto 0;max-width:520px}
@media(min-width:560px){.cta-row{flex-direction:row;justify-content:center}}
.hero .mono{margin-top:20px;display:block}
.pl-adapt-pending .hero h1,.pl-adapt-pending .hero .h1-like,.pl-adapt-pending .hero .lede,.pl-adapt-pending .hero .quote,.pl-adapt-pending .hero .mono{visibility:hidden}
.hero.picked h1,.hero.picked .h1-like{max-width:22ch}
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
.cell h3 a{color:inherit;text-decoration:none}
.cell h3 .nb{white-space:nowrap}
/* Карточка, поднятая наверх под намерение посетителя. Метка без слов —
   иначе пришлось бы придумывать и переводить текст на пять языков. */
.cell.pick{position:relative}
.cell.pick:before{content:"";position:absolute;left:-14px;top:26px;bottom:26px;
 width:2px;background:var(--accent)}
@media(max-width:699px){.cell.pick:before{left:-10px}}
.cell h3 a .go{color:var(--accent);opacity:.45;margin-left:2px;display:inline-block;transition:opacity .15s ease,transform .15s ease}
.cell[data-cell]:hover h3 a .go{opacity:1;transform:translateX(3px)}
.cell h3 a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
@media(hover:hover){.cell[data-cell]{cursor:pointer}}
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
.band{margin-top:46px;border:1px solid var(--line);overflow:hidden;background:#0d0f10}
.band img{display:block;width:100%;height:auto;aspect-ratio:16/7;object-fit:cover;opacity:.92}
@media(max-width:699px){.band{margin-top:34px}.band img{aspect-ratio:16/9}}
.cases{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:30px}
@media(min-width:700px){.cases{grid-template-columns:repeat(3,1fr);gap:18px}}
.case{display:block;text-decoration:none;color:inherit}
.case .shot{display:block;overflow:hidden;border:1px solid var(--line);background:var(--surface)}
.case .shot img{display:block;width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;
 object-position:top center;transition:transform .5s cubic-bezier(.2,.6,.2,1)}
.case:hover .shot img{transform:scale(1.03)}
.case .nm{display:flex;align-items:center;gap:6px;margin-top:10px;font-size:14.5px;color:var(--ink)}
.case .nm i{font-style:normal;color:var(--accent);opacity:.5;transition:opacity .15s,transform .15s}
.case:hover .nm i{opacity:1;transform:translate(2px,-2px)}
.cases-old a{font-size:16px;color:var(--accent);text-decoration:none;padding:6px 0;
border-bottom:1px solid transparent}
.cases-old a:hover{border-bottom-color:var(--accent)}
.final{padding:66px 0 76px}@media(min-width:768px){.final{padding:100px 0 118px}}
.final h2{max-width:22ch}.final .lede{max-width:56ch;margin-top:18px}
.final .cta-row{margin-left:0;justify-content:flex-start}
footer{border-top:1px solid var(--line);padding:46px 0 56px}
.flinks{display:flex;flex-wrap:wrap;gap:4px 26px;margin:22px 0 24px}
.flinks a{font-size:14px;color:var(--ink2);text-decoration:none;padding:8px 0}
.flinks a:hover{color:var(--accent)}
.fmeta{font-size:12.5px;color:var(--ink3);line-height:1.75}
/* Плашка языка — строка в потоке над первым экраном, а не чёрная панель
   поверх поля ввода. На телефоне она перекрывала главное действие. */
#langbar{display:none;background:var(--paper2);color:var(--ink);
border-bottom:1px solid var(--line);padding:10px 0}
#langbar.on{display:block}
.lb-in{display:flex;align-items:center;gap:14px;flex-wrap:wrap;justify-content:space-between}
.lb-t{font-size:15px;line-height:1.45;flex:1 1 260px}
.lb-b{display:flex;gap:8px;flex:none}
.lb-b button{font-family:inherit;font-size:14px;padding:11px 18px;min-height:44px;cursor:pointer;
border:1px solid #fff;background:#fff;color:var(--ink)}
.lb-b button.ghost{background:transparent;color:#fff}
.lb-b button:hover{opacity:.85}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

def page(code):
    d = L[code]
    # Галерея примеров. Импорт здесь, а не наверху: build_showcase импортирует
    # этот модуль ради CSS и шапки — на верхнем уровне получилось бы кольцо.
    from build_showcase import блок_для_главной, EXTRA_CSS as SHOWCASE_CSS, PAGE_PATH as SHOWCASE_PATH
    import scan_block as SB
    # Первый экран с помощником. Импорт здесь же, рядом с остальными блоками
    # страницы: наверху он тянул бы за собой содержимое пяти языков всегда,
    # даже когда собирается не главная.
    import hero_motion as HM
    import hero_sections as HS
    hero_block = HM.markup(code)
    # Разделы под задачу идут сразу за разговором: человек, ответивший на
    # пару вопросов, листает вниз и видит путь по своей задаче, а не общий
    # перечень услуг.
    pf_block = HS.markup(code)
    hero_js = HM.script(code)
    hero_css = HM.встроенный_css()
    scan_nav = SB.nav_button(code)
    scan_main = SB.main_block(code)
    scan_after = SB.after_gallery(code)
    scan_sticky = SB.sticky(code)
    scan_hero = (f'<a class="btn btn-lg" href="{SB.scan_url(code, "hero")}">'
                 f'{SB.S[code]["cta"]} &rarr;</a>')
    works_block = блок_работ(code)
    clients_block = блок_клиентов(code)
    С = СВОЁ_РАБОТЫ[code]
    # В блоке доверия три факта из шести: остальные уводят в юридический текст.
    facts_short = "".join(
        f'<div><dt>{H.escape(k)}</dt><dd>{H.escape(v)}</dd></div>'
        for k, v in d['facts'][1:4])
    showcase = блок_для_главной(code)
    showcase_nav = SHOWCASE_PATH[code]
    url = ORIGIN + d['home']
    scan = SCAN + d['scan_lang']
    diag = DIAG + d['scan_lang']
    e = H.escape
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{c}" href="{ORIGIN}{L[c]["home"]}">' for c, _ in LANGNAMES
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'
    import json as _js
    lang_names_js = _js.dumps(list(d['lang_names']), ensure_ascii=False)
    banner_ask_js = _js.dumps(d['banner_ask'], ensure_ascii=False)
    banner_open_js = _js.dumps(d['banner_open'], ensure_ascii=False)
    banner_stay_js = _js.dumps(d['banner_stay'], ensure_ascii=False)
    clients = "".join(
        f'<a class="case" href="{u}" target="_blank" rel="noopener">'
        f'<span class="shot"><img src="{i}" alt="{e(n)} \u2014 {e(d["cases_alt"])}" '
        f'loading="lazy" width="600" height="600"></span>'
        f'<span class="nm">{n}<i>&#8599;</i></span></a>' for n, u, i in CLIENTS)
    langs = "".join(
        f'<a href="{L[c]["home"]}"{" aria-current=\"page\"" if c == code else ""}>{n}</a>'
        for c, n in LANGNAMES)
    navmid = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in d['nav'])
    # Пункт меню появляется только когда в галерее есть что показать:
    # вести в пустой раздел хуже, чем не вести вовсе.
    from showcase_content import S as _SC
    _имя = _SC[code]['nav']
    _ссылка = f'<a href="{showcase_nav}">{e(_имя)}</a>' if showcase else ''
    showcase_link = _ссылка
    showcase_foot = _ссылка
    showcase_mob = (f'<a class="ml" href="{showcase_nav}">{e(_имя)}</a>'
                    if showcase else '')
    mobls = "".join(f'<a class="ml" href="{h}">{e(t)}</a>' for h, t in d['nav'])
    def _cell(i, tag, h3, p, lis):
        extra = ''
        # §10: AI-проверка сайта остаётся, но как вторичный путь внутри
        # категории «Сайт и e-commerce», а не как главный CTA страницы
        if i == 8:
            extra = (f'<p style="margin-top:14px"><a href="{scan}" target="_blank" rel="noopener" '
                     f'style="font-size:14px;color:var(--accent);text-decoration:none;'
                     f'border-bottom:1px solid var(--accent)">{e(d["scan_secondary"])} &rarr;</a></p>')
        # Карточка ведёт в анкету с гипотезой о направлении. Ссылка живёт на
        # заголовке, а не на всей карточке: внутри девятой уже есть ссылка на
        # скан, а вложенные <a> — невалидная разметка, которую браузер ломает.
        # Клик по остальной площади добирается скриптом, поэтому без JS
        # карточка всё равно остаётся рабочей ссылкой.
        слой = LAYER_BY_INDEX[i] if i < len(LAYER_BY_INDEX) else ''
        if слой:
            ссылка = f'{diag}&amp;initial_hypothesis={слой}'
            подпись = f' data-cell data-layer="{слой}"'
            стрелка = '<span class="go" aria-hidden="true">&rarr;</span>'
            части = e(h3).rsplit(' ', 1)
            если_длинный = (f'{части[0]} <span class="nb">{части[1]}&nbsp;{стрелка}</span>'
                            if len(части) == 2 else f'{e(h3)}&nbsp;{стрелка}')
            заголовок = f'<h3><a href="{ссылка}" data-diag>{если_длинный}</a></h3>'
        else:
            подпись = ''
            заголовок = f'<h3>{e(h3)}</h3>'
        return (f'<div class="cell"{подпись}><span class="mono">{e(tag)}</span>{заголовок}'
                f'<p>{e(p)}</p>'
                f'<ul>{"".join(f"<li>{e(li)}</li>" for li in lis)}</ul>{extra}</div>')
    # Девять направлений в порядке содержимого ложатся на направления
    # routing один к одному. Клик — то же самое действие выбора, что и чип.
    СЛОИ = ("payments", "banking", "funding", "growth", "operations",
            "infrastructure", "accounting", "fulfillment", "presence")
    # У каждого направления своя сцена: девять слов на пустом поле ничего не
    # объясняли, а картинка показывает, о чём речь, на любом языке.
    слои = "".join(
        f'<button type="button" data-layer="{СЛОИ[i]}">'
        f'<img class="ly-ph" src="/assets/il/{СЛОИ[i]}.jpg" alt="" '
        f'width="1200" height="800" loading="lazy" decoding="async">'
        f'<b>{e(название.split(chr(8212))[-1].strip())}</b>'
        f'<span>{e(боль)}</span></button>'
        for i, (название, боль, _о, _п) in enumerate(d['problems']))
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
<style>{CSS}{SHOWCASE_CSS}{SB.CSS}{НОВОЕ_CSS}</style>
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
<script>/* Визит с меткой: прячем текст героя до решения, максимум 1.5 с, чтобы не мигал. */
(function(){{try{{if(/[?&](initial_hypothesis|content_id|outreach_id|utm_campaign)=/.test(location.search)){{
var h=document.documentElement;h.classList.add("pl-adapt-pending");
setTimeout(function(){{h.classList.remove("pl-adapt-pending")}},1500);}}}}catch(e){{}}}})();</script>
</head>
<body>

<nav>
 <div class="wrap nav-in">
  <a class="brand" href="{d['home']}"><b>PRODIGY</b><span>LAB</span></a>
  <div class="nav-mid">{navmid}{showcase_link}</div>
  <div class="nav-right">
   <div class="langs">{langs}</div>
   <a class="icon" href="{WA}" target="_blank" rel="noopener"
      aria-label="{e(d['wa_label'])} {PHONE_TEXT}" title="{e(d['wa_label'])}">{WA_SVG}</a>
   <button id="burger" class="icon" aria-label="Menu" aria-expanded="false" onclick="tg(this)">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 7h18M3 12h18M3 17h18"/></svg>
   </button>
   <a class="btn nav-cta" href="#start">{e(d['cta1'])}</a>
  </div>
 </div>
 <div id="mob"><div class="wrap">{mobls}{showcase_mob}
  <a class="btn" href="#start">{e(d['cta1'])}</a>
  <a class="ml" href="{WA}" target="_blank" rel="noopener">{e(d['wa_label'])} {PHONE_TEXT}</a>
  <div class="mlangs">{langs}</div>
 </div></div>
</nav>

<div id="langbar" role="region" aria-live="polite"><div class="wrap lb-in">
 <span class="lb-t" id="lb-text"></span>
 <span class="lb-b">
  <button id="lb-go"></button>
  <button id="lb-no" class="ghost"></button>
 </span>
</div></div>

<main>
{hero_block}

{pf_block}

{works_block}

{clients_block}

<section class="band-layers" id="problems">
 <div class="wrap">
  <div class="lay-h">
   <h2 id="lay-title">{e(d['s1_h2'])}</h2>
   <p id="lay-lede">{e(С['layers_lede'])}</p>
  </div>
  <div id="layers">{слои}</div>
  <div id="layers-picked" hidden>
   <span id="layers-name"></span>
   <button type="button" id="layers-change">{e(HS.ОБЩЕЕ[code].get('change', ''))}</button>
  </div>
 </div>
</section>

<section class="band-who" id="who">
 <div class="who">
  <img class="who-face" src="/assets/founder.jpg" alt="{e(d['photo_alt'])}"
       width="192" height="192" loading="lazy" decoding="async">
  <div>
   <p class="who-role">{e(С['trust_role'])}</p>
   <h2>{e(d['s3_h2'])}</h2>
   <p>{e(d['s3_p1'])}</p>
   <dl class="facts">{facts_short}</dl>
  </div>
 </div>
</section>

<section class="band-final" id="diagnostic">
 <div class="fin-ph" id="fin-ph"></div>
 <div class="fin-in">
  <div class="fin-l">
   <p class="eyebrow">{e(d['final_eyebrow'])}</p>
   <h2>{e(d['final_h2'])}</h2>
   <p class="lede">{e(d['final_lede'])}</p>
   <div class="fin-row">
    <button type="button" id="fin-talk">{e(HS.ОБЩЕЕ[code]['talk'])}</button>
    <a class="fin-alt" href="{WA}" target="_blank" rel="noopener">{e(d['final_cta2'])}</a>
   </div>
   <p id="fin-state" hidden></p>
   <div class="fin-scan">
    <p>{e(С['scan_line'])}</p>
    <a href="{scan}" target="_blank" rel="noopener">{e(С['scan_cta'])} &rarr;</a>
   </div>
  </div>
  <div class="fin-r">
   <div class="fin-ill"><img id="fin-ill" src="/assets/il/neutral.jpg" alt=""
        width="1200" height="800" loading="lazy" decoding="async"></div>
  </div>
 </div>
</section>
</main>


{scan_sticky}
<footer>
 <div class="wrap">
  <a class="brand" href="{d['home']}"><b>PRODIGY</b><span>LAB</span></a>
  <div class="flinks">
   {"".join(f'<a href="{h}">{e(t)}</a>' for h,t in d['nav'])}{showcase_foot}
   <a href="{WA}" target="_blank" rel="noopener">{PHONE_TEXT}</a>
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
{SB.STICKY_JS}
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
// Идентификатор сессии (§19). Один на визит, живёт только в этой вкладке и
// уезжает в анкету ссылкой: домены разные, sessionStorage через границу не
// переносится. Персональных данных здесь нет — это случайная строка.
var PL_SID=(function(){{
 try{{var v=sessionStorage.getItem('pl_sid');
  if(v) return v;
  v='w'+Date.now().toString(36)+Math.random().toString(36).slice(2,10);
  sessionStorage.setItem('pl_sid',v); return v;}}
 catch(e){{return 'w'+Date.now().toString(36);}}}})();
// UTM и реферер прокидываем в диагностику, иначе источник заявки теряется (ТЗ §8)
(function(){{var q=new URLSearchParams(location.search);
 document.querySelectorAll('a[data-diag]').forEach(function(a){{
  var u=new URL(a.href);
  ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid','gclid'].forEach(function(k){{
   if(q.get(k)) u.searchParams.set(k,q.get(k));}});
  // content_id и outreach_id — гипотеза о проблеме из ролика или письма (§20, §21).
  ['content_id','outreach_id'].forEach(function(k){{
   if(q.get(k)) u.searchParams.set(k,q.get(k).slice(0,240));}});
  u.searchParams.set('sid', PL_SID);
  u.searchParams.set('from', location.pathname);
  if(document.referrer) u.searchParams.set('ref', document.referrer.slice(0,200));
  a.href=u.toString();
  a.addEventListener('click',function(){{
   plEvent('localized_cta_clicked',{{destination:'diagnostic',
    problem_category:a.closest('[data-layer]')?a.closest('[data-layer]').dataset.layer:''}});
  }});}});}})();
// Клик по всей карточке направления. Заголовок — настоящая ссылка, так что без
// скрипта всё работает; это только удобство, особенно на телефоне.
document.querySelectorAll('.cell[data-cell]').forEach(function(c){{
 c.addEventListener('click',function(ev){{
  if(ev.target.closest('a')) return;
  var a=c.querySelector('h3 a'); if(a) a.click();}});}});
// --- Адаптация главной под намерение. Правила отвечают первыми, Jev зовут
// только когда правил не хватило, и выбирает он из тех же девяти направлений.
// Тексты всех карточек написаны заранее — сочинить свою он не может.
// Молчание — штатный исход: холодному заходу без меток адаптировать нечего.
(function(){{
 var SIG='pl_signals_v1';
 function сигналы(){{try{{return JSON.parse(sessionStorage.getItem(SIG)||'[]');}}catch(e){{return [];}}}}
 function запомнить(слой){{
  try{{var a=сигналы(),k='opened_'+слой;
   if(a.indexOf(k)<0){{a.push(k);sessionStorage.setItem(SIG,JSON.stringify(a.slice(-8)));}}}}catch(e){{}}
 }}
 document.querySelectorAll('.cell[data-layer]').forEach(function(c){{
  c.addEventListener('click',function(){{запомнить(c.dataset.layer);}});}});

 var q=new URLSearchParams(location.search);
 var тело=JSON.stringify({{
  session_id:PL_SID, landing:location.pathname, lang:"{code}",
  content_id:q.get('content_id')||'', outreach_id:q.get('outreach_id')||'',
  explicit_layer:q.get('initial_hypothesis')||'',
  referrer:document.referrer||'', signals:сигналы(),
  utm:{{utm_source:q.get('utm_source')||'',utm_medium:q.get('utm_medium')||'',
       utm_campaign:q.get('utm_campaign')||'',utm_content:q.get('utm_content')||'',
       utm_term:q.get('utm_term')||''}}
 }});
 // Если человек уже доскроллил до блока проблем, переставлять поздно: он
 // читает, и карточки прыгнут под рукой. Тогда просто ничего не делаем.
 function можноПереставлять(){{
  var s=document.getElementById('problems');
  return s && s.getBoundingClientRect().top > 80;
 }}
 var отмена=setTimeout(function(){{отмена=null;}},1500);

 function отпустить(){{document.documentElement.classList.remove('pl-adapt-pending');}}
 // Первый экран под намерение. Текст и ссылку берём из уже утверждённой
 // карточки этого направления — свой текст здесь не появляется никогда.
 // Если человек уже ушёл ниже героя, не трогаем: менять видимое под рукой нельзя.
 function героем(слой){{
  var карта=document.querySelector('.cell[data-layer="'+слой+'"]');
  var г=document.getElementById('hero');
  if(!карта||!г||window.scrollY>120) return;
  var h=карта.querySelector('h3 a'), p=карта.querySelector('p'), м=карта.querySelector('.mono');
  if(!h||!p) return;
  var заголовок=h.textContent.replace(/[\u2192\s]+$/,'').trim();
  var g1=г.querySelector('h1, .h1-like'), lede=г.querySelector('.lede'), q=г.querySelector('.quote');
  var бровь=г.querySelector('.wrap > .mono');
  if(g1) g1.textContent=заголовок;
  if(lede) lede.textContent=p.textContent;
  if(q) q.style.display='none';
  if(бровь&&м) бровь.textContent=м.textContent.split('—').slice(1).join('—').trim()||м.textContent;
  var cta=г.querySelector('.cta-row a[data-diag]');
  if(cta) cta.href=h.href;
  var вторая=г.querySelector('.cta-row a.btn-g');
  if(вторая) вторая.setAttribute('href','#problems');
  г.classList.add('picked');
 }}
 fetch("{DECIDE}",{{method:'POST',body:тело,headers:{{'Content-Type':'text/plain;charset=UTF-8'}}}})
  .then(function(r){{return r.ok?r.json():null;}})
  .then(function(d){{
   if(d&&d.layer&&отмена!==null) героем(d.layer);
   отпустить();
   if(!d||!d.layer||отмена===null||!можноПереставлять()) return;
   var карта=document.querySelector('.cell[data-layer="'+d.layer+'"]');
   var сетка=карта&&карта.parentNode;
   if(!карта||!сетка||сетка.firstElementChild===карта) return;
   сетка.insertBefore(карта,сетка.firstElementChild);
   карта.classList.add('pick');
   var метка=карта.querySelector('.mono');
   if(метка && метка.textContent.indexOf('—')>0){{
    метка.textContent=метка.textContent.split('—').slice(1).join('—').trim();}}
   plEvent('homepage_adapted',{{problem_category:d.layer,decision_source:d.source,
    decision_confidence:d.confidence}});
  }})
  .catch(отпустить);
}})();
document.querySelectorAll('.langs a,.mlangs a').forEach(function(a){{
 a.addEventListener('click',function(){{
  try{{sessionStorage.setItem('pl_lang_choice','1');}}catch(e){{}}
  plEvent('language_selected',{{to:(a.getAttribute('href')||'').replace(/\//g,'')||'en'}});}});}});
// Языковой баннер. Никаких автоматических редиректов: только предложение.
// Показывается один раз на 90 дней и не показывается ботам (ТЗ §3).
(function(){{
 var PAGE="{code}";
 var HOMES={{en:"/",ru:"/ru/",es:"/es/",pt:"/pt/",de:"/de/"}};
 var NAMES={lang_names_js};
 var ORDER=["en","ru","es","pt","de"];
 var KEY="pl_lang_banner";
 var BOT=/bot|crawl|spider|slurp|bingpreview|headless|lighthouse|gptbot|claudebot|perplexity|applebot|facebookexternalhit/i;
 if(BOT.test(navigator.userAgent||"")||navigator.webdriver) return;
 try{{var until=parseInt(localStorage.getItem(KEY)||"0",10);
  if(until && Date.now()<until) return;}}catch(e){{}}
 var nav=(navigator.language||"").slice(0,2).toLowerCase();
 if(!nav||nav===PAGE||ORDER.indexOf(nav)<0) return;
 var bar=document.getElementById('langbar');
 var name=NAMES[ORDER.indexOf(nav)];
 document.getElementById('lb-text').textContent={banner_ask_js}.split('{{lang}}').join(name);
 document.getElementById('lb-go').textContent={banner_open_js};
 document.getElementById('lb-no').textContent={banner_stay_js};
 bar.classList.add('on');
 plEvent('language_suggestion_shown',{{suggested_language:nav}});
 function hide(){{try{{localStorage.setItem(KEY,String(Date.now()+90*864e5));}}catch(e){{}}
  bar.classList.remove('on');}}
 document.getElementById('lb-go').addEventListener('click',function(){{
  plEvent('language_suggestion_accepted',{{suggested_language:nav}});
  try{{sessionStorage.setItem('pl_lang_choice','1');}}catch(e){{}}
  hide();
  // UTM переносим, иначе источник теряется при смене языка
  location.href=HOMES[nav]+location.search+location.hash;
 }});
 document.getElementById('lb-no').addEventListener('click',function(){{
  plEvent('language_suggestion_dismissed',{{suggested_language:nav}});
  try{{sessionStorage.setItem('pl_lang_choice','1');}}catch(e){{}}
  hide();
 }});
}})();
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
   // Разговор на главной ведёт помощник на самой странице. Второй плавающий
   // чат рядом с ним — не выбор, а растерянность: пузырь на главной прячем.
   // На остальных страницах переписка доступна как прежде.
   if(document.getElementById('hm-hero')){{
    window.chatwootSettings.hideMessageBubble=true;
   }}
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
<script>{hero_js}</script>
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
