# -*- coding: utf-8 -*-
"""Первый экран: человек начинает решать свою задачу прямо здесь.

ГЛАВНАЯ МЕХАНИКА, КОТОРУЮ НЕЛЬЗЯ ПОТЕРЯТЬ. Посетитель пишет проблему или
выбирает ситуацию — и сразу идёт содержательный разговор. Не кнопка
«связаться», не анкета, не нарисованный чат. Думает та же связка, что и в
переписке: qualify.py держит состояние, routing.py выбирает следующий шаг,
Jev остаётся сигналом классификации. Второй машины диалога здесь нет.

ЧТО ПОКАЗЫВАЕМ КЛИЕНТУ, А ЧТО НЕТ
  • показываем: что поняли с его слов, что уточняем сейчас, что дальше;
  • не показываем: внутренние категории, «не обещать», имя партнёра до
    квалификации, оценки уверенности, служебные поля маршрутизации.

ПРО ВЫДУМАННЫЕ ФАКТЫ. В сцену попадает только сказанное клиентом. Нажатие
«не проходят платежи» значит ровно это: ни закрытого аккаунта, ни задержанных
выплат, пока он их не назвал. Готовый пример нашей работы стоит рядом и
подписан как пример.

ПРИЁМЫ ИЗ DESIGN_CONTEXT.md: заголовок строками; смена состояния вместо
прокрутки; глубина от курсора вместо видео; крупная типографика. Движение
отвечает на действие — само ничего не переключается.
"""
import html as H
import json
import re
import os

# Боевой адрес помощника по умолчанию. Пустое значение означало бы живую
# кнопку, которая никуда не ведёт, — на сайте это хуже её отсутствия.
ASSISTANT_API = os.environ.get("PL_ASSISTANT_API",
                               "https://scan.prodigylab.studio/api/assistant")
ОБРАЗЕЦ = '/showcase/covers/saeng-thai-house.jpg'

import hero_sections as HS  # noqa: E402
from hero_content import (ИМЕНА, КАМПАНИИ, ЯЗЫКИ, H1, НАБОРЫ, ПОДСКАЗКИ,
                          РЕШЕНИЕ, РЕШЕНИЕ_ПОДПИСЬ,  # noqa: E402
                          S)

CSS = """
/* Переключатель языка в шапке диалога. Названия языков — на своём языке,
   без флагов. Кнопка узкая, список раскрывается на месте и не растягивает
   шапку: иначе диалог дёргался бы при каждом открытии. */
.lang{margin-left:auto;position:relative}
.lang>button{font:500 12.5px/1 var(--mono);letter-spacing:.06em;color:var(--ink2);
 background:transparent;border:1px solid var(--line);padding:6px 9px;cursor:pointer;
 display:inline-flex;align-items:center;gap:6px}
.lang>button::after{content:"▾";font-size:10px;line-height:1;color:var(--ink3)}
.lang>button[aria-expanded="true"]::after{content:"▴";color:var(--accent)}
.lang>button:hover{color:var(--ink);border-color:var(--ink3)}
.lang>button[aria-expanded="true"]{color:var(--ink);border-color:var(--accent)}
.lang ul{position:absolute;right:0;top:calc(100% + 5px);z-index:40;margin:0;padding:4px;
 list-style:none;background:#fff;border:1px solid var(--line);min-width:132px;
 box-shadow:0 1px 0 var(--line)}
.lang[data-open="1"]{z-index:40}
.lang[hidden],.lang ul[hidden]{display:none}
.lang li+li{margin-top:1px}
.lang ul button{display:block;width:100%;text-align:left;font:400 14px/1.2 var(--sans);
 color:var(--ink);background:transparent;border:0;padding:8px 9px;cursor:pointer}
.lang ul button:hover{background:var(--paper2)}
.lang ul button[aria-current="true"]{color:var(--accent);font-weight:600}
.lang ul button[aria-current="true"]::after{content:" ✓"}
.m .tr{display:block;margin-top:5px;font:400 12.5px/1.3 var(--sans);color:var(--ink3);
 background:transparent;border:0;padding:0;cursor:pointer;text-decoration:underline}
.m .tr:hover{color:var(--ink2)}

/* Палитра — с живого prodigylab.studio. Скруглений нет нигде, кроме круглого
   знака; теней нет ни одной. Это сильнее любого цвета определяет наш вид. */
:root{--ink:#121212;--ink2:#5C5C5A;--ink3:#8A8A86;--paper:#FBFBF9;--paper2:#F3F2EE;
--line:#E2E1DC;--accent:#1C7E84;--accent2:#0F4A4E;--accent-soft:#E3F0F0;
--graphite:#0F1722;--graphite2:#1A2534;--on-dark:#E8ECEF;--on-dark2:#95A3B3;
--warn:#8A5A1C;--sans:Geist,system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:Geist,system-ui,sans-serif;
font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.hm-mono{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10.5px;
letter-spacing:.18em;text-transform:uppercase}

.hm{display:grid;grid-template-columns:1fr;align-items:start}
@media(min-width:1024px){.hm{grid-template-columns:44fr 56fr;min-height:100svh}}

.hm-l{padding:22px 20px 32px;display:flex;flex-direction:column}
@media(min-width:1024px){.hm-l{padding:30px 44px 40px}}
.hm-anchor{display:block;height:0;scroll-margin-top:72px}
.hm-brand{display:inline-flex;align-items:baseline;gap:6px;font-weight:700;letter-spacing:-.02em;
font-size:17px;text-decoration:none;color:var(--ink);margin-bottom:24px}
.hm-brand b{color:var(--accent);font-weight:700}
.hm-brand span{font-weight:300;color:var(--ink2)}
.hm-l .eyebrow{color:var(--accent)}
.hm h1{margin:12px 0 0;font-size:clamp(31px,4.1vw,52px);line-height:1.04;
letter-spacing:-.033em;font-weight:600;max-width:15ch}
.hm h1 .ln{display:block;overflow:hidden}
.hm h1 .ln>span{display:block;transform:translateY(104%);
transition:transform .6s cubic-bezier(.22,.8,.3,1)}
.hm h1 .ln>span.in{transform:translateY(0)}
.hm h1 .ln>span.done{transition:none;transform:none}
.hm-lede{max-width:40ch;margin:14px 0 0;color:var(--ink2);font-size:15.5px}

.talk{margin:22px 0 0;border:1px solid var(--line);background:var(--paper2);
display:flex;flex-direction:column}
.talk-h{display:flex;align-items:center;gap:9px;padding:11px 14px;
border-bottom:1px solid var(--line);background:#fff}
.talk-av{width:24px;height:24px;border-radius:50%;background:var(--accent);color:#fff;flex:none;
display:inline-flex;align-items:center;justify-content:center;font-size:9.5px}
.talk-n{font-size:13.5px;font-weight:500}
.talk-t{margin-left:auto;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:9px;
letter-spacing:.13em;text-transform:uppercase;color:var(--warn);border:1px solid var(--warn);
padding:3px 6px}
.stream{display:none;flex-direction:column;gap:10px;padding:14px}
.stream.hm-on{display:flex}
@media(min-width:1024px){.stream.hm-on{max-height:36svh;overflow-y:auto}}
.m{max-width:92%;font-size:15px;line-height:1.48;padding:10px 13px;
word-wrap:break-word;overflow-wrap:anywhere}
.m b{display:block;font-weight:500;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;
font-family:'JetBrains Mono',ui-monospace,monospace;margin-bottom:5px;opacity:.75}
.m-bot{align-self:flex-start;background:#fff;border:1px solid var(--line)}
.m-you{align-self:flex-end;background:var(--accent-soft);border:1px solid var(--accent);
color:var(--ink)}
.m-note{align-self:center;font-size:12px;color:var(--ink2);background:none;border:0;padding:2px}
.m-err{align-self:flex-start;background:#fff;border:1px solid var(--warn);color:var(--warn)}
.wait{align-self:flex-start;display:flex;align-items:center;gap:8px;font-size:14px;
color:var(--ink2);padding:8px 2px}
.wait i{width:8px;height:8px;background:var(--accent);display:inline-block;
animation:pulse 1s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}

.sugg{display:flex;flex-wrap:wrap;gap:7px;padding:0 14px 12px}
.sugg:empty{display:none}
.sugg button{font:inherit;font-size:14px;min-height:44px;padding:11px 14px;cursor:pointer;
background:#fff;color:var(--ink);border:1px solid var(--line)}
.sugg button:hover{border-color:var(--accent);color:var(--accent)}
.ask{display:flex;gap:8px;padding:12px 14px;border-top:1px solid var(--line);background:#fff}
.ask input{flex:1;min-width:0;font:inherit;font-size:16px;padding:13px;border:1px solid var(--line);
background:var(--paper);color:var(--ink)}
.ask input:focus{border-color:var(--accent)}
.ask button{flex:none;width:52px;min-height:48px;border:0;background:var(--accent);
color:#fff;cursor:pointer;font-size:18px}
.ask button:hover{background:var(--accent2)}
.ask button[disabled]{opacity:.5;cursor:default}

/* Финал: резюме, следующий шаг и заявка — в том же разговоре. */
.fin{border:1px solid var(--accent);background:#fff;padding:14px}
.fin h3{margin:0 0 9px;font-size:15px;font-weight:600}
.fin ul{margin:0 0 10px;padding-left:17px;font-size:14.5px;color:var(--ink2)}
.fin .next{background:var(--accent-soft);border-left:3px solid var(--accent);
padding:9px 11px;font-size:14.5px;margin:0 0 11px}
.fin .ways{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 10px}
.fin .ways button{font:inherit;font-size:14px;min-height:44px;padding:10px 14px;cursor:pointer;
background:var(--paper);border:1px solid var(--line);color:var(--ink)}
.fin .ways button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);
color:#fff}
.fin label{display:block;font-size:12.5px;color:var(--ink2);margin:0 0 4px}
.fin input{width:100%;font:inherit;font-size:16px;padding:11px;border:1px solid var(--line);
background:var(--paper);margin:0 0 9px}
.fin .row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.fin .hm-go{font:inherit;font-size:15px;min-height:48px;padding:12px 20px;border:0;cursor:pointer;
background:var(--ink);color:#fff}
.fin .hm-go:hover{background:var(--accent)}
.fin .hm-go[disabled]{opacity:.5;cursor:default}
.fin .edit{font:inherit;font-size:14px;background:none;border:0;padding:0;cursor:pointer;
color:var(--accent);border-bottom:1px solid var(--accent)}
.fin .ok{border:1px solid var(--accent);background:var(--accent-soft);padding:11px;font-size:14.5px}
.fin .err{border:1px solid var(--warn);color:var(--warn);padding:11px;font-size:14.5px}

.hm-pick{display:block;margin:18px 0 9px;color:var(--ink3)}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:0;padding:0;list-style:none}
.chips button{font:inherit;font-size:14px;min-height:44px;padding:11px 15px;cursor:pointer;
background:transparent;color:var(--ink);border:1px solid var(--line);
transition:border-color .15s,color .15s,background .15s}
.chips button:hover{border-color:var(--accent);color:var(--accent)}
.chips button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
.chips button[aria-pressed="true"]::before{content:"✓ "}
.chips .near button{color:var(--ink2);border-style:dashed}
.tail{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-top:16px}
.tail a,.tail button{font:inherit;font-size:14.5px;color:var(--ink2);background:none;border:0;
padding:0;cursor:pointer;text-decoration:none;border-bottom:1px solid var(--line)}
.tail a:hover,.tail button:hover{color:var(--accent);border-bottom-color:var(--accent)}
button:focus-visible,input:focus-visible,a:focus-visible{outline:2px solid var(--accent);
outline-offset:3px}

/* Сцена: графит, а не чёрная пустота. */
.hm-r{position:relative;background:var(--graphite);color:var(--on-dark);overflow:hidden;
padding:22px 20px 26px}
@media(min-width:1024px){.hm-r{padding:30px 40px;min-height:100svh;
display:flex;flex-direction:column;justify-content:center;gap:20px}}
.hm-face{display:flex;align-items:center;gap:11px;margin:0 0 16px}
.hm-face img{width:46px;height:46px;border-radius:50%;object-fit:cover;flex:none;
 border:1px solid var(--graphite2)}
.hm-face span{font:500 12px/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase;
 color:var(--on-dark2)}
@media(min-width:1024px){.hm-face img{width:56px;height:56px}}
.hm-steps{display:grid;gap:9px;grid-template-columns:1fr;
transform:translate3d(var(--dx,0),var(--dy,0),0);transition:transform .3s ease-out}
@media(min-width:640px){.hm-face{display:flex;align-items:center;gap:11px;margin:0 0 16px}
.hm-face img{width:46px;height:46px;border-radius:50%;object-fit:cover;flex:none;
 border:1px solid var(--graphite2)}
.hm-face span{font:500 12px/1.3 var(--mono);letter-spacing:.1em;text-transform:uppercase;
 color:var(--on-dark2)}
@media(min-width:1024px){.hm-face img{width:56px;height:56px}}
.hm-steps{grid-template-columns:repeat(3,1fr)}}
.hm-step{border:1px solid var(--graphite2);padding:13px 14px;background:#131C28;min-height:92px;
transition:border-color .3s,background .3s}
.hm-step.live{border-color:var(--accent);background:#102024}
.hm-step.done{border-color:#2F4A4C}
.hm-step .hm-mono{color:var(--on-dark2);display:flex;align-items:center;gap:6px;margin-bottom:7px}
.hm-step.live .hm-mono{color:var(--accent)}
.hm-step .hm-mono i{font-style:normal}
.hm-step p{margin:0;font-size:14.5px;line-height:1.45;color:var(--on-dark);overflow-wrap:anywhere}
.hm-step p.dim{color:var(--on-dark2)}
.hm-shot{position:relative;border:1px solid var(--graphite2);background:#0B1119;margin:0;
transform:translate3d(calc(var(--dx,0)*-.5),calc(var(--dy,0)*-.5),0);
transition:transform .3s ease-out}
.hm-shot img{display:block;width:100%;height:auto}
.hm-shot figcaption{padding:9px 13px;font-size:12px;color:var(--on-dark2);
border-top:1px solid var(--graphite2);display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.hm-shot .tag{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:9px;letter-spacing:.13em;
text-transform:uppercase;color:#07131A;background:var(--accent);padding:2px 6px}

@media(prefers-reduced-motion:reduce){
 .hm h1 .ln>span{transform:none;transition:none}
 .hm-steps,.hm-shot,.hm-step,.chips button,.wait i{transition:none;transform:none;animation:none}
}
"""

