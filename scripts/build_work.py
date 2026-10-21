# -*- coding: utf-8 -*-
"""Короткие описания работ на нашем домене.

Демо по адресу `/preview/<slug>/` — это сама работа, а не рассказ о ней.
Человеку, который пришёл из галереи или из разговора, нужен один экран:
какая была задача, что в демо сделано и какие у этого границы. Отсюда есть
переход в работающую демонстрацию.

Результатов здесь нет и не будет, пока их нечем подтвердить: оба примера —
концепты студии, а не заказы клиентов, и на самих демо это написано.
Выдумывать рост конверсии к концепту нельзя.

Источник — тот же SHOWCASE.json, второго каталога не заводим.
"""
from __future__ import annotations

import html as H
import json
import os

КОРЕНЬ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ЯЗЫКИ = ("en", "ru", "es", "pt", "de")
ПУТЬ = {'en': '/work/', 'ru': '/ru/work/', 'es': '/es/work/',
        'pt': '/pt/work/', 'de': '/de/work/'}
ГАЛЕРЕЯ = {'en': '/showcase/', 'ru': '/ru/showcase/', 'es': '/es/showcase/',
           'pt': '/pt/showcase/', 'de': '/de/showcase/'}
ГЛАВНАЯ = {'en': '/', 'ru': '/ru/', 'es': '/es/', 'pt': '/pt/', 'de': '/de/'}

ПОДПИСИ = {
 'ru': dict(eyebrow='Работа студии', task='Задача', done='Что сделано',
            limits='Границы', demo='Открыть демонстрацию',
            back='Все примеры', talk='Обсудить похожее',
            concept='Концепт студии', title_suffix='— Prodigy LAB'),
 'en': dict(eyebrow='Studio work', task='The task', done='What was built',
            limits='Boundaries', demo='Open the demo',
            back='All examples', talk='Discuss something similar',
            concept='Studio concept', title_suffix='— Prodigy LAB'),
 'es': dict(eyebrow='Trabajo del estudio', task='La tarea', done='Qué se hizo',
            limits='Límites', demo='Abrir la demo',
            back='Todos los ejemplos', talk='Hablar de algo similar',
            concept='Concepto del estudio', title_suffix='— Prodigy LAB'),
 'pt': dict(eyebrow='Trabalho do estúdio', task='A tarefa', done='O que foi feito',
            limits='Limites', demo='Abrir a demo',
            back='Todos os exemplos', talk='Falar de algo parecido',
            concept='Conceito do estúdio', title_suffix='— Prodigy LAB'),
 'de': dict(eyebrow='Studio-Arbeit', task='Die Aufgabe', done='Was gebaut wurde',
            limits='Grenzen', demo='Demo öffnen',
            back='Alle Beispiele', talk='Ähnliches besprechen',
            concept='Studio-Konzept', title_suffix='— Prodigy LAB'),
}


