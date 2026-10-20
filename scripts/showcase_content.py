# -*- coding: utf-8 -*-
"""Тексты галереи примеров на пяти языках.

Отдельно от каталога: в SHOWCASE.json лежат сами работы, здесь — обвязка
страницы. Так новый пример добавляется правкой одного JSON, без перевода
интерфейса заново.
"""

# Подписи ниш и типов решений. Ключи совпадают с полями niche и
# solution_type в SHOWCASE.json. Нет ключа — фильтр покажет сырое значение,
# и это заметно: значит, перевод забыли.
NICHE = {
    'fencing': {'en': 'Fencing', 'ru': 'Заборы', 'es': 'Vallas',
                'pt': 'Cercas', 'de': 'Zäune'},
    'restaurant': {'en': 'Restaurants', 'ru': 'Рестораны', 'es': 'Restaurantes',
                   'pt': 'Restaurantes', 'de': 'Restaurants'},
}

SOLUTION = {
    'configurator': {'en': 'Configurator', 'ru': 'Конфигуратор', 'es': 'Configurador',
                     'pt': 'Configurador', 'de': 'Konfigurator'},
    'menu_ordering': {'en': 'Menu & ordering', 'ru': 'Меню и заказ', 'es': 'Menú y pedidos',
                      'pt': 'Cardápio e pedidos', 'de': 'Karte & Bestellung'},
}

