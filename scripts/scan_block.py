# -*- coding: utf-8 -*-
"""Вход в бесплатную AI-проверку сайта: один компонент на все точки главной.

Зачем отдельным файлом. Вход в скан стоит в пяти местах: в шапке, на первом
экране, отдельным блоком, после галереи и внизу страницы. Если каждую кнопку
писать по месту, через месяц они разъедутся по тексту, адресу и меткам. Здесь
одна ссылка, один набор формулировок и один стиль.

ВАЖНО про адрес. Скан живёт на `/scan`, а `/diagnostic` — это другой сценарий:
там человек описывает проблему бизнеса словами, и сайт он может не называть
вовсе. Называть разбор сканированием сайта нельзя, это разные обещания.

Честность формулировок. Скан смотрит одну страницу и показывает результат
сразу на той же странице, но перед показом спрашивает имя, почту и телефон.
Поэтому «без регистрации» мы не обещаем нигде.
"""
import html as H
import os

# Боевой адрес скана. Переопределяется только для локального прогона воронки
# (PL_SCAN_BASE=http://localhost:4455/scan), чтобы можно было пройти путь
# целиком, не трогая боевой сервис. В сборке для публикации переменной нет.
SCAN_BASE = os.environ.get("PL_SCAN_BASE", "https://scan.prodigylab.studio/scan")
SCAN_LANG = {'en': 'en', 'ru': 'ru', 'es': 'es', 'pt': 'pt', 'de': 'de'}


def scan_url(code: str, place: str) -> str:
    """Ссылка на скан с языком и меткой места, откуда нажали.

    Метки те же, что уже понимает лендинг: он читает utm_* из адреса и кладёт
    их в заявку. Новых параметров не выдумываем.
    """
    return (f"{SCAN_BASE}?lang={SCAN_LANG.get(code, 'en')}"
            f"&amp;utm_source=site&amp;utm_medium={place}&amp;utm_campaign=free_scan")