# Тексты про сами концепты. Написаны по тому, что в демо действительно есть,
# и по описанию из каталога. Ни одной цифры результата здесь нет.
ТЕКСТЫ = {
 'saeng-thai-house': {
  'ru': dict(
   task='Ресторан судят по витрине. Гость с телефона хочет увидеть блюда, цены '
        'и понять, как забрать заказ, — а не звонить и уточнять.',
   done='Концепт витрины: каждое блюдо со своим снимком, ценой и опциями, '
        'раздел «что берут чаще», часы работы и путь к самовывозу. Заказ при '
        'этом остаётся в сервисе самого ресторана — мы его не подменяем.',
   limits='Это независимый концепт студии, а не заказ ресторана и не его '
          'официальный сайт; так и подписано на самой странице. Снимки блюд '
          'иллюстративные, заказы не принимаются. Результатов по этому примеру '
          'у нас нет, и приписывать их мы не будем.'),
  'en': dict(
   task='A restaurant is judged by its storefront. A guest on a phone wants to '
        'see the dishes and prices and understand how pickup works — not call '
        'to ask.',
   done='A storefront concept: every dish with its own photo, price and '
        'options, a “what people order” section, opening hours and the path to '
        'pickup. The order itself stays in the restaurant’s own service — we do '
        'not replace it.',
   limits='This is an independent studio concept, not an order from the '
          'restaurant and not its official site; the page says so itself. Food '
          'imagery is illustrative and no orders are taken. We have no results '
          'for this example and will not claim any.'),
  'es': dict(
   task='A un restaurante se le juzga por su escaparate. El cliente quiere ver '
        'los platos y precios en el móvil y entender cómo es la recogida, no '
        'llamar para preguntar.',
   done='Concepto de escaparate: cada plato con su foto, precio y opciones, una '
        'sección de lo más pedido, horarios y el camino a la recogida. El pedido '
        'se queda en el servicio del propio restaurante.',
   limits='Es un concepto independiente del estudio, no un encargo del '
          'restaurante ni su sitio oficial; así lo dice la propia página. Las '
          'fotos son ilustrativas y no se aceptan pedidos. No tenemos resultados '
          'de este ejemplo y no vamos a atribuirlos.'),
  'pt': dict(
   task='Um restaurante é julgado pela vitrine. O cliente no celular quer ver os '
        'pratos e preços e entender como é a retirada, não ligar para perguntar.',
   done='Conceito de vitrine: cada prato com sua foto, preço e opções, uma seção '
        'do que mais pedem, horários e o caminho até a retirada. O pedido em si '
        'fica no serviço do próprio restaurante.',
   limits='É um conceito independente do estúdio, não um pedido do restaurante '
          'nem o site oficial dele; a própria página diz isso. As fotos são '
          'ilustrativas e pedidos não são aceitos. Não temos resultados deste '
          'exemplo e não vamos atribuí-los.'),
  'de': dict(
   task='Ein Restaurant wird an seiner Auslage gemessen. Der Gast am Telefon '
        'will Gerichte und Preise sehen und verstehen, wie die Abholung läuft — '
        'nicht anrufen und nachfragen.',
   done='Ein Auslagen-Konzept: jedes Gericht mit eigenem Foto, Preis und '
        'Optionen, ein Abschnitt „was bestellt wird“, Öffnungszeiten und der Weg '
        'zur Abholung. Die Bestellung selbst bleibt im Dienst des Restaurants.',
   limits='Das ist ein eigenständiges Studio-Konzept, kein Auftrag des '
          'Restaurants und nicht dessen offizielle Seite; die Seite sagt das '
          'selbst. Die Bilder sind illustrativ, Bestellungen werden nicht '
          'angenommen. Ergebnisse zu diesem Beispiel haben wir nicht.'),
 },
 'neighborhood-fence': {
  'ru': dict(
   task='Подрядчику по заборам звонят с вопросом «сколько стоит», и разговор '
        'уходит на уточнения: какой тип работ, материал, длина, высота, нужны '
        'ли ворота и демонтаж.',
   done='Концепт планировщика: хозяин дома сам выбирает тип работ, материал, '
        'стиль, длину, высоту, ворота и демонтаж и получает понятное описание '
        'проекта для разговора с подрядчиком. Одна опубликованная вилка цены с '
        'ясными границами. Никуда ничего не уходит.',
   limits='Это независимый концепт студии, а не заказ компании и не её '
          'официальный сайт; так и подписано на странице. Цены в планировщике '
          'иллюстративные, заявки не отправляются. Результатов по этому примеру '
          'у нас нет.'),
  'en': dict(
   task='A fence contractor gets “how much does it cost” calls, and the '
        'conversation turns into clarifying: type of work, material, length, '
        'height, gates and demolition.',
   done='A planner concept: the homeowner picks the type of work, material, '
        'style, length, height, gates and demolition, and gets a clear project '
        'description to take into the conversation with the contractor. One '
        'published price range with stated limits. Nothing is submitted anywhere.',
   limits='This is an independent studio concept, not an order from the company '
          'and not its official site; the page says so. Prices in the planner '
          'are illustrative and no requests are sent. We have no results for '
          'this example.'),
  'es': dict(
   task='Al instalador de cercas le llaman para preguntar el precio y la '
        'conversación se va en aclarar: tipo de trabajo, material, longitud, '
        'altura, puertas y demolición.',
   done='Concepto de planificador: el dueño elige tipo de trabajo, material, '
        'estilo, longitud, altura, puertas y demolición y obtiene una '
        'descripción clara del proyecto para hablar con el instalador. Una '
        'horquilla de precio publicada con límites claros. No se envía nada.',
   limits='Es un concepto independiente del estudio, no un encargo de la empresa '
          'ni su sitio oficial; la página lo dice. Los precios del planificador '
          'son ilustrativos y no se envían solicitudes. No tenemos resultados de '
          'este ejemplo.'),
  'pt': dict(
   task='O instalador de cercas recebe ligações perguntando o preço, e a '
        'conversa vira esclarecimento: tipo de trabalho, material, comprimento, '
        'altura, portões e demolição.',
   done='Conceito de planejador: o dono da casa escolhe tipo de trabalho, '
        'material, estilo, comprimento, altura, portões e demolição e recebe uma '
        'descrição clara do projeto para conversar com o instalador. Uma faixa '
        'de preço publicada com limites claros. Nada é enviado.',
   limits='É um conceito independente do estúdio, não um pedido da empresa nem o '
          'site oficial dela; a página diz isso. Os preços do planejador são '
          'ilustrativos e solicitações não são enviadas. Não temos resultados '
          'deste exemplo.'),
  'de': dict(
   task='Beim Zaunbauer rufen Leute an und fragen nach dem Preis, und das '
        'Gespräch geht im Klären auf: Art der Arbeit, Material, Länge, Höhe, '
        'Tore und Abriss.',
   done='Ein Planer-Konzept: der Hausbesitzer wählt Art der Arbeit, Material, '
        'Stil, Länge, Höhe, Tore und Abriss und bekommt eine klare '
        'Projektbeschreibung für das Gespräch mit dem Handwerker. Eine '
        'veröffentlichte Preisspanne mit klaren Grenzen. Es wird nichts '
        'abgeschickt.',
   limits='Das ist ein eigenständiges Studio-Konzept, kein Auftrag der Firma und '
          'nicht deren offizielle Seite; die Seite sagt das. Die Preise im Planer '
          'sind illustrativ, Anfragen werden nicht gesendet. Ergebnisse zu diesem '
          'Beispiel haben wir nicht.'),
 },
}


