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

from hero_content import (ИМЕНА, КАМПАНИИ, ЯЗЫКИ, H1, НАБОРЫ, ПОДСКАЗКИ,  # noqa: E402
                          S)

CSS = """
/* Переключатель языка в шапке диалога. Названия языков — на своём языке,
   без флагов. Кнопка узкая, список раскрывается на месте и не растягивает
   шапку: иначе диалог дёргался бы при каждом открытии. */
.lang{margin-left:auto;position:relative}
.lang>button{font:500 12.5px/1 var(--mono);letter-spacing:.06em;color:var(--ink2);
 background:transparent;border:1px solid var(--line);padding:6px 9px;cursor:pointer}
.lang>button:hover{color:var(--ink);border-color:var(--ink3)}
.lang>button[aria-expanded="true"]{color:var(--ink);border-color:var(--accent)}
.lang ul{position:absolute;right:0;top:calc(100% + 5px);z-index:5;margin:0;padding:4px;
 list-style:none;background:#fff;border:1px solid var(--line);min-width:132px}
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
--warn:#8A5A1C}
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
.hm-steps{display:grid;gap:9px;grid-template-columns:1fr;
transform:translate3d(var(--dx,0),var(--dy,0),0);transition:transform .3s ease-out}
@media(min-width:640px){.hm-steps{grid-template-columns:repeat(3,1fr)}}
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
 var занят=false, начали=false;
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
  p.textContent=текст;
  p.classList.toggle('dim',!текст||текст===T().undefined||текст===T().waiting);
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
  var пусто=['eyebrow','lede','pick','other','more','panel'];
  document.querySelector('.eyebrow').innerHTML=d.eyebrow;
  document.querySelector('.hm-lede').innerHTML=d.lede;
  document.querySelector('.hm-pick').innerHTML=d.hm-pick;
  сменить.innerHTML=d.other;
  var ссылка=document.querySelector('.tail a');
  if(ссылка) ссылка.innerHTML=d.more+' &rarr;';
  document.querySelector('.talk-n').innerHTML=d.panel;
  поле.placeholder=начали?d.input_next:d.input;
  кнопка.setAttribute('aria-label',d.send);
  document.querySelector('label[for="ask-i"]').innerHTML=d.input;
  кнЯз.textContent=NAMES[новый];
  кнЯз.setAttribute('aria-label',d.lang_pick);
  document.querySelector('#s-task .hm-mono').innerHTML=d.task+' <i></i>';
  document.querySelector('#s-clar .hm-mono').innerHTML=d.clarify+' <i></i>';
  document.querySelector('#s-next .hm-mono').innerHTML=d.nxt+' <i></i>';
  var сн=document.querySelector('.hm-shot figcaption');
  if(сн) сн.innerHTML='<span class="tag">'+d.sample+'</span>'+d.sample_cap;
  // Подписи «Вы» и «Помощник» — наши, их обновляем. Текст реплик клиента
  // не трогаем ни при каких условиях: это его слова.
  поток.querySelectorAll('.m-you>b').forEach(function(b){ b.textContent=d.you; });
  поток.querySelectorAll('.m-bot>b').forEach(function(b){ b.textContent=d.bot; });
  рисоватьЧипы(ситуация?набор:набор);
  рисоватьСписок();
  заголовок(ситуация,true);
  подсказатьК(ключВопроса);
  if(финалБлок) обновитьФинал();
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

 async function подхватить(){
  // Разговор мог начаться на другой языковой странице. Переписку сервер не
  // хранит для показа, поэтому восстанавливаем состояние, а не ленту: что
  // за задача, что уже выяснено и какой следующий шаг.
  try{
   var r=await fetch(STATE_API+'?session='+encodeURIComponent(сессия));
   var d=await r.json();
   if(!d.ok||!d['задача']) return;
   начали=true; поле.placeholder=T().input_next;
   if(d['язык']&&d['язык']!==ЯЗЫК) применитьЯзык(d['язык']);
   шаг(шагДальше,d['следующий']||T().undefined,'live');
   сказать('note',T().kept);
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
  <div class="hm-steps" id="steps">
   <div class="hm-step" id="s-task"><span class="hm-mono">{d['task']} <i></i></span>
    <p class="dim">{d['undefined']}</p></div>
   <div class="hm-step" id="s-clar"><span class="hm-mono">{d['clarify']} <i></i></span>
    <p class="dim">{d['waiting']}</p></div>
   <div class="hm-step" id="s-next"><span class="hm-mono">{d['nxt']} <i></i></span>
    <p class="dim">{d['undefined']}</p></div>
  </div>
  <figure class="hm-shot">
   <img src="{ОБРАЗЕЦ}" alt="{e(H.unescape(d['sample_cap']))}" loading="lazy"
        decoding="async" width="800" height="500">
   <figcaption><span class="tag">{d['sample']}</span>{d['sample_cap']}</figcaption>
  </figure>
 </div>
</main>
<script>{js}</script>
</body>
</html>"""


# ------------------------------------------------------- встраивание в сайт
# На главной уже есть свои переменные палитры с теми же значениями, поэтому
# блок `:root` отсюда не переносится: он бы переопределял их на весь сайт.
# Свои переменные первого экрана объявляются на его же контейнере.
СВОИ_ПЕРЕМЕННЫЕ = ('--accent-soft', '--accent2', '--graphite', '--graphite2',
                   '--on-dark', '--on-dark2', '--sans', '--mono', '--warn')


def встроенный_css() -> str:
    """CSS первого экрана без блока :root, со своими переменными на секции."""
    корень = re.search(r':root\s*\{([^}]*)\}', CSS)
    свои = []
    if корень:
        for имя, знач in re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', корень.group(1)):
            if имя in СВОИ_ПЕРЕМЕННЫЕ:
                свои.append(f'{имя}:{знач.strip()}')
    без = CSS[:корень.start()] + CSS[корень.end():] if корень else CSS
    шапка = '#hm-hero{' + ';'.join(свои) + '}\n' if свои else ''
    return шапка + без


def markup(code: str = 'ru') -> str:
    """Разметка первого экрана как секции страницы."""
    целиком = page(code)
    начало = целиком.index('<main class="hm">')
    конец = целиком.index('</main>', начало) + len('</main>')
    тело = целиком[начало:конец].replace('<main class="hm">', '<div class="hm">', 1)
    тело = тело[:тело.rindex('</main>')] + '</div>'
    # Логотип в шапке сайта уже есть; второй подряд читается как ошибка вёрстки.
    начало = тело.find('<a class="hm-brand"')
    if начало >= 0:
        конец = тело.index('</a>', начало) + 4
        тело = тело[:начало] + тело[конец:]
    return f'<section id="hm-hero">\n{тело}\n</section>'


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