S = {
 'en': dict(
   nav='Free site check',
   eyebrow='FREE AI WEBSITE CHECK',
   h2='What is stopping your site from bringing enquiries?',
   lede='Paste your address. We read the page the way a first-time visitor does and show '
        'what we found, what is only worth a look, and one change you can make the same day.',
   cta='Check my site free',
   step1='You give the address of your site.',
   step2='We ask your name, email and phone — the result opens right after that, on the same page.',
   step3='You get the findings, each marked by how sure we are, and one ready-to-paste change.',
   note='One page is checked. No access to your site, no card, no call.',
   after_gallery_h='And what could be better on your site?',
   after_gallery_p='The same check, on your address.',
   example_cap='An example of the result. The site in it is made up, the layout is the real one.',
   sticky='Check my site free',
 ),
 'ru': dict(
   nav='Проверить сайт',
   eyebrow='БЕСПЛАТНАЯ AI-ПРОВЕРКА САЙТА',
   h2='Что мешает вашему сайту приносить обращения?',
   lede='Вставьте адрес. Мы читаем страницу так, как её читает новый посетитель, и показываем, '
        'что нашли, что лишь стоит посмотреть и одно изменение, которое можно сделать в тот же день.',
   cta='Проверить сайт бесплатно',
   step1='Вы даёте адрес своего сайта.',
   step2='Спрашиваем имя, почту и телефон — сразу после этого результат открывается на той же странице.',
   step3='Получаете находки, каждая с пометкой, насколько мы в ней уверены, и одно готовое изменение.',
   note='Проверяется одна страница. Без доступов к сайту, без карты, без звонка.',
   after_gallery_h='А что можно улучшить на вашем сайте?',
   after_gallery_p='Та же проверка, по вашему адресу.',
   example_cap='Пример результата. Сайт в нём выдуманный, вёрстка настоящая.',
   sticky='Проверить сайт',
 ),
 'es': dict(
   nav='Revisar mi sitio',
   eyebrow='REVISI&Oacute;N GRATUITA DEL SITIO',
   h2='&iquest;Qu&eacute; impide que su sitio traiga consultas?',
   lede='Pegue su direcci&oacute;n. Leemos la p&aacute;gina como la lee un visitante nuevo y mostramos '
        'qu&eacute; encontramos, qu&eacute; conviene revisar y un cambio que puede hacer el mismo d&iacute;a.',
   cta='Revisar mi sitio gratis',
   step1='Usted indica la direcci&oacute;n de su sitio.',
   step2='Pedimos nombre, correo y tel&eacute;fono: el resultado se abre justo despu&eacute;s, en la misma p&aacute;gina.',
   step3='Recibe los hallazgos, cada uno con su grado de certeza, y un cambio listo para pegar.',
   note='Se revisa una p&aacute;gina. Sin accesos, sin tarjeta, sin llamada.',
   after_gallery_h='&iquest;Y qu&eacute; se puede mejorar en su sitio?',
   after_gallery_p='La misma revisi&oacute;n, con su direcci&oacute;n.',
   example_cap='Ejemplo del resultado. El sitio es inventado; el dise&ntilde;o, real.',
   sticky='Revisar gratis',
 ),
 'pt': dict(
   nav='Verificar meu site',
   eyebrow='VERIFICA&Ccedil;&Atilde;O GRATUITA DO SITE',
   h2='O que impede seu site de trazer contatos?',
   lede='Cole o endere&ccedil;o. Lemos a p&aacute;gina como um visitante novo a l&ecirc; e mostramos o que '
        'encontramos, o que vale olhar e uma mudan&ccedil;a que d&aacute; para fazer no mesmo dia.',
   cta='Verificar meu site de gra&ccedil;a',
   step1='Voc&ecirc; informa o endere&ccedil;o do seu site.',
   step2='Pedimos nome, e-mail e telefone: o resultado abre logo depois, na mesma p&aacute;gina.',
   step3='Recebe os achados, cada um com o grau de certeza, e uma mudan&ccedil;a pronta para colar.',
   note='Uma p&aacute;gina &eacute; verificada. Sem acessos, sem cart&atilde;o, sem liga&ccedil;&atilde;o.',
   after_gallery_h='E o que d&aacute; para melhorar no seu site?',
   after_gallery_p='A mesma verifica&ccedil;&atilde;o, no seu endere&ccedil;o.',
   example_cap='Exemplo do resultado. O site &eacute; fict&iacute;cio; o layout, real.',
   sticky='Verificar de gra&ccedil;a',
 ),
 'de': dict(
   nav='Website pr&uuml;fen',
   eyebrow='KOSTENLOSE KI-PR&Uuml;FUNG DER WEBSITE',
   h2='Was h&auml;lt Ihre Website davon ab, Anfragen zu bringen?',
   lede='F&uuml;gen Sie Ihre Adresse ein. Wir lesen die Seite so, wie ein neuer Besucher sie liest, und '
        'zeigen, was wir gefunden haben, was einen Blick wert ist und eine &Auml;nderung f&uuml;r heute.',
   cta='Website kostenlos pr&uuml;fen',
   step1='Sie geben die Adresse Ihrer Website an.',
   step2='Wir fragen Name, E-Mail und Telefon — direkt danach &ouml;ffnet sich das Ergebnis auf derselben Seite.',
   step3='Sie erhalten die Befunde, jeweils mit unserer Sicherheit, und eine fertige &Auml;nderung.',
   note='Gepr&uuml;ft wird eine Seite. Ohne Zug&auml;nge, ohne Karte, ohne Anruf.',
   after_gallery_h='Und was l&auml;sst sich auf Ihrer Website verbessern?',
   after_gallery_p='Dieselbe Pr&uuml;fung, mit Ihrer Adresse.',
   example_cap='Beispielergebnis. Die Website darin ist erfunden, das Layout echt.',
   sticky='Kostenlos pr&uuml;fen',
 ),
}

EXAMPLE_IMG = '/assets/scan-example.jpg'