CSS = """
:root{--ink:#121212;--ink2:#5C5C5A;--ink3:#8A8A86;--paper:#FBFBF9;--paper2:#F3F2EE;
--line:#E2E1DC;--accent:#1C7E84;--accent2:#0F4A4E;
--sans:Geist,system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);background:#fff}
header .wrap{display:flex;align-items:center;justify-content:space-between;
min-height:64px;gap:16px}
.brand{font-weight:700;letter-spacing:-.02em;color:var(--ink);text-decoration:none}
.brand b{color:var(--accent)}
.langs{display:flex;gap:0}
.langs a{font:500 11px/1 var(--mono);letter-spacing:.08em;color:var(--ink3);
text-decoration:none;padding:8px 4px}
.langs a[aria-current]{color:var(--accent)}
main{padding:44px 0 60px}
.mono{font:500 11.5px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase;
color:var(--accent)}
h1{font-size:clamp(28px,4.6vw,46px);line-height:1.08;letter-spacing:-.03em;
margin:16px 0 0;max-width:18ch}
.lede{color:var(--ink2);margin:16px 0 0;max-width:56ch}
.tag{display:inline-block;font:500 11px/1 var(--mono);letter-spacing:.14em;
text-transform:uppercase;color:var(--accent2);background:#E3F0F0;padding:6px 9px;
margin:22px 0 0}
.shot{display:block;margin:28px 0 0;border:1px solid var(--line)}
.shot img{display:block;width:100%;height:auto}
.bl{margin:38px 0 0}
.bl h2{font:500 11.5px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;
color:var(--ink3);margin:0 0 10px}
.bl p{margin:0;max-width:62ch}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin:40px 0 0}
.cta a,.cta button{font:500 15.5px/1 var(--sans);padding:14px 20px;border:1px solid var(--line);
background:var(--paper);color:var(--ink);text-decoration:none;cursor:pointer}
.cta .go{background:var(--accent);border-color:var(--accent);color:#fff}
.cta .go:hover{background:var(--accent2);border-color:var(--accent2)}
footer{border-top:1px solid var(--line);padding:26px 0;color:var(--ink3);font-size:14px}
"""