JS = """
(function(){
 var API=%(api)s, LANG_API=%(lang_api)s, LEAD_API=%(lead_api)s, STATE_API=%(state_api)s;
 var DATA=%(data)s, NAMES=%(names)s, LANGS=%(langs)s, MAP=%(map)s;
 var ЯЗЫК=%(lang)s;
 var поток=document.getElementById('stream'), подсказки=document.getElementById('sugg');
 var поле=document.getElementById('ask-i'), форма=document.getElementById('ask');
 var кнопка=document.getElementById('ask-b'), чипы=document.getElementById('chips');
 var шагЗадача=document.getElementById('s-task'), шагУточн=document.getElementById('s-clar');
 var шагДальше=document.getElementById('s-next'), сцена=document.getElementById('hm-r');
 var сменить=document.getElementById('restart'), h1=document.getElementById('h1');
 var ролик=document.getElementById('lang'), списокЯз=document.getElementById('lang-list');
 var кнЯз=document.getElementById('lang-btn');
 // Сессия переживает переход на другую языковую страницу: иначе ссылка
 // «ES» в шапке начинала бы разговор с нуля и спрашивала уже известное.
 // Хранилище может быть недоступно — тогда просто новая сессия.
 var сессия=(function(){
  try{ var б=localStorage.getItem('pl-hm-sid'); if(б) return б; }catch(e){}
  var н='hm-'+Math.random().toString(36).slice(2,9)+Date.now().toString(36).slice(-4);
  try{ localStorage.setItem('pl-hm-sid',н); }catch(e){}
  return н;
 })();
 var занят=false, начали=false, ждётВыбора=null;
 var тонкая=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 var ситуация='', ключВопроса='', финалБлок=null;

 var q=new URLSearchParams(location.search);
 var demo=q.get('demo')||'';
 var метка=(q.get('utm_campaign')||q.get('src')||q.get('utm_content')||'').toLowerCase();
 var набор='general';
 for(var k in MAP){ if(метка.indexOf(k)>=0){ набор=MAP[k]; break; } }

 function T(){ return DATA[ЯЗЫК].s; }
 function экр(t){ return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;'); }

 // ---------------------------------------------------------------- ситуации
 function рисоватьЧипы(имя){
  var было=чипы.querySelector('button[aria-pressed="true"]');
  var выбран=было?было.getAttribute('data-k'):'';
  var порядок=было?было.getAttribute('data-i'):'';
  var s=DATA[ЯЗЫК].sets[имя]||DATA[ЯЗЫК].sets.general, html='';
  s.main.forEach(function(p,i){
   html+='<li><button type="button" data-k="'+p[0]+'" data-i="m'+i+'">'+экр(p[1])+'</button></li>'; });
  s.near.forEach(function(p,i){
   html+='<li class="near"><button type="button" data-k="'+p[0]+'" data-i="n'+i+'">'+экр(p[1])+'</button></li>'; });
  чипы.innerHTML=html;
  // Порядок кнопок при смене языка не меняется, поэтому выбранная остаётся
  // на своём месте — под тем же пальцем.
  if(выбран){
   var та=чипы.querySelector('button[data-i="'+порядок+'"]');
   if(та) та.setAttribute('aria-pressed','true');
  }
 }
 function заголовок(ключ,мгновенно){
  var пара=DATA[ЯЗЫК].h1[ключ]||DATA[ЯЗЫК].h1[''];
  var строки=h1.querySelectorAll('.ln>span');
  if(строки[0].textContent.trim()===пара[0]&&строки[1].textContent.trim()===пара[1]) return;
  строки.forEach(function(э,i){
   if(тонкая||мгновенно){ э.textContent=пара[i]; э.classList.add('in','done'); return; }
   э.classList.remove('done','in');
   window.setTimeout(function(){ э.textContent=пара[i];
    window.requestAnimationFrame(function(){ э.classList.add('in'); }); },120+i*60);
  });
 }

 // ---------------------------------------------------------------- реплики
 function сказать(кто,текст,ключ){
  поток.classList.add('hm-on');
  var d=document.createElement('div');
  if(кто==='note'){ d.className='m m-note'; d.textContent=текст; }
  else if(кто==='err'){ d.className='m m-err'; d.textContent=текст; }
  else {
   d.className='m '+(кто==='you'?'m-you':'m-bot');
   var b=document.createElement('b'); b.textContent=(кто==='you'?T().you:T().bot);
   d.appendChild(b);
   var t=document.createElement('span'); t.className='tx'; t.textContent=текст;
   d.appendChild(t);
   if(кто==='bot'){ d.setAttribute('data-key',ключ||''); d.setAttribute('data-lang',ЯЗЫК); }
  }
  поток.appendChild(d); поток.scrollTop=поток.scrollHeight;
  return d;
 }
 function ждём(){
  var d=document.createElement('div'); d.className='wait';
  d.innerHTML='<i></i><span>'+экр(T().thinking)+'</span>';
  поток.classList.add('hm-on'); поток.appendChild(d); поток.scrollTop=поток.scrollHeight; return d;
 }
 function шаг(узел,текст,состояние){
  var p=узел.querySelector('p'), м=узел.querySelector('.hm-mono i');
  var пусто=(!текст||текст===T().undefined||текст===T().waiting);
  var новое=пусто?'\u2014':текст;
  if(p.textContent!==новое){
   // Значение подменяется не рывком: гаснет, меняется, проявляется.
   p.classList.add('upd');
   window.setTimeout(function(){ p.textContent=новое; p.classList.remove('upd'); },260);
  }
  p.classList.toggle('dim',пусто);
  узел.classList.toggle('live',состояние==='live');
  узел.classList.toggle('done',состояние==='done');
  if(м) м.textContent=(состояние==='done'?'\\u2713':(состояние==='live'?'\\u2192':''));
 }
 function подсказатьК(ключ){
  // Ключ постоянный: идентификатор поля или строка-источник вопроса. Текст
  // вопроса сверять нельзя — после смены языка он другой.
  подсказки.innerHTML='';
  ключВопроса=ключ||'';
  var набор=(DATA[ЯЗЫК].hints||{})[ключВопроса];
  if(!набор) return;
  набор.forEach(function(в){
   подсказки.innerHTML+='<button type="button" data-say="'+экр(в)+'">'+экр(в)+'</button>'; });
 }

 // ------------------------------------------------------------------ язык
 function рисоватьСписок(){
  var html='';
  LANGS.forEach(function(к){
   html+='<li><button type="button" data-lang="'+к+'"'
        +(к===ЯЗЫК?' aria-current="true"':'')+'>'+экр(NAMES[к])+'</button></li>'; });
  списокЯз.innerHTML=html;
 }
 function применитьЯзык(новый){
  // Меняется только оформление: история, ввод, позиция прокрутки и этап
  // разговора остаются как были. Страница не перезагружается намеренно.
  var прокрутка=поток.scrollTop, фокус=(document.activeElement===поле);
  ЯЗЫК=новый;
  document.documentElement.lang=новый;
  var d=T();
  // Один промахнувшийся селектор не должен обрывать переключение: иначе
  // страница остаётся наполовину на старом языке, а человек видит ошибку.
  function уст(селектор,html){
   var э=document.querySelector(селектор);
   if(э) э.innerHTML=html;
   return !!э;
  }
  уст('.eyebrow',d.eyebrow);
  уст('.hm-lede',d.lede);
  уст('.hm-pick',d.pick);
  сменить.innerHTML=d.other;
  уст('.tail a',d.more+' &rarr;');
  уст('.talk-n',d.panel);
  поле.placeholder=начали?d.input_next:d.input;
  поток.setAttribute('data-hint',d.hint_start||d.input);
  кнопка.setAttribute('aria-label',d.send);
  уст('label[for="ask-i"]',d.input);
  кнЯз.textContent=NAMES[новый];
  кнЯз.setAttribute('aria-label',d.lang_pick);
  уст('#s-task .hm-mono',d.task+' <i></i>');
  уст('#s-clar .hm-mono',d.clarify+' <i></i>');
  уст('#s-next .hm-mono',d.nxt+' <i></i>');
  уст('.hm-shot figcaption','<span class="tag">'+d.sample+'</span>'+d.sample_cap);
  // Подписи «Вы» и «Помощник» — наши, их обновляем. Текст реплик клиента
  // не трогаем ни при каких условиях: это его слова.
  поток.querySelectorAll('.m-you>b').forEach(function(b){ b.textContent=d.you; });
  поток.querySelectorAll('.m-bot>b').forEach(function(b){ b.textContent=d.bot; });
  рисоватьЧипы(ситуация?набор:набор);
  рисоватьСписок();
  заголовок(ситуация,true);
  подсказатьК(ключВопроса);
  if(финалБлок) обновитьФинал();
  if(тема!==null) применитьРаздел(тема);
  поток.scrollTop=прокрутка;
  if(фокус) поле.focus({preventScroll:true});
 }
 function перевестиПоследнийВопрос(текст){
  // Вопрос — наша реплика, её можно показать на новом языке. Оригинал
  // остаётся доступен действием, а не пропадает.
  var все=поток.querySelectorAll('.m-bot');
  if(!все.length) return;
  var узел=все[все.length-1], тело=узел.querySelector('.tx');
  if(!тело||тело.textContent.trim()===текст) return;
  var оригинал=узел.getAttribute('data-orig')||тело.textContent;
  узел.setAttribute('data-orig',оригинал);
  тело.textContent=текст;
  var было=узел.querySelector('.tr');
  if(было) было.remove();
  var б=document.createElement('button');
  б.type='button'; б.className='tr'; б.textContent=T().show_original;
  var показан=false;
  б.addEventListener('click',function(){
   показан=!показан;
   тело.textContent=показан?оригинал:текст;
   б.textContent=показан?T().show_translation:T().show_original;
  });
  узел.appendChild(б);
 }
 async function выбратьЯзык(код){
  if(код===ЯЗЫК||занят) return;
  занят=true;
  try{
   var r=await fetch(LANG_API,{method:'POST',headers:{'Content-Type':'application/json'},
     body:JSON.stringify({session:сессия,lang:код})});
   var d=await r.json();
   if(!d.ok) throw new Error(d.error||'');
   применитьЯзык(код);
   if(d['вопрос']){
    перевестиПоследнийВопрос(d['вопрос']);
    // Правая колонка — то же состояние другими словами. Если её не обновить,
    // страница и разговор расходятся: вопрос на экране один, в колонке другой.
    шаг(шагУточн,d['вопрос'],'live');
   } else { шаг(шагУточн,T().done_q,'done'); }
   var р=d['резюме']||[];
   if(р.length) шаг(шагЗадача,р.join(' \\u00b7 '),'done');
   if(d['следующий']) шаг(шагДальше,d['следующий'],d['готово']?'live':'');
   сказать('note',d['подтверждение']||T().switched_to);
  }catch(e){
   // Язык интерфейса не меняем, если сервер не подтвердил: иначе страница и
   // разговор разойдутся.
   сказать('err',T().offline);
  }
  занят=false;
 }

 // ------------------------------------------------------------------ финал
 function обновитьФинал(){
  if(!финалБлок) return;
  var d=T();
  var п=финалБлок.querySelector('h3'); if(п) п.textContent=d.sum_h;
  var пр=финалБлок.querySelector('[data-edit]'); if(пр) пр.textContent=d.fix;
  var от=финалБлок.querySelector('[data-send]'); if(от) от.textContent=d.send_lead;
  var мк=финалБлок.querySelector('[data-l-how]'); if(мк) мк.textContent=d.how;
  var мc=финалБлок.querySelector('[data-l-contact]'); if(мc) мc.textContent=d.contact;
  var мn=финалБлок.querySelector('[data-l-name]'); if(мn) мn.textContent=d.name;
 }
 function финал(ф){
  подсказки.innerHTML=''; ключВопроса='';
  var d=document.createElement('div'); d.className='m fin';
  var список=(ф['резюме']||[]).map(function(x){ return '<li>'+экр(x)+'</li>'; }).join('');
  var нужно=(ф['нужно']||[])[0];
  d.innerHTML='<h3>'+экр(T().sum_h)+'</h3><ul>'+(список||'<li>'+экр(T().undefined)+'</li>')+'</ul>'
   +'<p style="margin:0 0 10px"><button type="button" class="edit" data-edit>'+экр(T().fix)+'</button></p>'
   +'<div class="next">'+экр(ф['следующий']||'')+'</div>'
   +(нужно?'<label for="fin-site">'+экр(нужно['вопрос'])+'</label>'
           +'<input id="fin-site" type="url" inputmode="url" placeholder="https://">':'')
   +'<label data-l-how>'+экр(T().how)+'</label><div class="ways">'
   +(ф['способы']||[]).map(function(s){
      return '<button type="button" data-way="'+s.k+'" aria-pressed="false">'+экр(s.n)+'</button>';
     }).join('')+'</div>'
   +'<label for="fin-c" data-l-contact>'+экр(T().contact)+'</label>'
   +'<input id="fin-c" type="text" autocomplete="off">'
   +'<label for="fin-n" data-l-name>'+экр(T().name)+'</label>'
   +'<input id="fin-n" type="text" autocomplete="off">'
   +'<div class="row"><button type="button" class="hm-go" data-send>'+экр(T().send_lead)+'</button>'
   +'<span data-msg></span></div>';
  поток.appendChild(d); поток.scrollTop=поток.scrollHeight;
  финалБлок=d;

  var способ='';
  d.querySelector('.ways').addEventListener('click',function(ev){
   var б=ev.target.closest('button'); if(!б) return;
   способ=б.getAttribute('data-way');
   d.querySelectorAll('.ways button').forEach(function(x){
    x.setAttribute('aria-pressed', x===б?'true':'false'); });
  });
  d.querySelector('[data-edit]').addEventListener('click',function(){
   сказать('note',T().fix_hint); поле.focus();
  });
  var отправка=d.querySelector('[data-send]'), сообщение=d.querySelector('[data-msg]');
  отправка.addEventListener('click',async function(){
   var c=(d.querySelector('#fin-c')||{}).value||'';
   var n=(d.querySelector('#fin-n')||{}).value||'';
   var site=(d.querySelector('#fin-site')||{}).value||'';
   if(!способ){ сообщение.textContent=T().pick_way; return; }
   if(!c.trim()){ сообщение.textContent=T().need_contact; return; }
   отправка.disabled=true; сообщение.textContent=T().saving;
   try{
    var r=await fetch(LEAD_API,{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({session:сессия,method:способ,contact:c.trim(),
                           name:n.trim(),site:site.trim()})});
    var o=await r.json();
    if(!o.ok) throw new Error(o.error||'');
    // Подтверждение только после успешной записи, и с номером обращения.
    d.innerHTML='<div class="ok"><b>'+экр(T().saved)+'</b>'
      +экр(T().saved_p)+' #'+o.lead+(o['повтор']?' ('+экр(T().again)+')':'')+'</div>';
    финалБлок=null;
    показатьЗаявку(o.lead,o['повтор']);
   }catch(e){
    сообщение.textContent=''; отправка.disabled=false;
    var пред=d.querySelector('.err'); if(пред) пред.remove();
    var pp=document.createElement('div'); pp.className='err';
    pp.textContent=T().save_err; d.appendChild(pp);
   }
  });
 }

 // ------------------------------------------------------------------ обмен
 async function послать(тело, эхо){
  if(занят) return;
  // Человек заговорил, не ответив на «продолжить прошлое?». Значит начинает
  // новое: на старую сессию его реплику слать нельзя — вернётся чужое для
  // него состояние. Прошлый разговор при этом не удаляется.
  if(ждётВыбора){
   ждётВыбора.querySelectorAll('button').forEach(function(б){ б.remove(); });
   ждётВыбора=null; новаяСессия();
  }
  занят=true; кнопка.disabled=true;
  var w=ждём();
  try{
   if(!API) throw new Error('нет адреса');
   var r=await fetch(API,{method:'POST',headers:{'Content-Type':'application/json'},
     body:JSON.stringify(Object.assign({session:сессия,lang:ЯЗЫК},тело))});
   var d=await r.json(); w.remove();
   if(!d.ok) throw new Error(d.error||'отказ');
   начали=true;
   var сдвиг=d['язык_сдвиг']||{};
   if(сдвиг['перешли']&&сдвиг['перешли']!==ЯЗЫК){
    // Клиент сам перешёл на другой язык, ручного выбора не было.
    применитьЯзык(сдвиг['перешли']);
    сказать('note',сдвиг['подтверждение']||T().switched_to);
   }
   if(d['готово']&&d['следующий']) следующийШаг=d['следующий'];
   else следующийШаг='';
   if(d['тема']!==undefined) показатьРаздел(d['тема']||'', d['известно']);
   var р=d['резюме']||[];
   шаг(шагЗадача, р.length?р.join(' \\u00b7 '):T().undefined, р.length?'done':'');
   if(d['вопрос']){
    сказать('bot',d['вопрос'],d['вопрос_ключ']);
    подсказатьК(d['вопрос_ключ']);
    шаг(шагУточн,d['вопрос'],'live');
    шаг(шагДальше,T().undefined,'');
   } else {
    шаг(шагУточн,T().done_q,'done');
    шаг(шагДальше,(d['финал']||{})['следующий']||T().undefined,'live');
    if(d['финал']) финал(d['финал']);
   }
   if(сдвиг['предложить']){
    // Ручной выбор не перебиваем — только предлагаем.
    var п=сказать('note',сдвиг['вопрос_языка']);
    var б=document.createElement('button');
    б.type='button'; б.className='tr'; б.textContent=NAMES[сдвиг['предложить']];
    б.addEventListener('click',function(){ выбратьЯзык(сдвиг['предложить']); });
    п.appendChild(б);
   }
   поле.placeholder=T().input_next;
  }catch(e){
   w.remove(); сказать('err',T().offline);
   if(эхо) поле.value=эхо;
  }
  занят=false; кнопка.disabled=false;
 }

 // -------------------------------------------------------------- действия
 чипы.addEventListener('click',function(ev){
  var б=ev.target.closest('button'); if(!б) return;
  var k=б.getAttribute('data-k');
  чипы.querySelectorAll('button').forEach(function(x){
   x.setAttribute('aria-pressed', x===б?'true':'false'); });
  ситуация=k; заголовок(k); сказать('you',б.textContent.trim());
  свернутьСетку(б.textContent.trim());
  послать({action:'start',situation:k,text:б.textContent.trim()});
  поле.focus({preventScroll:true});
 });
 подсказки.addEventListener('click',function(ev){
  var б=ev.target.closest('button'); if(!б) return;
  var t=б.getAttribute('data-say'); подсказки.innerHTML='';
  сказать('you',t); послать({action: начали?'say':'start', text:t}, t);
 });
 форма.addEventListener('submit',function(ev){
  ev.preventDefault();
  var t=(поле.value||'').trim(); if(!t||занят) return;
  поле.value=''; подсказки.innerHTML='';
  сказать('you',t); послать({action: начали?'say':'start', text:t}, t);
 });
 сменить.addEventListener('click',function(){
  сказать('note',T().kept);
  чипы.querySelectorAll('button').forEach(function(x){ x.setAttribute('aria-pressed','false'); });
  ситуация=''; рисоватьЧипы('general'); заголовок(''); поле.focus({preventScroll:true});
 });
 кнЯз.addEventListener('click',function(){
  var открыт=кнЯз.getAttribute('aria-expanded')==='true';
  кнЯз.setAttribute('aria-expanded', открыт?'false':'true');
  списокЯз.hidden=открыт;
  ролик.setAttribute('data-open', открыт?'0':'1');
  if(!открыт){ var п=списокЯз.querySelector('button'); if(п) п.focus(); }
 });
 списокЯз.addEventListener('click',function(ev){
  var б=ev.target.closest('button'); if(!б) return;
  кнЯз.setAttribute('aria-expanded','false'); списокЯз.hidden=true;
  выбратьЯзык(б.getAttribute('data-lang'));
  поле.focus({preventScroll:true});
 });
 document.addEventListener('click',function(ev){
  if(!ролик.contains(ev.target)&&кнЯз.getAttribute('aria-expanded')==='true'){
   кнЯз.setAttribute('aria-expanded','false'); списокЯз.hidden=true; }
 });
 document.addEventListener('keydown',function(ev){
  if(ev.key==='Escape'&&кнЯз.getAttribute('aria-expanded')==='true'){
   кнЯз.setAttribute('aria-expanded','false'); списокЯз.hidden=true; кнЯз.focus(); }
 });

 if(!тонкая && window.matchMedia('(hover: hover) and (pointer: fine)').matches){
  сцена.addEventListener('pointermove',function(e){
   var r=сцена.getBoundingClientRect();
   сцена.style.setProperty('--dx',(((e.clientX-r.left)/r.width-.5)*12).toFixed(1)+'px');
   сцена.style.setProperty('--dy',(((e.clientY-r.top)/r.height-.5)*9).toFixed(1)+'px'); });
  сцена.addEventListener('pointerleave',function(){
   сцена.style.setProperty('--dx','0px'); сцена.style.setProperty('--dy','0px'); });
 }



 // -------------------------------------------------- разделы под задачу
 // Отдельной логики персонализации нет: направление приходит из того же
 // ответа, что ведёт разговор. Разделы собираются из данных на языке
 // разговора — поэтому испанского разговора с английским предложением
 // ниже не получится.
 var разделы=document.getElementById('pf');
 var гнездо=разделы?разделы.querySelector('.pf-in'):null;
 var переклБлок=document.getElementById('pf-switch');
 var тема=null, ждётПоказа=null;

 function видимРаздел(){
  if(!разделы) return false;
  var r=разделы.getBoundingClientRect();
  return r.top < window.innerHeight - 80 && r.bottom > 80;
 }
 // Направления, где показывать чужую работу нельзя: у денежных задач нет
 // опубликованного примера, а любая подставленная картинка читается как
 // «вот решение вашей проблемы». Там остаётся только трекер.
 var БЕЗ_КАРТИНКИ = {payments:1, banking:1, funding:1, accounting:1};

 function подобратьПример(к){
  var S=DATA[ЯЗЫК].sections, б=S.routes[к]||S.routes[''];
  var список=б.examples||[];
  if(подтверждено.demo_id){
   for(var d=0;d<список.length;d++){
    if(список[d].url.indexOf(подтверждено.demo_id)>=0) return список[d];
   }
  }
  var ниша=((подтверждено.business_type||'')+' '
            +(подтверждено.what_happened||'')).toLowerCase();
  if(ниша){
   for(var i=0;i<список.length;i++){
    var приметы=(S.niche_hints||{})[список[i].niche]||[список[i].niche];
    for(var j=0;j<приметы.length;j++){
     if(приметы[j] && ниша.indexOf(приметы[j])>=0) return список[i];
    }
   }
  }
  return список[0]||null;
 }

 // ------------------------------------------------- тема полосы под задачу
 // Фотография и иллюстрация меняются вместе с направлением разговора и
 // нишей клиента: ресторану не показываем склад. Снимки свои на каждой
 // полосе, чтобы страница не повторяла одну картинку.
 var ФОТО = {
  '': ['neutral-1','operations-1','presence-2'],
  presence: ['presence-1','presence-2','fence-1'],
  growth: ['growth-1','growth-2','neutral-1'],
  payments: ['payments-1','payments-2','growth-1'],
  banking: ['banking-1','banking-2','accounting-2'],
  funding: ['funding-1','funding-2','fulfillment-2'],
  operations: ['operations-1','operations-2','accounting-1'],
  infrastructure: ['infrastructure-1','infrastructure-2','operations-2'],
  accounting: ['accounting-1','accounting-2','banking-1'],
  fulfillment: ['fulfillment-1','fulfillment-2','funding-1']
 };
 var НИША_ФОТО = {
  fencing:['fence-1','fence-2','funding-2'], restaurant:['food-1','food-2','growth-2'],
  bakery:['food-2','presence-1','growth-2'], flowers:['growth-2','presence-1','neutral-1'],
  retail:['growth-1','presence-1','fulfillment-1'],
  logistics:['fulfillment-1','fulfillment-2','funding-1'],
  beauty:['growth-1','presence-1','neutral-2'], fitness:['growth-2','neutral-1','operations-1'],
  auto:['funding-2','fulfillment-1','operations-2'], clinic:['banking-1','operations-1','accounting-2'],
  construction:['funding-2','fence-2','fulfillment-2'], realestate:['presence-1','neutral-2','banking-2'],
  coffee:['food-2','food-1','presence-2'], cleaning:['operations-1','fulfillment-2','neutral-1']
 };
 var ПРИМЕТЫ_НИШИ = {
  fencing:['fenc','забор','ограда','ворота','cerca','valla','zaun'],
  restaurant:['restaur','ресторан','кафе','cafe','кухн','пицц','суши','бар','food'],
  bakery:['пекарн','bakery','хлеб','кондитер','panader','konditor'],
  flowers:['цвет','flower','floral','flor'],
  retail:['магазин','shop','store','retail','tienda','бутик','косметик','одежд'],
  logistics:['склад','доставк','логист','warehouse','shipping','fulfil']
 };
 var ИЛЛ_НАПРАВЛЕНИЯ = ['presence','payments','banking','funding','growth',
   'operations','infrastructure','accounting','fulfillment'];
 var ИЛЛ_НИШИ = ['fencing','restaurant','bakery','flowers','retail','logistics',
   'beauty','fitness','auto','clinic','construction','realestate','coffee','cleaning'];
 function нишаКлиента(){
  var т=((подтверждено.business_type||'')+' '+(подтверждено.what_happened||'')).toLowerCase();
  if(!т.trim()) return '';
  for(var н in ПРИМЕТЫ_НИШИ){
   for(var i=0;i<ПРИМЕТЫ_НИШИ[н].length;i++){
    if(т.indexOf(ПРИМЕТЫ_НИШИ[н][i])>=0) return н; } }
  return '';
 }
 window.ИЛЛЮСТРАЦИЯ = function(к){
  var н=нишаКлиента();
  if(н && ИЛЛ_НИШИ.indexOf(н)>=0) return н;
  return ИЛЛ_НАПРАВЛЕНИЯ.indexOf(к)>=0 ? к : 'neutral';
 };
 var темаСейчас=null, фонРаздела=null;
 // Снимок меняется перекрёстным растворением: новый слой проявляется над
 // старым, и только потом старый убирается. Подмена одной картинки давала
 // рывок.
 function поставитьФон(узел,имя,класс){
  if(!узел||!имя) return;
  if(узел.getAttribute('data-ph')===имя){ if(класс) узел.classList.add(класс); return; }
  узел.setAttribute('data-ph',имя);
  var путь='/assets/ph/'+имя+'.jpg';
  var i=new Image();
  i.onload=function(){
   if(узел.getAttribute('data-ph')!==имя) return;  // пока грузили, выбрали другой
   var слой=document.createElement('i');
   слой.className='ph-l';
   слой.style.backgroundImage='url('+путь+')';
   узел.appendChild(слой);
   if(класс) узел.classList.add(класс);
   var снято=false;
   // Нижние слои снимаем только когда верхний стал полностью непрозрачным.
   // Раньше их убирали на 950 мс при переходе в 1.6 с — и фон моргал.
   function снять(){
    if(снято) return; снято=true;
    var все=узел.querySelectorAll('.ph-l');
    for(var k=0;k<все.length;k++){ if(все[k]===слой) break; все[k].remove(); }
   }
   слой.addEventListener('transitionend',function(e){
    if(e.propertyName==='opacity') снять(); });
   void слой.offsetHeight;
   слой.classList.add('on');
   window.setTimeout(снять,2200);   // запас, если события не будет
  };
  i.src=путь;
 }
 // У каждой задачи свой набор полос. Концепты сайтов не показываем тому,
 // у кого вопрос про банк или автоматизацию: это не его пример.
 var ПОТОК = {presence:'site', growth:'site',
   payments:'money', banking:'money', funding:'money', accounting:'money',
   operations:'ops', infrastructure:'ops', fulfillment:'ops'};
 function поставитьПоток(к){
  var п=ПОТОК[к]||'start';
  if(document.body.getAttribute('data-flow')!==п) document.body.setAttribute('data-flow',п);
 }
 window.наТему = function(к, известно){
  поставитьПоток(к||'');
  var н=нишаКлиента(), ключ=(к||'')+'|'+н;
  if(темаСейчас===ключ) return;
  темаСейчас=ключ;
  var с=(н&&НИША_ФОТО[н])||ФОТО[к||'']||ФОТО[''];
  поставитьФон(document.getElementById('hero-ph'), с[0], 'on');
  фонРаздела=с[1%%с.length];
  поставитьФон(document.querySelector('.pf-ph'), фонРаздела);
  поставитьФон(document.getElementById('fin-ph'), с[2%%с.length]);
  var ф=document.getElementById('fin-ill');
  if(ф){ var файл=(window.ИЛЛЮСТРАЦИЯ||function(){return 'neutral';})(к);
   var п='/assets/il/'+файл+'.jpg';
   if(ф.getAttribute('src')!==п){ ф.style.opacity='0'; var n=new Image();
    n.onload=function(){ ф.src=п; ф.style.opacity=''; }; n.src=п; } }
 };
 // Полосу раздела помощник пересобирает целиком — фон и проявление
 // возвращаем наблюдателем, а не одним вызовом.
 (function(){
  var полоса=document.getElementById('pf');
  if(!полоса||!window.MutationObserver) return;
  new MutationObserver(function(){
   var у=полоса.querySelector('.pf-ph');
   if(у&&фонРаздела&&!у.style.backgroundImage) поставитьФон(у,фонРаздела);
   оживить(полоса);
  }).observe(полоса,{childList:true,subtree:true});
 })();
 var тихо2=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 var наблюдатель=(!тихо2&&window.IntersectionObserver)
  ? new IntersectionObserver(function(зап){
      зап.forEach(function(з){ if(з.isIntersecting){
       з.target.classList.add('seen'); наблюдатель.unobserve(з.target); } });
    },{threshold:0.12,rootMargin:'0px 0px -40px 0px'})
  : null;
 function оживить(корень){
  корень.querySelectorAll('.pf-card,.pf-visual,.pf-known,.ill').forEach(function(n){
   if(n.classList.contains('rise')||n.classList.contains('seen')) return;
   if(!наблюдатель){ n.classList.add('seen'); return; }
   n.classList.add('rise'); наблюдатель.observe(n); });
 }
 // Карточки работ: переключение компьютер/телефон.
 document.addEventListener('click',function(ev){
  var б=ev.target.closest('.wk-dev button'); if(!б) return;
  var карта=б.closest('.wk'), реж=б.getAttribute('data-dev');
  карта.setAttribute('data-dev',реж);
  карта.querySelectorAll('.wk-dev button').forEach(function(x){
   x.setAttribute('aria-pressed', x===б?'true':'false'); });
  var img=карта.querySelector('.wk-inset img');
  if(img) img.src=img.getAttribute(реж==='d'?'data-desk':'data-phone');
 });
 // ---------------------------------------------------- сцена первого экрана
 // Три состояния: настоящая работа в макете устройства, схема разбора под
 // направление и — пока задача не названа — работа из галереи. Ни одного
 // выдуманного интерфейса с одобрениями и ростом.
 var СНИМКИ = {
  '/preview/neighborhood-fence/': {d:'/assets/demo/fence-desk.jpg', p:'/assets/demo/fence-phone.jpg'},
  '/preview/saeng-thai-house/':   {d:'/assets/demo/thai-desk.jpg',  p:'/assets/demo/thai-phone.jpg'}
 };
 // Как рисуем ход разбора для каждого направления: ветвление, поток или опись.
 var ВИД = {payments:'tree', banking:'tree', funding:'tree',
            operations:'flow', fulfillment:'flow', infrastructure:'flow',
            accounting:'list', growth:'steps', presence:'steps'};
 function PT(){ return T(); }   // подписи берём из общего набора строк
 // На телефоне и сцену показываем телефонную: широкий снимок там
 // обрезается в полоску и ничего не объясняет.
 var устройство=(window.innerWidth<=700?'p':'d');

 // В нейтральном состоянии показываем иллюстрацию, а не чужую работу:
 // пока задача не названа, подставлять пример не по адресу.
 function работаИзКаталога(){ return null; }
 function сценаРабота(пример){
  var s=СНИМКИ[пример.url]||(пример._desk?{d:пример._desk,p:пример._phone}:null), t=PT();
  var src=s?(устройство==='d'?s.d:s.p):пример.cover;
  var хост=(пример.url||'').replace(/^\\/preview\\//,'').replace(/\\/$/,'')+'.demo';
  return '<div class="shot" data-dev="'+(s?устройство:'d')+'">'
   +'<div class="shot-win"><div class="shot-bar"><i></i><i></i><i></i><span>'+экр(хост)+'</span></div>'
   +'<img src="'+src+'" alt="'+экр(пример.title)+'" decoding="async"></div>'
   +(s&&устройство==='d'?'<div class="shot-phone"><img src="'+s.p+'" alt="" decoding="async"></div>':'')
   +'<div class="shot-cap"><span class="tag">'+экр(T().sample)+'</span>'+экр(пример.title)
   +'<span class="shot-dev"><button type="button" data-dev="d"'
   +(устройство==='d'?' aria-pressed="true"':' aria-pressed="false"')+'>'+экр(t.desk||'')+'</button>'
   +'<button type="button" data-dev="p"'
   +(устройство==='p'?' aria-pressed="true"':' aria-pressed="false"')+'>'+экр(t.phone||'')+'</button></span>'
   +'<a class="shot-go" href="'+пример.url+'">'+экр((DATA[ЯЗЫК].sections.labels||{}).open||'')+' &rarr;</a>'
   +'</div></div>';
 }
 function сценаСхема(к){
  var S=DATA[ЯЗЫК].sections, б=S.routes[к]||S.routes[''], t=PT();
  var поток=(ВИД[к]==='flow');
  var узлы=б.steps.map(function(ш,i){
   return '<li class="nd" data-i="'+i+'"><span class="nd-n">'+('0'+(i+1)).slice(-2)+'</span>'
        +'<span><b>'+экр(ш[0])+'</b><span class="nd-p">'+экр(ш[1])+'</span></span></li>'; }).join('');
  var нужно=(б.need||[]).map(function(x){ return '<li>'+экр(x)+'</li>'; }).join('');
  return '<div class="scheme'+(поток?' scheme-flow':'')+'" data-mode="a">'
   +'<div class="scheme-h"><span class="tag">'+экр(t.scheme||'')+'</span>'
   +(поток?'<span class="scheme-sw"><button type="button" data-mode="a" aria-pressed="true">'
       +экр(t.flow_manual||'')+'</button><button type="button" data-mode="b" aria-pressed="false">'
       +экр(t.flow_auto||'')+'</button></span>':'')+'</div>'
   +'<ol class="scheme-l">'+узлы+'</ol>'
   +(нужно?'<div class="scheme-need"><span>'+экр(t.need_short||'')+'</span><ul>'+нужно+'</ul></div>':'')
   +'<p class="scheme-note">'+экр(поток?(t.flow_note||''):(t.scheme_note||''))+'</p></div>';
 }
 // Иллюстрация направления: одна сцена на задачу, собрана студией.
 function сценаИлл(к){
  var t=PT(), S=DATA[ЯЗЫК].sections, б=S.routes[к]||S.routes[''];
  var файл=(window.ИЛЛЮСТРАЦИЯ||function(){return 'neutral';})(к);
  return '<figure class="ill">'
   +'<div class="ill-img"><img src="/assets/il/'+файл+'.jpg" alt="" decoding="async"></div>'
   +'<figcaption><span class="tag">'+экр(t.scheme||'')+'</span>'
   +экр(б.problem)+'</figcaption></figure>';
 }
 var ключСцены='', счётСцен=0;
 // Ждём, пока снимки новой сцены лягут в кеш. Иначе кадр проявляется пустым,
 // а картинка вскакивает следом — это и читается как моргание.
 function сКартинками(узел, дальше){
  var список=Array.prototype.slice.call(узел.querySelectorAll('img'));
  var осталось=список.length, всё=false;
  function конец(){ if(всё) return; всё=true; дальше(); }
  if(!осталось){ конец(); return; }
  список.forEach(function(и){
   var к=new Image(), раз=false;
   function шаг(){ if(раз) return; раз=true; осталось--; if(осталось<=0) конец(); }
   к.onload=шаг; к.onerror=шаг; к.src=и.getAttribute('src');
   if(к.complete) шаг();
  });
  // Медленная сеть не должна морозить сцену дольше этого.
  window.setTimeout(конец,700);
 }
 function нарисоватьСцену(к, пример){
  var гн=document.getElementById('hm-scene'), пр=document.getElementById('hm-r');
  if(!гн) return;
  if(window.наТему) window.наТему(к, подтверждено);
  var показ = (пример && !БЕЗ_КАРТИНКИ[к]) ? пример : (к ? null : работаИзКаталога());
  var режим = показ ? 'work' : 'scheme';
  if(пр) пр.setAttribute('data-mode',режим);
  var новое = показ ? сценаРабота(показ) : сценаИлл(к);
  if(новое===ключСцены) return;
  ключСцены=новое;
  var мой=++счётСцен, уход=гн.firstElementChild;
  var обёртка=document.createElement('div');
  обёртка.className='сц';
  обёртка.innerHTML=новое;
  if(тонкая){ гн.innerHTML=''; гн.appendChild(обёртка); return; }
  function проявить(снять){
   обёртка.classList.add('сц-новая');
   гн.appendChild(обёртка);
   void обёртка.offsetHeight;
   обёртка.classList.add('on');
   window.setTimeout(function(){
    if(снять) снять();
    // Во вкладке на фоне кадры не идут и переход замирает на нуле. Снимаем
    // переход принудительно, иначе сцена останется невидимой.
    обёртка.style.transition='none';
    обёртка.classList.remove('сц-новая');
    обёртка.classList.remove('on');
    void обёртка.offsetHeight;
    обёртка.style.transition='';
   },1400);
  }
  // Первая сцена проявляется так же, как смена: отдельного пути нет.
  if(!уход){ сКартинками(обёртка,function(){ if(мой===счётСцен) проявить(null); }); return; }
  // Старая гаснет, новая проявляется на её месте — и остаётся ТЕМ ЖЕ узлом.
  // Раньше в конце перехода сцена пересобиралась из разметки: картинка
  // создавалась заново и анимация появления шла по второму кругу.
  сКартинками(обёртка, function(){
   if(мой!==счётСцен) return;
   уход.classList.add('уходит');
   проявить(function(){ if(уход.parentNode===гн) гн.removeChild(уход); });
  });
 }
 document.addEventListener('click',function(ev){
  var д=ev.target.closest('.shot-dev button');
  if(д){ устройство=д.getAttribute('data-dev');
   нарисоватьСцену(тема===null?'':тема, подобратьПример(тема===null?'':тема)); return; }
  var м=ev.target.closest('.scheme-sw button');
  if(м){ var бл=м.closest('.scheme'); бл.setAttribute('data-mode',м.getAttribute('data-mode'));
   бл.querySelectorAll('.scheme-sw button').forEach(function(x){
    x.setAttribute('aria-pressed', x===м?'true':'false'); }); }
 });

 // ------------------------------------------------- вертикаль под направление
 // У каждой задачи свой путь по странице: свой заголовок, своя визуальная
 // модель разбора и своя глубина. Чем больше человек рассказал, тем глубже
 // раздел: сначала путь, потом разбор, потом собранное по его словам.
 function глубина(){
  if(следующийШаг) return 2;
  var n=0; for(var k in подтверждено){ if(подтверждено[k]) n++; }
  return (начали||n>=1) ? 1 : 0;
 }
 function блокПуть(к){
  var S=DATA[ЯЗЫК].sections, L=S.labels, б=S.routes[к]||S.routes[''], t=PT();
  var шаги=б.steps.map(function(ш,i){
   return '<li><b>'+('0'+(i+1)).slice(-2)+'</b><div><h3>'+экр(ш[0])+'</h3><p>'
        +экр(ш[1])+'</p></div></li>'; }).join('');
  var нужно=(б.need||[]).map(function(x){ return '<li>'+экр(x)+'</li>'; }).join('');
  return '<div class="pf-card">'
   +'<div class="pf-card-h"><span class="tag">'+экр(T()['stage_'+глубина()]||'')+'</span></div>'
   +'<ol class="pf-steps">'+шаги+'</ol>'
   +двеКолонки(L,б,нужно)+'</div>';
 }
 // На телефоне два списка подряд удлиняют полосу: там они сворачиваются.
 function двеКолонки(L,б,нужно){
  var тело='<div class="pf-two"><div class="pf-need"><h3>'+экр(L.need)+'</h3><ul>'+нужно+'</ul></div>'
   +'<div class="pf-lim"><h3>'+экр(L.limits)+'</h3><p>'+экр(б.limits)+'</p></div></div>';
  if(window.innerWidth>700) return тело;
  return '<details class="pf-two-d"><summary>'+экр(L.need)+'</summary>'+тело+'</details>';
 }
 function блокПутьКратко(к){
  var S=DATA[ЯЗЫК].sections, L=S.labels, б=S.routes[к]||S.routes[''];
  var нужно=(б.need||[]).map(function(x){ return '<li>'+экр(x)+'</li>'; }).join('');
  return '<div class="pf-card pf-card-min">'
   +'<div class="pf-two"><div class="pf-need"><h3>'+экр(L.need)+'</h3><ul>'+нужно+'</ul></div>'
   +'<div class="pf-lim"><h3>'+экр(L.limits)+'</h3><p>'+экр(б.limits)+'</p></div></div></div>';
 }
 // Разбор: ветвление для денежных задач, поток для операционных, опись для
 // учёта. Везде подписано, что это наш порядок разбора, а не чужое решение.
 function блокРазбор(к){
  var S=DATA[ЯЗЫК].sections, б=S.routes[к]||S.routes[''], t=PT(), вид=ВИД[к]||'steps';
  var имя=T()['view_'+вид]||'';
  var тело='';
  if(вид==='tree'){
   var ветви=(б.need||[]).map(function(x,i){
    return '<li class="br"><span class="br-n">'+('0'+(i+1)).slice(-2)+'</span>'+экр(x)+'</li>'; }).join('');
   тело='<div class="tree"><div class="tree-top">'+экр(б.problem)+'</div>'
     +'<ul class="tree-br">'+ветви+'</ul>'
     +'<div class="tree-end">'+экр(б.steps[3]?б.steps[3][0]:'')+'<span>'
     +экр(б.steps[3]?б.steps[3][1]:'')+'</span></div></div>';
  } else if(вид==='flow'){
   var шаги=б.steps.map(function(ш,i){
    return '<li class="fl" data-i="'+i+'"><b>'+экр(ш[0])+'</b><span>'+экр(ш[1])+'</span></li>'; }).join('');
   тело='<div class="flow" data-mode="a"><div class="flow-h">'
     +'<span class="scheme-sw"><button type="button" data-mode="a" aria-pressed="true">'
     +экр(t.flow_manual||'')+'</button><button type="button" data-mode="b" aria-pressed="false">'
     +экр(t.flow_auto||'')+'</button></span></div><ul class="flow-l">'+шаги+'</ul></div>';
  } else if(вид==='list'){
   var пункты=(б.need||[]).map(function(x){ return '<li>'+экр(x)+'</li>'; }).join('');
   тело='<div class="chk"><ul>'+пункты+'</ul></div>';
  } else if(к){
   // Если ниша названа, в полосе показываем её сцену — она отличается от
   // сцены направления в первом экране.
   var н=нишаКлиента();
   var файл=(н&&ИЛЛ_НИШИ.indexOf(н)>=0)?н:(window.ИЛЛЮСТРАЦИЯ||function(){return 'neutral';})(к);
   тело='<div class="ill-wide"><img src="/assets/il/'+файл+'.jpg" alt="" loading="lazy" decoding="async"></div>';
   имя=имя||экр(б.problem);
  } else {
   тело='';
  }
  if(!тело) return '';
  var сноска = (вид==='tree'||вид==='list') ? (t.scheme_note||'')
             : (вид==='flow' ? (t.flow_note||'') : '');
  return '<div class="pf-visual"><p class="pf-eyebrow">'+экр(имя)+'</p>'+тело
   +(сноска?'<p class="pf-note">'+экр(сноска)+'</p>':'')+'</div>';
 }
 // Что собрано по словам клиента. Ничего не добавляем от себя.
 function блокСобрано(){
  var t=T(), поля=[];
  for(var k in подтверждено){
   var v=подтверждено[k];
   if(v&&String(v).length<120) поля.push(String(v));
  }
  if(!поля.length) return '';
  return '<div class="pf-known"><p class="pf-eyebrow">'+экр(t.known_l||'')+'</p>'
   +'<ul>'+поля.map(function(x){ return '<li>'+экр(x)+'</li>'; }).join('')+'</ul>'
   +(следующийШаг?'<p class="pf-next">'+экр(следующийШаг)+'</p>':'')+'</div>';
 }
 // Примеры решений — часть воронки, а не отдельная витрина: в полосе под
 // задачу показываем подходящие работы и ссылку в галерею с тем же
 // направлением. Если опубликованного примера нет, так и пишем.
 function блокПримеры(к){
  var S=DATA[ЯЗЫК].sections, L=S.labels, б=S.routes[к]||S.routes[''];
  var список=(б.examples||[]).slice(0,2);
  var ссылка='<a class="pf-all" href="'+ссылкаГалереи(к)+'">'+экр(L.all)+' &rarr;</a>';
  if(!список.length){
   // Своего опубликованного примера по этой задаче нет. Если направление
   // закрывает проверенный партнёр — показываем его путь, а не пустую
   // строку. Имя называем только там, где партнёр готов принять задачу.
   // Опубликованного примера по этой задаче нет, но решение есть: показываем,
   // что именно делается по шагам, и сразу даём действие. Имён исполнителей
   // здесь нет — человеку важно, что задача решается.
   var R=(DATA[ЯЗЫК].solve||{})[к];
   if(R){
    var шаги=R.steps.map(function(x,i){
     return '<li><b>'+('0'+(i+1)).slice(-2)+'</b><span>'+экр(x)+'</span></li>'; }).join('');
    return '<div class="pf-solve"><p class="pf-eyebrow">'+экр(DATA[ЯЗЫК].solve_t||'')+'</p>'
     +'<ol class="pf-solve-l">'+шаги+'</ol>'
     +'<p class="pf-note">'+экр(R.limit)+'</p>'
     +'<button type="button" class="pf-main pf-solve-go" data-talk>'+экр(б.cta)+'</button>'
     +'</div>';
   }
   return '<div class="pf-cases"><div class="pf-cases-h"><p class="pf-eyebrow">'
    +экр(L.example)+'</p>'+ссылка+'</div>'
    +'<p class="pf-nocase">'+экр(L.no_case)+'</p></div>';
  }
  var карточки=список.map(function(п){
   return '<a class="pf-case" href="'+п.url+'">'
    +'<span class="pf-case-sh"><img src="'+п.cover+'" alt="'+экр(п.title)+'" '
    +'loading="lazy" decoding="async" width="800" height="500"></span>'
    +'<span class="pf-case-t">'+(п.concept?'<i>'+экр(L.concept)+'</i>':'')
    +экр(п.title)+'</span>'
    +'<span class="pf-case-go">'+экр(L.open)+' &rarr;</span></a>';
  }).join('');
  return '<div class="pf-cases"><div class="pf-cases-h"><p class="pf-eyebrow">'
   +экр(L.example)+'</p>'+ссылка+'</div>'
   +'<div class="pf-case-grid">'+карточки+'</div></div>';
 }
 function собратьРаздел(к){
  var S=DATA[ЯЗЫК].sections, L=S.labels, б=S.routes[к]||S.routes[''];
  var г=глубина();
  return '<div class="pf-v" data-route="'+к+'" data-depth="'+г+'">'
   +'<div class="pf-ph"></div>'
   +'<div class="pf-l"><p class="pf-eyebrow">'+экр(L.path)+'</p>'
   +'<h2 class="pf-h">'+экр(б.problem)+'</h2>'
   +'<p class="pf-lede">'+экр(б.approach)+'</p>'
   +'<span id="how" class="pf-anchor"></span>'
   +'<div class="pf-cta"><button type="button" class="pf-main" data-talk>'
   +экр(б.cta)+'</button><a href="#works">'+экр(L.all)+' &rarr;</a></div>'
   +(к?'':'<p class="pf-note">'+экр(L.hint)+'</p>')+'</div>'
   +'<div class="pf-r">'+блокРазбор(к)+блокПуть(к)+блокПримеры(к)
   +(г>=1?блокСобрано():'')+'</div>'
   +'</div>';
 }
  // Высота полосы меняется переходом и в конце догоняет настоящую высоту
 // содержимого: снятие фиксированной высоты одним кадром давало прыжок.
 // Высота полосы: либо плавный переход, либо изменение сразу в момент
 // нажатия. Отложенный сброс через секунду — это и был прыжок на пол-экрана,
 // поэтому если переход не стартовал за 80 мс, отпускаем высоту немедленно.
 function вестиВысоту(узел, было){
  var стало=узел.scrollHeight;
  if(Math.abs(стало-было)<=24) return;
  var отпущено=false;
  var отпустить=function(){
   if(отпущено) return; отпущено=true;
   узел.style.transition=''; узел.style.height='';
   узел.classList.remove('ведём');
   узел.removeEventListener('transitionend',финал);
   узел.removeEventListener('transitionstart',пошло);
  };
  var финал=function(){
   // Содержимое могло дорасти (картинки) — догоняем коротким переходом.
   var сейчас=узел.scrollHeight;
   if(Math.abs(сейчас-parseFloat(узел.style.height||'0'))>4){
    узел.style.transition='height .35s ease';
    узел.style.height=сейчас+'px';
    window.setTimeout(отпустить,380);
   } else отпустить();
  };
  var стартовал=false;
  var пошло=function(){ стартовал=true; };
  узел.classList.add('ведём');
  узел.style.transition='none';
  узел.style.height=было+'px';
  void узел.offsetHeight;
  узел.addEventListener('transitionstart',пошло);
  узел.addEventListener('transitionend',финал);
  узел.style.transition='height .9s cubic-bezier(.25,.6,.25,1)';
  узел.style.height=стало+'px';
  window.setTimeout(function(){ if(!стартовал) отпустить(); },80);
  window.setTimeout(отпустить,1400);
 }
 function применитьРаздел(к){
  if(!гнездо) return;
  var прокрутка=window.scrollY, фокус=(document.activeElement===поле);
  var старое=гнездо.querySelector('.pf-v');
  // Высоту полосы ведём плавно: иначе всё, что ниже, прыгает рывком.
  // Важно: содержимое может дорасти уже после вставки (картинки), поэтому
  // в конце перехода высота догоняется, а не сбрасывается одним кадром —
  // именно этот сброс и давал прыжок на 477 px.
  var былаВысота=гнездо.getBoundingClientRect().height;
  гнездо.insertAdjacentHTML('afterbegin',собратьРаздел(к));
  if(старое) старое.remove();
  if(былаВысота && !тонкая) вестиВысоту(гнездо, былаВысота);
  тема=к;
  // Страница не должна уехать под рукой: прокрутку и фокус возвращаем.
  нарисоватьСцену(к, подобратьПример(к));
  if(window.scrollY!==прокрутка) window.scrollTo(0,прокрутка);
  if(фокус) поле.focus({preventScroll:true});
  var липкая=document.getElementById('sn-sticky');
  if(липкая){
   // Бесплатную проверку сайта не предлагаем тому, у кого сайта нет, и тому,
   // чья задача не про сайт: это предложение не по адресу.
   var уместна=(к===''||к==='presence')&&!(известноНет==='has_site');
   липкая.setAttribute('data-off',уместна?'0':'1');
   if(!уместна) липкая.hidden=true;
  }
 }
 var известноНет='', подтверждено={}, отпечаток='', следующийШаг='';

 // Галерея открывается с тем же направлением: человек видит примеры по
 // своей задаче, а не весь каталог. Это интерес, а не ответ на вопрос —
 // собранные ответы ссылка не меняет.
 function ссылкаГалереи(к){
  var б=(DATA[ЯЗЫК].sections.labels||{}).gallery_url||'/showcase/';
  return к?(б+'?layer='+encodeURIComponent(к)):б;
 }
 function показатьРаздел(к,известно){
  к=к||'';
  if(известно){ подтверждено=известно;
   if(известно.has_site==='нет') известноНет='has_site'; }
  // Раздел зависит не только от направления: ниша клиента меняет пример, а
  // отсутствие сайта — предложение проверки. Пересобираем, когда меняется
  // что-то из этого, и не трогаем, когда не меняется ничего.
  var новый=к+'|'+(подтверждено.business_type||'')+'|'
           +(подтверждено.what_happened||'')+'|'+(подтверждено.has_site||'')
           +'|'+(подтверждено.demo_id||'');
  if(новый===отпечаток) return;
  отпечаток=новый;
  // Сцена первого экрана обновляется сразу: человек смотрит именно туда,
  // а подмена раздела ниже может быть отложена, если он его читает.
  нарисоватьСцену(к, подобратьПример(к));
  if(к===тема&&тема!==null){
   // Направление то же, изменились подробности — обновляем на месте, без
   // предложения перейти: человек остаётся в том же разделе.
   применитьРаздел(к);
   return;
  }
  if(тема!==null&&тема!==''&&видимРаздел()){
   // Человек читает этот раздел — подменять под рукой нельзя. Предлагаем.
   ждётПоказа=к;
   переклБлок.querySelector('button').textContent=T().show_solutions;
   переклБлок.setAttribute('data-on','1');
   return;
  }
  применитьРаздел(к);
 }
 if(переклБлок){
  переклБлок.querySelector('button').addEventListener('click',function(){
   применитьРаздел(ждётПоказа===null?тема:ждётПоказа); ждётПоказа=null;
   переклБлок.setAttribute('data-on','0');
  });
 }
 // Финальное действие — то же самое продолжение разговора, а не отдельная
 // диагностика с повторными вопросами. После заявки на её месте остаётся
 // состояние обращения.
 var финКнопка=document.getElementById('fin-talk');
 var финСостояние=document.getElementById('fin-state');
 function кРазговору(){
  var я=document.getElementById('hm-hero');
  if(я) я.scrollIntoView({behavior: тонкая?'auto':'smooth', block:'start'});
  window.setTimeout(function(){ поле.focus({preventScroll:true}); }, тонкая?0:420);
 }
 function показатьЗаявку(номер,повтор){
  if(!финСостояние) return;
  финСостояние.textContent=T().saved+'. '+T().saved_p+' #'+номер
   +(повтор?' ('+T().again+')':'');
  финСостояние.hidden=false;
  if(финКнопка) финКнопка.hidden=true;
 }
 if(финКнопка) финКнопка.addEventListener('click',кРазговору);

 if(разделы){
  // «Продолжить разговор» возвращает к тому же диалогу, а не заводит новый.
  разделы.addEventListener('click',function(ev){
   var б=ev.target.closest('[data-talk]'); if(!б) return;
   var я=document.getElementById('hm-hero');
   if(я) я.scrollIntoView({behavior: тонкая?'auto':'smooth', block:'start'});
   window.setTimeout(function(){ поле.focus({preventScroll:true}); }, тонкая?0:420);
  });
  применитьРаздел('');
 }

 // ------------------------------------------------- выбор направления
 // Одно действие на все элементы: чип в первом экране и карточка в сетке
 // «что решаем» делают одно и то же — ставят направление в том же
 // состоянии, которое ведёт разговор. Собранные ответы не стираются.
 var сетка=document.getElementById('layers');
 var выбрано=document.getElementById('layers-picked');
 var выбраноИмя=document.getElementById('layers-name');
 var сменитьСлой=document.getElementById('layers-change');

 // Сетка направлений раньше пропадала целиком — это читалось как рывок.
 // Теперь она остаётся на месте: выбранное помечено, остальные приглушены.
 function свернутьСетку(имя){
  if(!сетка) return;
  сетка.setAttribute('data-picked','1');
  var н=(имя||'').trim().toLowerCase();
  сетка.querySelectorAll('button[data-layer]').forEach(function(б){
   var своё=(б.querySelector('b')||{}).textContent||'';
   var это=(своё.trim().toLowerCase()===н) || (б.getAttribute('data-layer')===тема);
   б.setAttribute('aria-pressed', это?'true':'false');
  });
  if(выбрано) выбрано.hidden=false;
  if(выбраноИмя) выбраноИмя.textContent=имя||'';
  if(сменитьСлой) сменитьСлой.textContent=T().change;
 }
 function развернутьСетку(){
  if(!сетка) return;
  сетка.removeAttribute('data-picked');
  сетка.querySelectorAll('button[data-layer]').forEach(function(б){
   б.setAttribute('aria-pressed','false'); });
  if(выбрано) выбрано.hidden=true;
 }
 async function выбратьНаправление(слой, имя){
  if(занят) return;
  if(ждётВыбора){
   ждётВыбора.querySelectorAll('button').forEach(function(б){ б.remove(); });
   ждётВыбора=null; новаяСессия();
  }
  занят=true;
  var w=ждём();
  try{
   var r=await fetch(API,{method:'POST',headers:{'Content-Type':'application/json'},
     body:JSON.stringify({session:сессия,lang:ЯЗЫК,action:'layer',layer:слой})});
   var d=await r.json(); w.remove();
   if(!d.ok) throw new Error(d.error||'');
   начали=true; поле.placeholder=T().input_next;
   свернутьСетку(имя);
   показатьРаздел(d['тема']||'', d['известно']);
   var р=d['резюме']||[];
   шаг(шагЗадача, р.length?р.join(' · '):T().undefined, р.length?'done':'');
   if(d['вопрос']){
    сказать('bot',d['вопрос'],d['вопрос_ключ']);
    подсказатьК(d['вопрос_ключ']);
    шаг(шагУточн,d['вопрос'],'live');
   }
   var я=document.getElementById('hm-hero');
   if(я) я.scrollIntoView({behavior: тонкая?'auto':'smooth', block:'start'});
   window.setTimeout(function(){ поле.focus({preventScroll:true}); }, тонкая?0:420);
  }catch(e){ w.remove(); сказать('err',T().offline); }
  занят=false;
 }
 if(сетка){
  сетка.addEventListener('click',function(ev){
   var б=ev.target.closest('button[data-layer]'); if(!б) return;
   выбратьНаправление(б.getAttribute('data-layer'),
                      (б.querySelector('b')||{}).textContent||'');
  });
 }
 if(сменитьСлой){
  сменитьСлой.addEventListener('click',function(){ развернутьСетку(); });
 }

 // Пока первый экран на виду, закреплённая кнопка не показывается: поле
 // ввода и отправка не должны быть ничем перекрыты.
 (function(){
  var я=document.getElementById('hm-hero'); if(!я||!window.IntersectionObserver) return;
  new IntersectionObserver(function(записи){
   document.documentElement.classList.toggle('hm-on',записи[0].isIntersecting);
  },{threshold:0.12}).observe(я);
 })();

 function новаяСессия(){
  var н='hm-'+Math.random().toString(36).slice(2,9)+Date.now().toString(36).slice(-4);
  try{ localStorage.setItem('pl-hm-sid',н); }catch(e){}
  сессия=н; начали=false; поле.placeholder=T().input;
 }
 async function восстановить(д){
  начали=true; поле.placeholder=T().input_next;
  шаг(шагДальше,д['следующий']||T().undefined,'live');
  if(д['заявка']) показатьЗаявку(д['заявка_номер']||'',false);
  показатьРаздел(д['задача']||'', д['подтверждено']||{});
 }
 async function подхватить(){
  // Разговор мог идти в прошлый визит или на другой языковой странице.
  // Молча подставлять прошлое состояние нельзя — человек увидит чужое для
  // себя «сейчас». Спрашиваем и ничего не трогаем до ответа.
  try{
   var r=await fetch(STATE_API+'?session='+encodeURIComponent(сессия));
   var d=await r.json();
   if(!d.ok||!d['задача']) return;
   if(d['язык']&&d['язык']!==ЯЗЫК){
    try{
     await fetch(LANG_API,{method:'POST',headers:{'Content-Type':'application/json'},
       body:JSON.stringify({session:сессия,lang:ЯЗЫК})});
    }catch(e){}
   }
   var узел=сказать('note',T().resume_old+'. '+T().resume_q);
   ждётВыбора=узел;
   var да=document.createElement('button');
   да.type='button'; да.className='tr'; да.textContent=T().resume_yes;
   var нет=document.createElement('button');
   нет.type='button'; нет.className='tr'; нет.textContent=T().resume_no;
   узел.appendChild(да); узел.appendChild(нет);
   да.addEventListener('click',function(){
    да.remove(); нет.remove(); ждётВыбора=null; восстановить(d);
   });
   нет.addEventListener('click',function(){
    // Прошлый разговор не удаляем — просто начинаем новый.
    да.remove(); нет.remove(); ждётВыбора=null; новаяСессия();
   });
  }catch(e){}
 }

 рисоватьСписок();
 рисоватьЧипы(набор);
 подхватить();
 if(набор!=='general'&&DATA[ЯЗЫК].sets[набор]){
  ситуация=DATA[ЯЗЫК].sets[набор].main[0][0]; заголовок(ситуация); }
 if(demo){ послать({action:'start',situation:'demo_same',demo:{id:demo,source:'showcase'}}); }
 var строки=[].slice.call(h1.querySelectorAll('.ln>span'));
 if(тонкая){ строки.forEach(function(э){ э.classList.add('in','done'); }); }
 else { window.requestAnimationFrame(function(){ строки.forEach(function(э,i){
   window.setTimeout(function(){ э.classList.add('in'); },40+i*70);
   э.addEventListener('transitionend',function(){ э.classList.add('done'); },{once:true}); }); }); }
})();
"""