S = {
 'en': dict(
   title='Explore our work — interactive concepts by Prodigy LAB',
   desc='Working demonstrations we build for real businesses: a fence project planner, '
        'a restaurant menu with pickup. Open any of them and try the tool yourself.',
   nav='Explore our work',
   h1='Explore our work',
   lead='These are working demonstrations, not screenshots. Open one and use the tool — '
        'it runs in your browser and sends nothing anywhere.',
   count_one='One example published.',
   count_many='{n} examples published.',
   concept='Concept',
   client='Client project',
   concept_note='Independent prototype. Built by Prodigy LAB on public information, '
                'not commissioned by the business and not affiliated with it.',
   client_note='Built and launched for a client, shown with their permission.',
   filter_niche='Industry',
   filter_solution='Solution',
   filter_all='All',
   empty='Nothing matches these filters.',
   reset='Show everything',
   demo='Explore demo',
   demo_aria='Explore the {title} demo — opens in a new tab',
   similar='Build something like this for my business',
   more='Show more',
   footer_back='Home',
   soon='More examples are being prepared. The gallery shows only what is ready.',
 ),
 'ru': dict(
   title='Примеры решений — интерактивные концепты Prodigy LAB',
   desc='Рабочие демонстрации, которые мы собираем для настоящего бизнеса: планировщик '
        'забора, меню ресторана с самовывозом. Любую можно открыть и попробовать.',
   nav='Примеры решений',
   h1='Примеры решений',
   lead='Это рабочие демонстрации, а не скриншоты. Откройте любую и попробуйте инструмент — '
        'он работает прямо в браузере и никуда ничего не отправляет.',
   count_one='Опубликован один пример.',
   count_many='Опубликовано примеров: {n}.',
   concept='Концепт',
   client='Клиентский проект',
   concept_note='Независимый прототип. Собран Prodigy LAB по открытым данным, компания его '
                'не заказывала и к нему отношения не имеет.',
   client_note='Сделано и запущено для клиента, показывается с его разрешения.',
   filter_niche='Ниша',
   filter_solution='Решение',
   filter_all='Все',
   empty='Под эти фильтры ничего нет.',
   reset='Показать всё',
   demo='Попробовать',
   demo_aria='Открыть демонстрацию «{title}» — в новой вкладке',
   similar='Хочу похожее решение',
   more='Показать ещё',
   footer_back='На главную',
   soon='Новые примеры готовятся. В галерее только то, что готово.',
 ),
 'es': dict(
   title='Ejemplos de soluciones — conceptos interactivos de Prodigy LAB',
   desc='Demostraciones funcionales que creamos para negocios reales: un planificador de '
        'cercas, un menú de restaurante con recogida. Abre cualquiera y pruébala.',
   nav='Ejemplos',
   h1='Ejemplos de soluciones',
   lead='Son demostraciones funcionales, no capturas de pantalla. Abre una y usa la '
        'herramienta: funciona en tu navegador y no envía nada a ningún sitio.',
   count_one='Un ejemplo publicado.',
   count_many='Ejemplos publicados: {n}.',
   concept='Concepto',
   client='Proyecto de cliente',
   concept_note='Prototipo independiente. Creado por Prodigy LAB con información pública; '
                'la empresa no lo encargó ni está vinculada a él.',
   client_note='Creado y lanzado para un cliente, mostrado con su permiso.',
   filter_niche='Sector',
   filter_solution='Solución',
   filter_all='Todos',
   empty='Nada coincide con estos filtros.',
   reset='Mostrar todo',
   demo='Probar',
   demo_aria='Abrir la demo «{title}» — en una pestaña nueva',
   similar='Quiero una solución así',
   more='Mostrar más',
   footer_back='Inicio',
   soon='Se están preparando más ejemplos. La galería muestra solo lo que está listo.',
 ),
 'pt': dict(
   title='Exemplos de soluções — conceitos interativos da Prodigy LAB',
   desc='Demonstrações funcionais que criamos para negócios reais: um planejador de cercas, '
        'um cardápio de restaurante com retirada. Abra qualquer uma e experimente.',
   nav='Exemplos',
   h1='Exemplos de soluções',
   lead='São demonstrações funcionais, não capturas de tela. Abra uma e use a ferramenta: '
        'ela roda no seu navegador e não envia nada para lugar nenhum.',
   count_one='Um exemplo publicado.',
   count_many='Exemplos publicados: {n}.',
   concept='Conceito',
   client='Projeto de cliente',
   concept_note='Protótipo independente. Criado pela Prodigy LAB com informações públicas; '
                'a empresa não o encomendou nem tem ligação com ele.',
   client_note='Criado e lançado para um cliente, exibido com autorização.',
   filter_niche='Setor',
   filter_solution='Solução',
   filter_all='Todos',
   empty='Nada corresponde a estes filtros.',
   reset='Mostrar tudo',
   demo='Experimentar',
   demo_aria='Abrir a demo «{title}» — em uma nova aba',
   similar='Quero uma solução assim',
   more='Mostrar mais',
   footer_back='Início',
   soon='Mais exemplos estão sendo preparados. A galeria mostra apenas o que está pronto.',
 ),
 'de': dict(
   title='Beispiele unserer Arbeit — interaktive Konzepte von Prodigy LAB',
   desc='Funktionierende Demonstrationen für echte Unternehmen: ein Zaunplaner, eine '
        'Restaurantkarte mit Abholung. Jede lässt sich öffnen und ausprobieren.',
   nav='Beispiele',
   h1='Beispiele unserer Arbeit',
   lead='Das sind funktionierende Demonstrationen, keine Screenshots. Öffnen Sie eine und '
        'nutzen Sie das Werkzeug — es läuft im Browser und sendet nichts.',
   count_one='Ein Beispiel veröffentlicht.',
   count_many='Veröffentlichte Beispiele: {n}.',
   concept='Konzept',
   client='Kundenprojekt',
   concept_note='Unabhängiger Prototyp. Von Prodigy LAB aus öffentlichen Informationen '
                'erstellt; das Unternehmen hat ihn nicht beauftragt.',
   client_note='Für einen Kunden erstellt und veröffentlicht, mit dessen Erlaubnis gezeigt.',
   filter_niche='Branche',
   filter_solution='Lösung',
   filter_all='Alle',
   empty='Zu diesen Filtern gibt es nichts.',
   reset='Alles anzeigen',
   demo='Ausprobieren',
   demo_aria='Demo „{title}“ öffnen — in einem neuen Tab',
   similar='Ich möchte so eine Lösung',
   more='Mehr anzeigen',
   footer_back='Startseite',
   soon='Weitere Beispiele entstehen gerade. Die Galerie zeigt nur, was fertig ist.',
 ),
}

# Блок на главной. Заголовок короче, чем на самой галерее: там он объясняет
# раздел, здесь — зовёт в него.
HOME = {
 'en': dict(eyebrow='PREVIEW FACTORY', h2='See what we build, not what we promise.',
            lead='Working demonstrations for real businesses. Open one and use the tool.',
            all='Explore our work'),
 'ru': dict(eyebrow='PREVIEW FACTORY', h2='Посмотрите, что мы делаем, а не что обещаем.',
            lead='Рабочие демонстрации для настоящего бизнеса. Откройте и попробуйте.',
            all='Все примеры'),
 'es': dict(eyebrow='PREVIEW FACTORY', h2='Mire lo que hacemos, no lo que prometemos.',
            lead='Demostraciones funcionales para negocios reales. Ábralas y pruébelas.',
            all='Ver todos los ejemplos'),
 'pt': dict(eyebrow='PREVIEW FACTORY', h2='Veja o que fazemos, não o que prometemos.',
            lead='Demonstrações funcionais para negócios reais. Abra e experimente.',
            all='Ver todos os exemplos'),
 'de': dict(eyebrow='PREVIEW FACTORY', h2='Sehen Sie, was wir bauen, nicht was wir versprechen.',
            lead='Funktionierende Demonstrationen für echte Unternehmen. Öffnen und testen.',
            all='Alle Beispiele'),
}