def _т(значение, lang):
    if isinstance(значение, dict):
        return значение.get(lang) or значение.get('en') or ''
    return str(значение or '')


def страница(it: dict, lang: str) -> str:
    e = H.escape
    п = ПОДПИСИ[lang]
    т = ТЕКСТЫ[it['slug']][lang]
    назв = _т(it.get('title'), lang)
    языки = "".join(
        f'<a href="{ПУТЬ[к]}{it["slug"]}/"'
        f'{" aria-current=\"page\"" if к == lang else ""}>{к.upper()}</a>'
        for к in ЯЗЫКИ)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(назв)} {e(п['title_suffix'])}</title>
<meta name="description" content="{e(т['task'][:150])}">
<link rel="canonical" href="https://prodigylab.studio{ПУТЬ[lang]}{it['slug']}/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap">
 <a class="brand" href="{ГЛАВНАЯ[lang]}"><b>PRODIGY</b> LAB</a>
 <nav class="langs">{языки}</nav>
</div></header>
<main><div class="wrap">
 <span class="mono">{e(п['eyebrow'])}</span>
 <h1>{e(назв)}</h1>
 <p class="lede">{e(_т(it.get('short_description'), lang))}</p>
 <span class="tag">{e(п['concept'])}</span>
 <span class="shot"><img src="{it['cover']}" alt="{e(назв)}" width="800" height="500"
   loading="lazy" decoding="async"></span>
 <div class="bl"><h2>{e(п['task'])}</h2><p>{e(т['task'])}</p></div>
 <div class="bl"><h2>{e(п['done'])}</h2><p>{e(т['done'])}</p></div>
 <div class="bl"><h2>{e(п['limits'])}</h2><p>{e(т['limits'])}</p></div>
 <div class="cta">
  <a class="go" href="{it['demo_url']}">{e(п['demo'])} &rarr;</a>
  <a href="{ГЛАВНАЯ[lang]}?demo={it['slug']}#start">{e(п['talk'])}</a>
  <a href="{ГАЛЕРЕЯ[lang]}">{e(п['back'])}</a>
 </div>
</div></main>
<footer><div class="wrap">© 2026 Prodigy LAB · Platonaire LLC</div></footer>
</body>
</html>"""


def собрать() -> list:
    с = os.path.join(КОРЕНЬ, 'SHOWCASE.json')
    with open(с, encoding='utf-8') as f:
        items = json.load(f)['items']
    готовые = [i for i in items
               if i['publication_status'] == 'published' and i.get('showcase')
               and i['slug'] in ТЕКСТЫ]
    сделано = []
    for it in готовые:
        for lang in ЯЗЫКИ:
            путь = os.path.join(КОРЕНЬ, ПУТЬ[lang].strip('/'), it['slug'], 'index.html')
            os.makedirs(os.path.dirname(путь), exist_ok=True)
            with open(путь, 'w', encoding='utf-8') as f:
                f.write(страница(it, lang))
            сделано.append(os.path.relpath(путь, КОРЕНЬ))
    return сделано


if __name__ == '__main__':
    for п in собрать():
        print('  ✓', п)
    print('Описания работ собраны')