def _данные() -> dict:
    """Строки всех языков для страницы.

    Все пять наборов уходят в разметку намеренно: смена языка должна
    происходить без перезагрузки, иначе потеряются история разговора,
    набранный текст и позиция прокрутки.

    В JS тексты идут без HTML-сущностей: там они попадают и в textContent,
    где «&iacute;» осталась бы видна как есть.
    """
    из = {}
    for код in ЯЗЫКИ:
        из[код] = {
            "s": {k: H.unescape(v) for k, v in S[код].items()},
            "h1": H1[код],
            "sets": НАБОРЫ[код],
            "hints": {к: v[код] for к, v in ПОДСКАЗКИ.items()},
            "sections": HS.данные(код),
            "solve": {к: v[код] for к, v in РЕШЕНИЕ.items()},
            "solve_t": РЕШЕНИЕ_ПОДПИСЬ[код],
        }
    return из


def page(code: str = 'ru') -> str:
    d, e = S[code], H.escape
    пара = H1[code]['']
    база = ASSISTANT_API.rstrip('/')
    js = JS % {"api": json.dumps(база),
               "lang_api": json.dumps(f"{база}/lang" if база else ""),
               "lead_api": json.dumps(f"{база}/lead" if база else ""),
               "state_api": json.dumps(f"{база}/state" if база else ""),
               "data": json.dumps(_данные(), ensure_ascii=False),
               "names": json.dumps(ИМЕНА, ensure_ascii=False),
               "langs": json.dumps(list(ЯЗЫКИ)),
               "map": json.dumps(КАМПАНИИ, ensure_ascii=False),
               "lang": json.dumps(code)}
    имя = H.unescape(ИМЕНА[code])
    return f"""<!DOCTYPE html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Prodigy LAB</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<main class="hm">
 <div class="hm-l">
  <a class="hm-brand" href="/">PRODIGY<span>LAB</span></a>
  <span class="hm-mono eyebrow">{d['eyebrow']}</span>
  <h1 id="h1"><span class="ln"><span>{e(пара[0])}</span></span><span class="ln"><span>{e(пара[1])}</span></span></h1>
  <p class="hm-lede">{d['lede']}</p>

  <div class="talk">
   <div class="talk-h">
    <span class="talk-av" aria-hidden="true">PL</span>
    <span class="talk-n">{d['panel']}</span>
    <div class="lang" id="lang">
     <button type="button" id="lang-btn" aria-expanded="false"
             aria-controls="lang-list" aria-label="{e(H.unescape(d['lang_pick']))}">{e(имя)}</button>
     <ul id="lang-list" hidden></ul>
    </div>
   </div>
   <div class="stream" id="stream" aria-live="polite"></div>
   <div class="sugg" id="sugg"></div>
   <form class="ask" id="ask">
    <label for="ask-i" style="position:absolute;left:-9999px">{d['input']}</label>
    <input id="ask-i" type="text" autocomplete="off" enterkeyhint="send"
           placeholder="{e(H.unescape(d['input']))}">
    <button id="ask-b" type="submit" aria-label="{e(H.unescape(d['send']))}">&rarr;</button>
   </form>
  </div>

  <span class="hm-mono hm-pick">{d['pick']}</span>
  <ul class="chips" id="chips"></ul>
  <div class="tail">
   <button type="button" id="restart">{d['other']}</button>
   <a href="/showcase/">{d['more']} &rarr;</a>
  </div>
 </div>

 <div class="hm-r" id="hm-r">
  <div class="hm-face">
   <img src="/assets/founder.jpg" alt="{e(H.unescape(d['founder_alt']))}"
        width="56" height="56" loading="lazy" decoding="async">
   <span>{d['founder_role']}</span>
  </div>
  <div class="hm-steps" id="steps">
   <div class="hm-step" id="s-task"><span class="hm-mono">{d['task']} <i></i></span>
    <p class="dim">{d['undefined']}</p></div>
   <div class="hm-step" id="s-clar"><span class="hm-mono">{d['clarify']} <i></i></span>
    <p class="dim">{d['waiting']}</p></div>
   <div class="hm-step" id="s-next"><span class="hm-mono">{d['nxt']} <i></i></span>
    <p class="dim">{d['undefined']}</p></div>
  </div>
  <div id="hm-scene"></div>
 </div>
</main>
<script>{js}</script>
</body>
</html>"""