CSS = """
.sn-btn{display:inline-flex;align-items:center;gap:8px;background:var(--accent);color:#fff;
border:0;border-radius:3px;padding:15px 26px;font:inherit;font-size:15px;font-weight:500;
text-decoration:none;line-height:1;transition:background .15s,transform .15s}
.sn-btn:hover{background:var(--accent2);transform:translateY(-1px)}
.sn-btn:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
/* Две кнопки в шапке помещаются не везде. До 1180px показываем только проверку
   сайта — она теперь основное действие; разбор остаётся в меню и на странице. */
.sn-nav{display:none;background:var(--accent);color:#fff;border-radius:3px;padding:10px 16px;
font-size:13px;text-decoration:none;white-space:nowrap}
.sn-nav:hover{background:var(--accent2)}
@media(min-width:860px){.sn-nav{display:inline-block}}
@media(max-width:1179px){.nav-cta{display:none!important}}
.nav-cta{white-space:nowrap}
.sn{padding:78px 0;background:var(--ink);color:#fff;border-top:1px solid var(--line)}
.sn .mono{color:#9FD3D6}
.sn h2{font-size:clamp(28px,4.4vw,44px);line-height:1.08;letter-spacing:-.025em;margin:14px 0 0;
max-width:19ch}
.sn-lede{color:#C9C9C5;max-width:52ch;margin:18px 0 0;font-size:17px}
.sn-grid{display:grid;gap:34px;grid-template-columns:1fr;align-items:start;margin-top:34px}
@media(min-width:900px){.sn-grid{grid-template-columns:1fr 1fr;gap:48px}}
.sn-steps{list-style:none;margin:0 0 26px;padding:0;display:flex;flex-direction:column;gap:12px}
.sn-steps li{display:flex;gap:12px;color:#E4E4E0;font-size:15px;line-height:1.5}
.sn-steps b{flex:none;width:22px;height:22px;border-radius:50%;background:#2C2C2C;color:#9FD3D6;
font-size:12px;display:inline-flex;align-items:center;justify-content:center;margin-top:1px}
.sn-note{margin:16px 0 0;font-size:13px;color:#8A8A86}
.sn-shot{margin:0;border:1px solid #2C2C2C;border-radius:4px;overflow:hidden;background:#1A1A1A}
.sn-shot img{display:block;width:100%;height:auto}
.sn-shot figcaption{padding:10px 14px;font-size:12px;color:#8A8A86;border-top:1px solid #2C2C2C}
.sn-after{padding:54px 0;border-top:1px solid var(--line)}
.sn-after h2{font-size:clamp(22px,3vw,30px);line-height:1.15;letter-spacing:-.02em;margin:0}
.sn-after p{color:var(--ink2);margin:10px 0 20px}
.sn-sticky{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;display:flex}
.sn-sticky a{flex:1;justify-content:center;box-shadow:0 6px 24px rgba(0,0,0,.22)}
@media(min-width:760px){.sn-sticky{display:none}}
"""


def nav_button(code: str) -> str:
    """Компактная кнопка в шапке."""
    return (f'<a class="sn-nav" href="{scan_url(code, "header")}">'
            f'{S[code]["nav"]}</a>')


def main_block(code: str) -> str:
    """Основной блок: две колонки на компьютере, последовательный на телефоне."""
    d = S[code]
    шаги = "".join(f'<li><b>{i}</b><span>{d[f"step{i}"]}</span></li>' for i in (1, 2, 3))
    return f"""
<section class="sn" id="scan">
 <div class="wrap">
  <span class="mono">{d['eyebrow']}</span>
  <h2>{d['h2']}</h2>
  <p class="sn-lede">{d['lede']}</p>
  <div class="sn-grid">
   <div>
    <ul class="sn-steps">{шаги}</ul>
    <a class="sn-btn" href="{scan_url(code, 'main_block')}">{d['cta']} &rarr;</a>
    <p class="sn-note">{d['note']}</p>
   </div>
   <figure class="sn-shot">
    <img src="{EXAMPLE_IMG}" alt="{H.escape(_plain(d['example_cap']))}"
         loading="lazy" decoding="async" width="900" height="1500">
    <figcaption>{d['example_cap']}</figcaption>
   </figure>
  </div>
 </div>
</section>"""


def after_gallery(code: str) -> str:
    """Короткий переход от чужих примеров к своему сайту."""
    d = S[code]
    return f"""
<section class="sn-after">
 <div class="wrap">
  <h2>{d['after_gallery_h']}</h2>
  <p>{d['after_gallery_p']}</p>
  <a class="sn-btn" href="{scan_url(code, 'after_gallery')}">{d['cta']} &rarr;</a>
 </div>
</section>"""


def sticky(code: str) -> str:
    """Закреплённая кнопка на телефоне. Прячется, когда виден основной блок,
    чтобы не стоять поверх того же предложения."""
    return (f'<div class="sn-sticky" id="sn-sticky" hidden>'
            f'<a class="sn-btn" href="{scan_url(code, "sticky")}">{S[code]["sticky"]}</a></div>')


STICKY_JS = """
// Закреплённую кнопку показываем, когда человек ушёл с первого экрана, и
// прячем, когда на виду сам блок скана: два одинаковых призыва на одном
// экране — это не настойчивость, а шум.
(function(){
 var кнопка=document.getElementById('sn-sticky'); if(!кнопка) return;
 var блок=document.getElementById('scan'), низ=document.getElementById('diagnostic');
 var рядом=false;
 if('IntersectionObserver' in window){
  var глаз=new IntersectionObserver(function(записи){
   рядом=записи.some(function(з){return з.isIntersecting;}); решить();
  },{rootMargin:'-10% 0px -10% 0px'});
  [блок,низ].forEach(function(э){ if(э) глаз.observe(э); });
 }
 function решить(){
  var ушли=window.scrollY>window.innerHeight*0.9;
  кнопка.hidden=!(ушли&&!рядом);
 }
 window.addEventListener('scroll',решить,{passive:true});
 решить();
})();
"""


def _plain(text: str) -> str:
    import re
    from html import unescape
    return unescape(re.sub(r'<[^>]+>', '', text))