# ------------------------------------------------------- встраивание в сайт
# Переменные палитры, общие с сайтом (--accent, --ink, --paper и прочие),
# отсюда не переносятся: у них те же значения, и переопределять их на весь
# сайт незачем. А вот те, которых в сайте нет, объявляются на :root — ими
# пользуется не только первый экран, но и разделы под задачу ниже.
# `--accent2` в сайте уже есть с тем же значением, поэтому его не трогаем.
СВОИ_ПЕРЕМЕННЫЕ = ('--accent-soft', '--graphite', '--graphite2',
                   '--on-dark', '--on-dark2', '--sans', '--mono', '--warn')


def встроенный_css() -> str:
    """CSS первого экрана без блока :root, со своими переменными на секции."""
    корень = re.search(r':root\s*\{([^}]*)\}', CSS)
    свои = []
    if корень:
        for имя, знач in re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;}]+)', корень.group(1)):
            if имя in СВОИ_ПЕРЕМЕННЫЕ:
                свои.append(f'{имя}:{знач.strip()}')
    без = CSS[:корень.start()] + CSS[корень.end():] if корень else CSS
    шапка = ':root{' + ';'.join(свои) + '}\n' if свои else ''
    return шапка + без


def markup(code: str = 'ru', шапка: str = '') -> str:
    """Первый экран: разговор слева, сцена под задачу справа.

    Строки берутся из тех же данных, что ведут разговор, поэтому сервер и
    помощник не расходятся. Фотография направления подставляется скриптом.
    """
    d = _данные()[code]['s']
    h1 = _данные()[code]['h1']['']
    e = H.escape
    return f'''<section id="hm-hero"><span id="start" class="hm-anchor"></span>
 <div class="hero-ph" id="hero-ph"></div>
 <div class="hero-in">
  <div class="hero-l">
   {шапка}
   <p class="eyebrow">{e(d['eyebrow'])}</p>
   <h1 id="h1"><span class="ln"><span>{e(h1[0])}</span></span><span class="ln"><span>{e(h1[1])}</span></span></h1>
   <p class="hm-lede">{e(d['lede'])}</p>
   <div class="talk">
    <div class="talk-h">
     <span class="talk-n">{e(d['panel'])}</span>
     <div class="lang" id="lang">
      <button type="button" id="lang-btn" aria-expanded="false" aria-haspopup="true"
              aria-label="{e(d['lang_pick'])}">{e(ИМЕНА[code])}</button>
      <ul id="lang-list" hidden></ul>
     </div>
    </div>
    <div class="stream" id="stream" data-hint="{e(d['hint_start'])}"></div>
    <div class="sugg" id="sugg"></div>
    <form id="ask" autocomplete="off">
     <label class="vh" for="ask-i">{e(d['input'])}</label>
     <input id="ask-i" type="text" autocomplete="off" placeholder="{e(d['input'])}">
     <button id="ask-b" type="submit" aria-label="{e(d['send'])}">&rarr;</button>
    </form>
   </div>
   <ul class="chips" id="chips"></ul>
   <p class="hm-pick vh">{e(d['pick'])}</p>
   <div class="tail">
    <button type="button" id="restart">{e(d['other'])}</button>
    <a href="#works" id="tail-more">{e(d['more'])} &rarr;</a>
   </div>
  </div>
  <div class="hero-r" id="hm-r" data-mode="idle">
   <div class="steps" id="steps">
    <div class="hm-step" id="s-task"><span class="hm-mono">{e(d['task'])} <i></i></span><p class="dim">&#8212;</p></div>
    <div class="hm-step" id="s-clar"><span class="hm-mono">{e(d['clarify'])} <i></i></span><p class="dim">&#8212;</p></div>
    <div class="hm-step" id="s-next"><span class="hm-mono">{e(d['nxt'])} <i></i></span><p class="dim">&#8212;</p></div>
   </div>
   <div id="hm-scene"></div>
  </div>
 </div>
</section>'''


def script(code: str = 'ru') -> str:
    целиком = page(code)
    начало = целиком.index('<script>') + len('<script>')
    конец = целиком.index('</script>', начало)
    return целиком[начало:конец]


if __name__ == '__main__':
    import pathlib
    out = pathlib.Path(os.environ.get(
        "PL_HERO_OUT", "/private/tmp/claude-501/-Users-sashagun-Desktop/"
        "779e658d-5d00-4262-bad0-4bf3d1f4f4c0/scratchpad/hero"))
    out.mkdir(parents=True, exist_ok=True)
    for c in ЯЗЫКИ:
        p = out / f'hero-{c}.html'
        p.write_text(page(c), encoding='utf-8')
        print(f'  ✓ {p.name}  {len(p.read_text(encoding="utf-8"))//1024} КБ')
