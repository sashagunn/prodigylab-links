# -*- coding: utf-8 -*-
"""Нижние секции главной: библиотека блоков под направление задачи.

Второй логики персонализации здесь нет. Направление приходит из того же
состояния посетителя, что ведёт разговор (`qualify` + `routing`), и секции
только выбирают заранее написанный блок. Текст под клиента не сочиняется.

Правила отбора простые и видимые:

* реклама задаёт начальную гипотезу, слова клиента её заменяют;
* пока направление не подтверждено, показывается общий блок;
* пример берётся из SHOWCASE.json и только опубликованный; если для
  направления опубликованного примера нет — показывается разбор процесса, а
  не чужой кейс. Выдавать ресторан за решение по процессингу нельзя.

Что здесь намеренно не пишется: обещания одобрения, сроков ответа, возврата
средств и роста конверсии. По платежам, банкам и финансированию это не
скромность, а граница: решение принимает не студия.
"""

ЯЗЫКИ = ("en", "ru", "es", "pt", "de")

# Подписи самих секций.
ОБЩЕЕ = {
 'ru': dict(path='Как разбираем', need='Что понадобится', limits='Границы',
            example='Пример', talk='Продолжить разговор', open='Открыть демо',
            all='Все примеры', process='Разбор процесса',
            no_case='Опубликованного примера по этой задаче у нас нет — '
                    'показываем порядок разбора, а не чужой кейс.',
            concept='концепт студии', hint='Ответьте помощнику выше — '
                    'и этот раздел покажет путь под вашу задачу.'),
 'en': dict(path='How we work it', need='What we will need', limits='Boundaries',
            example='Example', talk='Continue the conversation', open='Open the demo',
            all='All examples', process='How the work goes',
            no_case='We have no published example for this task — '
                    'so here is the order of work, not someone else’s case.',
            concept='studio concept', hint='Answer the assistant above — '
                    'and this section will show the path for your task.'),
 'es': dict(path='Cómo lo analizamos', need='Qué hará falta',
            limits='Límites', example='Ejemplo',
            talk='Seguir la conversación', open='Abrir la demo',
            all='Todos los ejemplos', process='Cómo es el trabajo',
            no_case='No tenemos un ejemplo publicado para esta tarea: '
                    'mostramos el orden del trabajo, no el caso de otro.',
            concept='concepto del estudio',
            hint='Responda al asistente arriba y esta sección mostrará '
                 'el camino para su tarea.'),
 'pt': dict(path='Como analisamos', need='O que vamos precisar',
            limits='Limites', example='Exemplo',
            talk='Continuar a conversa', open='Abrir a demo',
            all='Todos os exemplos', process='Como o trabalho acontece',
            no_case='Não temos exemplo publicado para esta tarefa: '
                    'mostramos a ordem do trabalho, não o caso de outro.',
            concept='conceito do estúdio',
            hint='Responda ao assistente acima e esta seção mostrará '
                 'o caminho para a sua tarefa.'),
 'de': dict(path='Wie wir vorgehen', need='Was wir brauchen',
            limits='Grenzen', example='Beispiel',
            talk='Gespräch fortsetzen', open='Demo öffnen',
            all='Alle Beispiele', process='Wie die Arbeit läuft',
            no_case='Für diese Aufgabe haben wir kein veröffentlichtes '
                    'Beispiel — hier steht die Reihenfolge der Arbeit, '
                    'nicht der Fall eines anderen.',
            concept='Studio-Konzept',
            hint='Antworten Sie dem Assistenten oben — dann zeigt dieser '
                 'Abschnitt den Weg für Ihre Aufgabe.'),
}


def _б(problem, approach, steps, need, limits, cta):
    return dict(problem=problem, approach=approach, steps=steps,
                need=need, limits=limits, cta=cta)


# Блоки под направление. Тексты короткие намеренно: раздел должен помочь
# понять порядок работы, а не заменить разговор.
БЛОКИ = {
 '': {
  'ru': _б('Пока не ясно, что именно чинить',
           'Сначала выясняем, где теряются деньги. Чаще всего — не там, где кажется.',
           [('Слушаем', 'Что происходит и как это видно по цифрам'),
            ('Сужаем', 'Отделяем причину от следствия'),
            ('Предлагаем', 'Что делаем первым и почему именно это'),
            ('Считаем', 'Сколько это стоит и что меняется')],
           ['Чем занимается бизнес', 'Что уже пробовали', 'К какому сроку нужно'],
           'Пока направление не названо, конкретный путь показать нечем — '
           'и выдумывать его мы не станем.',
           'Рассказать, что происходит'),
  'en': _б('Not yet clear what needs fixing',
           'First we find where the money leaks. Usually not where it seems.',
           [('Listen', 'What is happening and how it shows in the numbers'),
            ('Narrow', 'Separate the cause from the symptom'),
            ('Propose', 'What we do first and why that'),
            ('Count', 'What it costs and what changes')],
           ['What the business does', 'What you already tried', 'By when you need it'],
           'Until the direction is named there is no specific path to show — '
           'and we will not invent one.',
           'Tell us what is happening'),
  'es': _б('Aún no está claro qué hay que arreglar',
           'Primero buscamos dónde se escapa el dinero. Casi nunca donde parece.',
           [('Escuchamos', 'Qué pasa y cómo se ve en las cifras'),
            ('Acotamos', 'Separamos la causa del síntoma'),
            ('Proponemos', 'Qué hacemos primero y por qué eso'),
            ('Calculamos', 'Cuánto cuesta y qué cambia')],
           ['A qué se dedica el negocio', 'Qué ya intentó',
            'Para cuándo lo necesita'],
           'Mientras no se nombre la dirección no hay camino concreto que '
           'mostrar, y no lo vamos a inventar.',
           'Contar qué está pasando'),
  'pt': _б('Ainda não está claro o que precisa de conserto',
           'Primeiro achamos por onde o dinheiro vaza. Quase nunca onde parece.',
           [('Ouvimos', 'O que acontece e como aparece nos números'),
            ('Estreitamos', 'Separamos a causa do sintoma'),
            ('Propomos', 'O que fazemos primeiro e por quê'),
            ('Calculamos', 'Quanto custa e o que muda')],
           ['O que o negócio faz', 'O que você já tentou',
            'Para quando precisa'],
           'Enquanto a direção não for nomeada não há '
           'caminho concreto a mostrar, e não vamos inventá-lo.',
           'Contar o que está acontecendo'),
  'de': _б('Noch unklar, was genau zu beheben ist',
           'Zuerst finden wir, wo das Geld verloren geht. Selten dort, wo es scheint.',
           [('Zuhören', 'Was passiert und wie es sich in Zahlen zeigt'),
            ('Eingrenzen', 'Ursache vom Symptom trennen'),
            ('Vorschlagen', 'Was wir zuerst tun und warum gerade das'),
            ('Rechnen', 'Was es kostet und was sich ändert')],
           ['Was das Geschäft macht', 'Was Sie schon versucht haben',
            'Bis wann Sie es brauchen'],
           'Solange die Richtung nicht benannt ist, gibt es keinen konkreten '
           'Weg zu zeigen — und erfinden werden wir ihn nicht.',
           'Erzählen, was passiert'),
 },
 'presence': {
  'ru': _б('Сайт не приносит обращений — или его ещё нет',
           'Смотрим путь посетителя целиком: от первого экрана до отправленной заявки. '
           'Чинить начинаем с того места, где люди уходят.',
           [('Смотрим сайт', 'Первый экран, скорость, путь к действию'),
            ('Находим обрыв', 'Где посетитель уходит и почему'),
            ('Показываем правку', 'Одно исправление целиком, на вашем материале'),
            ('Собираем', 'Страница или магазин, с оплатой если нужна')],
           ['Адрес сайта, если он есть', 'Что продаёте', 'Заявки или продажи на сайте'],
           'Конверсию заранее не обещаем: до замера это была бы цифра из воздуха.',
           'Обсудить сайт'),
  'en': _б('The site brings no enquiries — or there is none yet',
           'We look at the whole visitor path, from the first screen to a sent request. '
           'We start fixing where people drop off.',
           [('Look at the site', 'First screen, speed, path to action'),
            ('Find the break', 'Where the visitor leaves and why'),
            ('Show one fix', 'One correction in full, on your own material'),
            ('Build', 'A page or a store, with payment if needed')],
           ['The site address, if there is one', 'What you sell',
            'Enquiries or sales on the site'],
           'We do not promise a conversion number in advance: before measuring '
           'it would be a figure out of thin air.',
           'Discuss the site'),
  'es': _б('El sitio no trae solicitudes, o aún no existe',
           'Miramos todo el recorrido del visitante, de la primera pantalla a la '
           'solicitud enviada. Arreglamos donde la gente se va.',
           [('Miramos el sitio', 'Primera pantalla, velocidad, camino a la acción'),
            ('Hallamos el corte', 'Dónde se va el visitante y por qué'),
            ('Mostramos una corrección', 'Una entera, sobre su propio material'),
            ('Construimos', 'Página o tienda, con pago si hace falta')],
           ['La dirección del sitio, si existe', 'Qué vende',
            'Solicitudes o ventas en el sitio'],
           'No prometemos una cifra de conversión por adelantado: sin medir '
           'sería un número inventado.',
           'Hablar del sitio'),
  'pt': _б('O site não traz solicitações, ou ainda não existe',
           'Olhamos todo o caminho do visitante, da primeira tela até a '
           'solicitação enviada. Começamos onde as pessoas saem.',
           [('Olhamos o site', 'Primeira tela, velocidade, caminho até a ação'),
            ('Achamos a quebra', 'Onde o visitante sai e por quê'),
            ('Mostramos uma correção', 'Uma inteira, no seu próprio material'),
            ('Construímos', 'Página ou loja, com pagamento se precisar')],
           ['O endereço do site, se houver', 'O que você vende',
            'Solicitações ou vendas no site'],
           'Não prometemos um número de conversão antes: sem medir '
           'seria um número inventado.',
           'Falar sobre o site'),
  'de': _б('Die Website bringt keine Anfragen — oder es gibt sie noch nicht',
           'Wir sehen uns den ganzen Weg des Besuchers an, vom ersten Bildschirm bis '
           'zur abgeschickten Anfrage. Wir reparieren dort, wo Leute abspringen.',
           [('Website ansehen', 'Erster Bildschirm, Tempo, Weg zur Handlung'),
            ('Bruchstelle finden', 'Wo der Besucher geht und warum'),
            ('Eine Korrektur zeigen', 'Eine vollständig, an Ihrem Material'),
            ('Bauen', 'Seite oder Shop, mit Zahlung wenn nötig')],
           ['Die Website-Adresse, falls vorhanden', 'Was Sie verkaufen',
            'Anfragen oder Verkäufe auf der Seite'],
           'Eine Conversion-Zahl versprechen wir nicht im Voraus: ohne Messung '
           'wäre sie aus der Luft gegriffen.',
           'Über die Website sprechen'),
 },
}


БЛОКИ['payments'] = {
 'ru': _б('Приём платежей остановлен или ограничен',
          'Сначала разбираем, что именно произошло и на каком основании. '
          'Потом — как вернуть приём и на чём держаться дальше.',
          [('Читаем решение', 'Что написал процессор и на каком основании'),
           ('Смотрим риск', 'Возвраты, споры, вертикаль, объём'),
           ('Готовим ответ', 'Какие документы и формулировки нужны'),
           ('Строим запас', 'Второй процессинг, чтобы это не повторилось')],
          ['Какой процессор и что он написал', 'Объём платежей в месяц',
           'Были ли возвраты и споры'],
          'Решение принимает процессор, а не студия. Одобрение, сроки и возврат '
          'зависших денег мы не обещаем — ни заранее, ни после разбора.',
          'Разобрать ситуацию'),
 'en': _б('Payments are stopped or restricted',
          'First we work out what exactly happened and on what grounds. '
          'Then how to get acceptance back and what to stand on next.',
          [('Read the decision', 'What the processor wrote and on what grounds'),
           ('Look at risk', 'Refunds, disputes, vertical, volume'),
           ('Prepare the reply', 'Which documents and wording are needed'),
           ('Build a backup', 'A second processor so it does not repeat')],
          ['Which processor and what they wrote', 'Monthly payment volume',
           'Whether there were refunds and disputes'],
          'The decision is the processor\u2019s, not the studio\u2019s. We promise no '
          'approval, no timeline and no return of held funds — neither before '
          'nor after the review.',
          'Work through the situation'),
 'es': _б('El cobro est\u00e1 detenido o limitado',
          'Primero entendemos qu\u00e9 pas\u00f3 exactamente y con qu\u00e9 fundamento. '
          'Luego c\u00f3mo recuperar el cobro y en qu\u00e9 apoyarse despu\u00e9s.',
          [('Leemos la decisi\u00f3n', 'Qu\u00e9 escribi\u00f3 el procesador y con qu\u00e9 base'),
           ('Miramos el riesgo', 'Devoluciones, disputas, vertical, volumen'),
           ('Preparamos la respuesta', 'Qu\u00e9 documentos y qu\u00e9 redacci\u00f3n hacen falta'),
           ('Armamos respaldo', 'Un segundo procesador para que no se repita')],
          ['Qu\u00e9 procesador y qu\u00e9 escribi\u00f3', 'Volumen de pagos al mes',
           'Si hubo devoluciones y disputas'],
          'La decisi\u00f3n es del procesador, no del estudio. No prometemos '
          'aprobaci\u00f3n, ni plazos, ni la devoluci\u00f3n del dinero retenido.',
          'Analizar la situaci\u00f3n'),
 'pt': _б('O recebimento est\u00e1 parado ou limitado',
          'Primeiro entendemos o que exatamente aconteceu e com que fundamento. '
          'Depois como voltar a receber e em que se apoiar adiante.',
          [('Lemos a decis\u00e3o', 'O que o processador escreveu e com que base'),
           ('Olhamos o risco', 'Estornos, disputas, vertical, volume'),
           ('Preparamos a resposta', 'Quais documentos e qual reda\u00e7\u00e3o s\u00e3o precisos'),
           ('Montamos reserva', 'Um segundo processador para n\u00e3o repetir')],
          ['Qual processador e o que ele escreveu', 'Volume de pagamentos por m\u00eas',
           'Se houve estornos e disputas'],
          'A decis\u00e3o \u00e9 do processador, n\u00e3o do est\u00fadio. N\u00e3o prometemos '
          'aprova\u00e7\u00e3o, prazos nem a devolu\u00e7\u00e3o do dinheiro retido.',
          'Analisar a situa\u00e7\u00e3o'),
 'de': _б('Zahlungsannahme gestoppt oder eingeschr\u00e4nkt',
          'Zuerst kl\u00e4ren wir, was genau passiert ist und auf welcher Grundlage. '
          'Dann, wie die Annahme zur\u00fcckkommt und worauf man danach steht.',
          [('Entscheidung lesen', 'Was der Anbieter schrieb und auf welcher Basis'),
           ('Risiko ansehen', 'R\u00fcckbuchungen, Disputes, Vertikale, Volumen'),
           ('Antwort vorbereiten', 'Welche Unterlagen und Formulierungen n\u00f6tig sind'),
           ('Reserve bauen', 'Ein zweiter Anbieter, damit es sich nicht wiederholt')],
          ['Welcher Anbieter und was er schrieb', 'Zahlungsvolumen pro Monat',
           'Ob es R\u00fcckbuchungen und Disputes gab'],
          'Die Entscheidung trifft der Anbieter, nicht das Studio. Wir versprechen '
          'keine Zusage, keine Fristen und keine R\u00fcckgabe eingefrorener Gelder.',
          'Die Lage durchgehen'),
}

БЛОКИ['banking'] = {
 'ru': _б('Счёт закрыли, ограничили или не открывают',
          'Банк редко объясняет причину полностью. Разбираем, что известно, '
          'и готовим такую подачу, с которой есть о чём говорить.',
          [('Собираем факты', 'Что произошло со счётом и когда'),
           ('Читаем причину', 'Что банк указал и что обычно стоит за этим'),
           ('Готовим подачу', 'Структура, документы, описание деятельности'),
           ('Ищем площадку', 'Банк или финтех под вашу деятельность')],
          ['Что произошло со счётом', 'Где зарегистрирована компания',
           'Какие операции нужны'],
          'Открытие счёта — решение банка. Ни одобрения, ни сроков мы не обещаем '
          'и не можем на них повлиять.',
          'Разобрать ситуацию'),
 'en': _б('The account was closed, restricted or refused',
          'Banks rarely explain the reason in full. We work through what is known '
          'and prepare a presentation there is something to talk about with.',
          [('Collect facts', 'What happened to the account and when'),
           ('Read the reason', 'What the bank stated and what usually sits behind it'),
           ('Prepare the case', 'Structure, documents, description of the business'),
           ('Find a venue', 'A bank or fintech that fits your activity')],
          ['What happened to the account', 'Where the company is registered',
           'Which operations you need'],
          'Opening an account is the bank\u2019s decision. We promise no approval and '
          'no timeline, and we cannot influence them.',
          'Work through the situation'),
 'es': _б('Cerraron, limitaron o no abren la cuenta',
          'El banco rara vez explica del todo. Revisamos lo que se sabe y '
          'preparamos una presentaci\u00f3n con la que haya de qu\u00e9 hablar.',
          [('Reunimos hechos', 'Qu\u00e9 pas\u00f3 con la cuenta y cu\u00e1ndo'),
           ('Leemos el motivo', 'Qu\u00e9 indic\u00f3 el banco y qu\u00e9 suele haber detr\u00e1s'),
           ('Preparamos el caso', 'Estructura, documentos, descripci\u00f3n del negocio'),
           ('Buscamos d\u00f3nde', 'Banco o fintech acorde a su actividad')],
          ['Qu\u00e9 pas\u00f3 con la cuenta', 'D\u00f3nde est\u00e1 registrada la empresa',
           'Qu\u00e9 operaciones necesita'],
          'Abrir una cuenta es decisi\u00f3n del banco. No prometemos aprobaci\u00f3n ni '
          'plazos, y no podemos influir en ellos.',
          'Analizar la situaci\u00f3n'),
 'pt': _б('A conta foi encerrada, limitada ou recusada',
          'O banco raramente explica tudo. Revisamos o que se sabe e preparamos '
          'uma apresenta\u00e7\u00e3o com a qual haja o que conversar.',
          [('Reunimos fatos', 'O que aconteceu com a conta e quando'),
           ('Lemos o motivo', 'O que o banco indicou e o que costuma estar por tr\u00e1s'),
           ('Preparamos o caso', 'Estrutura, documentos, descri\u00e7\u00e3o do neg\u00f3cio'),
           ('Procuramos onde', 'Banco ou fintech conforme sua atividade')],
          ['O que aconteceu com a conta', 'Onde a empresa est\u00e1 registrada',
           'Quais opera\u00e7\u00f5es voc\u00ea precisa'],
          'Abrir conta \u00e9 decis\u00e3o do banco. N\u00e3o prometemos aprova\u00e7\u00e3o nem '
          'prazos, e n\u00e3o podemos influenci\u00e1-los.',
          'Analisar a situa\u00e7\u00e3o'),
 'de': _б('Konto gek\u00fcndigt, eingeschr\u00e4nkt oder abgelehnt',
          'Banken erkl\u00e4ren den Grund selten vollst\u00e4ndig. Wir gehen durch, was '
          'bekannt ist, und bereiten eine Darstellung vor, mit der man reden kann.',
          [('Fakten sammeln', 'Was mit dem Konto passiert ist und wann'),
           ('Grund lesen', 'Was die Bank nannte und was meist dahintersteht'),
           ('Unterlagen bauen', 'Struktur, Dokumente, Beschreibung der T\u00e4tigkeit'),
           ('Ort finden', 'Bank oder Fintech passend zu Ihrer T\u00e4tigkeit')],
          ['Was mit dem Konto passiert ist', 'Wo die Firma registriert ist',
           'Welche Transaktionen Sie brauchen'],
          'Die Kontoer\u00f6ffnung entscheidet die Bank. Wir versprechen weder Zusage '
          'noch Fristen und k\u00f6nnen sie nicht beeinflussen.',
          'Die Lage durchgehen'),
}


БЛОКИ['funding'] = {
 'ru': _б('Бизнесу нужны деньги на рост или кассовый разрыв',
          'Сначала считаем, под что берутся деньги и чем они возвращаются. '
          'Потом смотрим, какие площадки вообще рассматривают такой профиль.',
          [('Считаем цель', 'Подо что деньги и что они закроют'),
           ('Смотрим профиль', 'Возраст бизнеса, оборот, уже взятые обязательства'),
           ('Готовим пакет', 'Выписки и документы в том виде, в каком их читают'),
           ('Говорим прямо', 'Что реально подходит, а что нет')],
          ['Сколько нужно и на что', 'Оборот в месяц и возраст бизнеса',
           'Уже имеющиеся кредиты'],
          'Условия, ставку и одобрение определяет кредитор. Мы не обещаем ни '
          'сумму, ни ставку, ни сам факт одобрения.',
          'Разобрать задачу'),
 'en': _б('The business needs money for growth or a cash gap',
          'First we work out what the money is for and what repays it. '
          'Then which venues even look at a profile like this.',
          [('Count the goal', 'What the money is for and what it closes'),
           ('Look at the profile', 'Age, revenue, obligations already taken'),
           ('Prepare the pack', 'Statements and documents in the form they are read'),
           ('Say it straight', 'What actually fits and what does not')],
          ['How much and what for', 'Monthly revenue and age of the business',
           'Loans you already have'],
          'Terms, rate and approval are set by the lender. We promise no amount, '
          'no rate and no approval.',
          'Work through the task'),
 'es': _б('El negocio necesita dinero para crecer o cubrir caja',
          'Primero calculamos para qu\u00e9 es el dinero y con qu\u00e9 se devuelve. '
          'Luego qu\u00e9 entidades miran siquiera un perfil as\u00ed.',
          [('Calculamos el objetivo', 'Para qu\u00e9 es el dinero y qu\u00e9 cubre'),
           ('Miramos el perfil', 'Antig\u00fcedad, facturaci\u00f3n, obligaciones ya tomadas'),
           ('Preparamos el paquete', 'Extractos y documentos como se leen'),
           ('Decimos claro', 'Qué encaja de verdad y qué no')],
          ['Cu\u00e1nto y para qu\u00e9', 'Facturaci\u00f3n mensual y antig\u00fcedad',
           'Pr\u00e9stamos que ya tiene'],
          'Las condiciones, la tasa y la aprobaci\u00f3n las fija el prestamista. No '
          'prometemos monto, ni tasa, ni aprobaci\u00f3n.',
          'Analizar la tarea'),
 'pt': _б('O neg\u00f3cio precisa de dinheiro para crescer ou cobrir caixa',
          'Primeiro calculamos para que \u00e9 o dinheiro e com o que ele volta. '
          'Depois quais institui\u00e7\u00f5es sequer olham um perfil assim.',
          [('Calculamos o objetivo', 'Para que \u00e9 o dinheiro e o que ele cobre'),
           ('Olhamos o perfil', 'Idade, faturamento, obriga\u00e7\u00f5es j\u00e1 assumidas'),
           ('Preparamos o pacote', 'Extratos e documentos no formato em que s\u00e3o lidos'),
           ('Falamos direto', 'O que realmente serve e o que não')],
          ['Quanto e para qu\u00ea', 'Faturamento mensal e idade do neg\u00f3cio',
           'Empr\u00e9stimos que j\u00e1 tem'],
          'Condi\u00e7\u00f5es, taxa e aprova\u00e7\u00e3o s\u00e3o do credor. N\u00e3o prometemos valor, '
          'taxa nem aprova\u00e7\u00e3o.',
          'Analisar a tarefa'),
 'de': _б('Das Gesch\u00e4ft braucht Geld f\u00fcr Wachstum oder eine Liquidit\u00e4tsl\u00fccke',
          'Zuerst rechnen wir, wof\u00fcr das Geld ist und womit es zur\u00fcckkommt. '
          'Dann, welche Stellen so ein Profil \u00fcberhaupt ansehen.',
          [('Ziel rechnen', 'Wof\u00fcr das Geld ist und was es schlie\u00dft'),
           ('Profil ansehen', 'Alter, Umsatz, bereits bestehende Verpflichtungen'),
           ('Paket vorbereiten', 'Ausz\u00fcge und Unterlagen in der gelesenen Form'),
           ('Klar sagen', 'Was wirklich passt und was nicht')],
          ['Wie viel und wof\u00fcr', 'Monatsumsatz und Alter des Gesch\u00e4fts',
           'Bereits bestehende Kredite'],
          'Konditionen, Zins und Zusage bestimmt der Kreditgeber. Wir versprechen '
          'weder Summe noch Zins noch Zusage.',
          'Die Aufgabe durchgehen'),
}

БЛОКИ['operations'] = {
 'ru': _б('Слишком много делается руками',
          'Идём по пути заявки от первого касания до закрытия и ищем, где она '
          'стоит, теряется или переписывается в третий раз.',
          [('Рисуем путь', 'Что происходит с заявкой от первого касания'),
           ('Находим простои', 'Где ждут, теряют и дублируют'),
           ('Убираем лишнее', 'Сначала то, что отнимает больше всего времени'),
           ('Связываем', 'Учёт, передачи и уведомления в одном месте')],
          ['Что происходит с заявкой сейчас', 'Сколько людей в процессе',
           'Какие инструменты уже стоят'],
          'Сколько времени освободится, скажем после разбора пути, а не до него.',
          '\u041e\u0431\u0441\u0443\u0434\u0438\u0442\u044c \u043f\u0440\u043e\u0446\u0435\u0441\u0441'),
 'en': _б('Too much is done by hand',
          'We walk the path of a request from first touch to close and look for '
          'where it waits, gets lost or is retyped a third time.',
          [('Draw the path', 'What happens to a request from first touch'),
           ('Find the stalls', 'Where it waits, gets lost and is duplicated'),
           ('Remove the extra', 'Starting with what eats the most time'),
           ('Connect', 'Records, handoffs and alerts in one place')],
          ['What happens to a request now', 'How many people are in the process',
           'Which tools are already in place'],
          'How much time is freed we say after walking the path, not before.',
          'Discuss the process'),
 'es': _б('Demasiado se hace a mano',
          'Recorremos el camino de una solicitud desde el primer contacto hasta '
          'el cierre y buscamos d\u00f3nde espera, se pierde o se reescribe.',
          [('Dibujamos el camino', 'Qu\u00e9 pasa con la solicitud desde el primer contacto'),
           ('Hallamos las paradas', 'D\u00f3nde espera, se pierde y se duplica'),
           ('Quitamos lo sobrante', 'Empezando por lo que m\u00e1s tiempo consume'),
           ('Conectamos', 'Registro, traspasos y avisos en un solo lugar')],
          ['Qu\u00e9 pasa con una solicitud ahora', 'Cu\u00e1ntas personas hay en el proceso',
           'Qu\u00e9 herramientas ya tiene'],
          'Cu\u00e1nto tiempo se libera lo decimos tras recorrer el camino, no antes.',
          'Hablar del proceso'),
 'pt': _б('Coisas demais s\u00e3o feitas na m\u00e3o',
          'Percorremos o caminho de uma solicita\u00e7\u00e3o do primeiro contato at\u00e9 o '
          'fechamento e procuramos onde ela espera, se perde ou \u00e9 redigitada.',
          [('Desenhamos o caminho', 'O que acontece com a solicita\u00e7\u00e3o desde o primeiro contato'),
           ('Achamos as paradas', 'Onde espera, se perde e se duplica'),
           ('Tiramos o excesso', 'Come\u00e7ando pelo que mais consome tempo'),
           ('Conectamos', 'Registro, repasses e avisos em um lugar s\u00f3')],
          ['O que acontece com uma solicita\u00e7\u00e3o hoje', 'Quantas pessoas no processo',
           'Quais ferramentas j\u00e1 existem'],
          'Quanto tempo se libera dizemos depois de percorrer o caminho, n\u00e3o antes.',
          'Falar do processo'),
 'de': _б('Zu vieles l\u00e4uft von Hand',
          'Wir gehen den Weg einer Anfrage vom ersten Kontakt bis zum Abschluss '
          'und suchen, wo sie wartet, verloren geht oder erneut abgetippt wird.',
          [('Weg zeichnen', 'Was mit einer Anfrage ab dem ersten Kontakt passiert'),
           ('Stockungen finden', 'Wo gewartet, verloren und doppelt erfasst wird'),
           ('\u00dcberfl\u00fcssiges entfernen', 'Zuerst das, was am meisten Zeit frisst'),
           ('Verbinden', 'Erfassung, \u00dcbergaben und Hinweise an einem Ort')],
          ['Was mit einer Anfrage heute passiert', 'Wie viele Personen im Prozess sind',
           'Welche Tools bereits laufen'],
          'Wie viel Zeit frei wird, sagen wir nach dem Durchgehen des Wegs, nicht davor.',
          '\u00dcber den Prozess sprechen'),
}


# --------------------------------------------------------------- примеры
# Пример берём только из SHOWCASE.json. Второго каталога нет. Годится не
# всякое живое демо, а только отобранное в портфолио (showcase: true):
# персональные концепты остаются доступными по своим ссылкам, но публичным
# примером студии не являются.
# Соответствие направлению — по типу решения: конфигуратор и меню с заказом
# это задачи присутствия. Для платежей, банков, финансирования и процессов
# опубликованного примера у нас нет, и подставлять туда ресторан нельзя.
ПОД_НАПРАВЛЕНИЕ = {
    'presence': ('configurator', 'menu_ordering', 'store', 'landing'),
}

# Приметы ниши на пяти языках. Сравнивать название ниши из каталога с тем,
# что человек написал о себе, напрямую нельзя: «fencing» не встречается в
# «fence company», а «restaurant» — в «ресторан».
ПРИМЕТЫ_НИШИ = {
    'fencing': ('fenc', 'забор', 'ограда', 'cerca', 'valla', 'veda', 'zaun',
                'gate', 'ворота'),
    'restaurant': ('restaur', 'ресторан', 'кафе', 'cafe', 'caf\u00e9', 'пицц',
                   'pizza', 'food', 'кухн', 'бар', 'доставка еды', 'comida',
                   'gastro', 'imbiss'),
}


def кандидаты(направление: str, каталог=None) -> list:
    """Опубликованные примеры, подходящие направлению. Пусто — значит пусто."""
    if каталог is None:
        каталог = _каталог()
    типы = ПОД_НАПРАВЛЕНИЕ.get(направление)
    if not типы:
        return []
    годные = [и for и in каталог
              if и.get('publication_status') == 'published' and и.get('showcase')
              and и.get('solution_type') in типы]
    годные.sort(key=lambda и: (not и.get('featured'), и.get('sort_order') or 0))
    return годные


def _каталог():
    import json
    import os
    корень = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(корень, 'SHOWCASE.json'), encoding='utf-8') as f:
        return json.load(f)['items']


def пример_для(направление: str, известно: dict, lang: str = 'ru',
               каталог=None) -> dict | None:
    """Опубликованный пример под задачу или None, если такого нет."""
    if каталог is None:
        import json
        import os
        корень = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(корень, 'SHOWCASE.json'), encoding='utf-8') as f:
            каталог = json.load(f)['items']
    # Только отобранные в портфолио: живое демо, сделанное для конкретной
    # компании, подставлять посетителю как наш публичный пример нельзя.
    годные = [и for и in каталог
              if и.get('publication_status') == 'published' and и.get('showcase')]
    типы = ПОД_НАПРАВЛЕНИЕ.get(направление)
    if not типы:
        return None
    подходят = [и for и in годные if и.get('solution_type') in типы]
    if not подходят:
        return None
    # Ниша клиента важнее порядка в каталоге: человеку из ресторана полезнее
    # ресторан. Ниша берётся из ответов, а не из метки кампании.
    ниша = str((известно or {}).get('business_type') or '').lower()
    if ниша:
        for и in подходят:
            н = str(и.get('niche') or '').lower()
            приметы = ПРИМЕТЫ_НИШИ.get(н) or ((н,) if н else ())
            if any(п in ниша for п in приметы):
                return и
    избранные = [и for и in подходят if и.get('featured')]
    return (избранные or подходят)[0]


def _т(значение, lang: str) -> str:
    if isinstance(значение, dict):
        return значение.get(lang) or значение.get('en') or ''
    return str(значение or '')


# ----------------------------------------------------------------- вёрстка
# Все варианты направлений лежат в разметке сразу, видим один. Так смена
# задачи не требует запроса и не перерисовывает страницу: меняется только
# то, какой блок показан. Высоты блоков близки, поэтому страница не прыгает.
CSS = """
#pf{background:var(--paper)}
#pf .pf-in{max-width:1180px;margin:0 auto;padding:68px 20px 76px}
@media(min-width:900px){#pf .pf-in{padding:104px 32px 112px}}
.pf-v[hidden]{display:none}
.pf-anchor{display:block;height:0;scroll-margin-top:84px}
#pf .pf-in{scroll-margin-top:72px}
.pf-eyebrow{font:500 11.5px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase;
 color:var(--accent);margin:0 0 18px}
.pf-h{font:600 clamp(28px,4.6vw,52px)/1.08 var(--sans);letter-spacing:-.03em;
 color:var(--ink);margin:0;max-width:17ch}
.pf-lede{font:400 clamp(16px,1.5vw,19px)/1.5 var(--sans);color:var(--ink2);
 margin:20px 0 0;max-width:52ch}
.pf-steps{list-style:none;margin:44px 0 0;padding:0;display:grid;gap:1px;
 background:var(--line);border:1px solid var(--line)}
@media(min-width:760px){.pf-steps{grid-template-columns:repeat(4,1fr)}}
.pf-steps li{background:var(--paper);padding:22px 20px 26px}
.pf-steps b{display:block;font:500 11.5px/1 var(--mono);letter-spacing:.14em;
 color:var(--ink3);margin-bottom:14px}
.pf-steps h3{font:600 17px/1.2 var(--sans);color:var(--ink);margin:0 0 8px;
 letter-spacing:-.01em}
.pf-steps p{font:400 14.5px/1.45 var(--sans);color:var(--ink2);margin:0}
.pf-two{display:grid;gap:28px;margin:44px 0 0}
@media(min-width:760px){.pf-two{grid-template-columns:1fr 1fr;gap:1px;
 background:var(--line);border:1px solid var(--line)}
 .pf-two>div{background:var(--paper);padding:26px 24px 30px}}
.pf-two h3{font:500 11.5px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;
 color:var(--ink3);margin:0 0 14px}
.pf-two ul{margin:0;padding:0;list-style:none}
.pf-two li{font:400 16px/1.5 var(--sans);color:var(--ink);padding:9px 0;
 border-bottom:1px solid var(--line)}
.pf-two li:last-child{border-bottom:0}
.pf-two p{font:400 15.5px/1.5 var(--sans);color:var(--ink2);margin:0}
/* Пример или разбор процесса — тёмный блок посреди светлой страницы.
   Он держит внимание лучше любой анимации и отделяет показ от объяснения. */
/* Светлый блок: тёмных зон на странице две — первый экран и проверка сайта.
   Третий остров посередине читался как сбой стиля, а не как приём. */
.pf-dark{margin:56px 0 0;background:var(--paper2);color:var(--ink);
 border:1px solid var(--line);padding:30px 22px 34px}
@media(min-width:900px){.pf-dark{margin:72px 0 0;padding:40px 40px 44px}}
.pf-dark h3{font:600 clamp(20px,2.4vw,27px)/1.2 var(--sans);margin:0 0 10px;
 color:var(--ink);letter-spacing:-.02em}
.pf-dark p{font:400 15.5px/1.5 var(--sans);color:var(--ink2);margin:0;max-width:56ch}
.pf-shot{display:block;margin:24px 0 0;border:1px solid var(--line)}
.pf-shot img{display:block;width:100%;height:auto}
.pf-tagline{display:inline-block;font:500 11px/1 var(--mono);letter-spacing:.14em;
 text-transform:uppercase;color:var(--accent2);background:var(--accent-soft);
 padding:6px 9px;margin:0 0 14px}
.pf-open{display:inline-block;margin:18px 0 0;font:500 15px/1 var(--sans);
 color:#fff;background:var(--accent);padding:13px 18px;text-decoration:none}
.pf-open:hover{background:var(--accent2)}
/* Разбор процесса для направлений, где опубликованного примера нет. */

.pf-cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:40px 0 0}
.pf-cta button,.pf-cta a{font:500 15.5px/1 var(--sans);padding:14px 20px;
 border:1px solid var(--line);background:var(--paper);color:var(--ink);
 text-decoration:none;cursor:pointer}
.pf-cta .pf-main{background:var(--accent);border-color:var(--accent);color:#fff}
.pf-cta .pf-main:hover{background:var(--accent2);border-color:var(--accent2)}
.pf-cta button:hover,.pf-cta a:hover{border-color:var(--ink3)}
.pf-note{font:400 14.5px/1.5 var(--sans);color:var(--ink3);margin:18px 0 0}
/* Если человек уже читает раздел, подменять его под рукой нельзя. Вместо
   этого предлагаем перейти — решение остаётся за ним. */
.pf-switch{position:sticky;bottom:14px;z-index:4;display:none;margin:18px 0 0}
.pf-switch[data-on="1"]{display:block}
.pf-switch button{font:500 15px/1 var(--sans);background:var(--graphite);color:#fff;
 border:0;padding:14px 18px;cursor:pointer;width:100%;text-align:left}
@media(prefers-reduced-motion:no-preference){
 .pf-v{animation:pf-in .28s ease both}
 @keyframes pf-in{from{opacity:.4}to{opacity:1}}
}
"""


def _шаги(блок, ОБ):
    куски = []
    for i, (загол, текст) in enumerate(блок['steps'], 1):
        куски.append(f'<li><b>{i:02d}</b><h3>{загол}</h3><p>{текст}</p></li>')
    return '<ol class="pf-steps">' + ''.join(куски) + '</ol>'


def _тёмный(направление, блок, ОБ, lang, пример):
    if пример:
        назв = _т(пример.get('title'), lang)
        опис = _т(пример.get('short_description'), lang)
        метка = ОБ['concept'] if пример.get('project_type') == 'concept' else ''
        шапка = f'<span class="pf-tagline">{метка}</span>' if метка else ''
        return (f'<div class="pf-dark">{шапка}<h3>{назв}</h3><p>{опис}</p>'
                f'<span class="pf-shot"><img src="{пример["cover"]}" alt="" '
                f'loading="lazy" decoding="async" width="800" height="500"></span>'
                f'<a class="pf-open" href="{пример["demo_url"]}">{ОБ["open"]} &rarr;</a>'
                f'</div>')
    # Опубликованного примера нет. Повторять те же четыре шага вторым
    # списком незачем — они уже выше. Остаётся прямая оговорка.
    return (f'<div class="pf-dark"><h3>{ОБ["process"]}</h3>'
            f'<p>{ОБ["no_case"]}</p></div>')


def вариант(направление: str, lang: str, пример=None) -> str:
    """Разметка одного направления. Скрытые варианты лежат рядом."""
    блок = БЛОКИ.get(направление) or БЛОКИ['']
    б = блок.get(lang) or блок['ru']
    ОБ = ОБЩЕЕ.get(lang) or ОБЩЕЕ['ru']
    нужно = ''.join(f'<li>{x}</li>' for x in б['need'])
    подсказка = (f'<p class="pf-note">{ОБ["hint"]}</p>' if not направление else '')
    return (
        f'<div class="pf-v" data-route="{направление}">'
        f'<p class="pf-eyebrow">{ОБ["path"]}</p>'
        f'<h2 class="pf-h">{б["problem"]}</h2>'
        f'<p class="pf-lede">{б["approach"]}</p>'
        f'<span id="how" class="pf-anchor"></span>{_шаги(б, ОБ)}'
        f'<div class="pf-two">'
        f'<div><h3>{ОБ["need"]}</h3><ul>{нужно}</ul></div>'
        f'<div><h3>{ОБ["limits"]}</h3><p>{б["limits"]}</p></div>'
        f'</div>'
        f'{_тёмный(направление, б, ОБ, lang, пример)}'
        f'<div class="pf-cta">'
        f'<button type="button" class="pf-main" data-talk>{б["cta"]}</button>'
        f'<a href="/showcase/">{ОБ["all"]} &rarr;</a>'
        f'</div>{подсказка}</div>')


def markup(lang: str = 'ru') -> str:
    """Полоса под задачу.

    Сервер рисует нейтральный вариант: он виден сразу и остаётся, если
    скрипты не выполнились. Дальше страница заменяет его вариантом под
    направление, собранным из данных на языке разговора.
    """
    import html as _h
    e = _h.escape
    ОБ = ОБЩЕЕ.get(lang) or ОБЩЕЕ['ru']
    б = БЛОКИ[''].get(lang) or БЛОКИ['']['ru']
    шаги = "".join(
        f'<li><b>{i:02d}</b><div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>'
        for i, (t, p) in enumerate(б['steps'], 1))
    нужно = "".join(f'<li>{e(x)}</li>' for x in б['need'])
    карта = (f'<div class="pf-card"><div class="pf-card-h">'
             f'<span class="tag">{e(ОБ.get("path", ""))}</span></div>'
             f'<ol class="pf-steps">{шаги}</ol>'
             f'<div class="pf-two"><div class="pf-need"><h3>{e(ОБ["need"])}</h3>'
             f'<ul>{нужно}</ul></div>'
             f'<div class="pf-lim"><h3>{e(ОБ["limits"])}</h3><p>{e(б["limits"])}</p></div>'
             f'</div></div>')
    return (f'<section id="pf"><div class="pf-in">'
            f'<div class="pf-v" data-route="" data-depth="0"><div class="pf-ph"></div>'
            f'<div class="pf-l"><p class="pf-eyebrow">{e(ОБ["path"])}</p>'
            f'<h2 class="pf-h">{e(б["problem"])}</h2>'
            f'<p class="pf-lede">{e(б["approach"])}</p>'
            f'<span id="how" class="pf-anchor"></span>'
            f'<div class="pf-cta"><button type="button" class="pf-main" data-talk>'
            f'{e(б["cta"])}</button><a href="#works">{e(ОБ["all"])} &rarr;</a></div></div>'
            f'<div class="pf-r">{карта}</div></div></div>'
            f'<div id="pf-switch" data-on="0"><button type="button"></button></div>'
            f'</section>')


ГАЛЕРЕЯ = {'en': '/showcase/', 'ru': '/ru/showcase/', 'es': '/es/showcase/',
           'pt': '/pt/showcase/', 'de': '/de/showcase/'}


def данные(lang: str) -> dict:
    """Содержимое разделов для языка: отрисовкой занимается страница.

    Пять языков целиком в разметку не кладём — это пять копий одного и того
    же. В страницу уходят данные, а вариант под текущее направление
    собирается на месте. Так смена языка меняет и разделы, не перезагружая
    страницу и не теряя разговор.
    """
    ОБ = dict(ОБЩЕЕ.get(lang) or ОБЩЕЕ['ru'])
    ОБ['gallery_url'] = ГАЛЕРЕЯ.get(lang, '/showcase/')
    из = {'labels': dict(ОБ), 'routes': {},
          'niche_hints': {к: list(v) for к, v in ПРИМЕТЫ_НИШИ.items()}}
    for направление, по_языкам in БЛОКИ.items():
        б = по_языкам.get(lang) or по_языкам['ru']
        пример = пример_для(направление, {}, lang)
        из['routes'][направление] = {
            'problem': б['problem'], 'approach': б['approach'],
            'steps': [list(x) for x in б['steps']],
            'need': list(б['need']), 'limits': б['limits'], 'cta': б['cta'],
            # Список, а не один пример: нишу клиента мы узнаём в разговоре,
            # а не при сборке. Выбор делает страница по тем же приметам.
            'examples': [{'title': _т(и.get('title'), lang),
                          'about': _т(и.get('short_description'), lang),
                          'cover': и['cover'], 'url': и['demo_url'],
                          'niche': и.get('niche') or '',
                          'concept': и.get('project_type') == 'concept'}
                         for и in кандидаты(направление)],
        }
    return из


БЛОКИ['growth'] = {
 'ru': _б('Трафик есть, а выручки нет',
          'Смотрим путь от показа до оплаты и ищем, на каком шаге теряются люди. '
          'Чинить начинаем с самого дорогого обрыва, а не с самого заметного.',
          [('Считаем путь', 'Показы, клики, заявки, продажи — по шагам'),
           ('Находим дорогой обрыв', 'Где теряется больше всего денег'),
           ('Меняем одно', 'Так видно, что именно сработало'),
           ('Повторяем', 'Следующий шаг выбираем по замеру')],
          ['Откуда сейчас идёт трафик', 'Сколько заявок и продаж в месяц',
           'Что уже пробовали менять'],
          'Рост в процентах заранее не называем: до замера это обещание, а не расчёт.',
          'Разобрать воронку'),
 'en': _б('Traffic comes in, revenue does not',
          'We follow the path from impression to payment and find the step where '
          'people drop. We fix the most expensive break, not the most visible one.',
          [('Count the path', 'Impressions, clicks, enquiries, sales — step by step'),
           ('Find the costly break', 'Where the most money is lost'),
           ('Change one thing', 'So it is clear what actually worked'),
           ('Repeat', 'The next step follows the measurement')],
          ['Where the traffic comes from now', 'Enquiries and sales per month',
           'What you already tried to change'],
          'We do not name a growth percentage in advance: before measuring that '
          'is a promise, not a calculation.',
          'Work through the funnel'),
 'es': _б('Hay tr\u00e1fico, pero no ingresos',
          'Seguimos el camino de la impresi\u00f3n al pago y buscamos en qu\u00e9 paso se '
          'pierde la gente. Arreglamos el corte m\u00e1s caro, no el m\u00e1s visible.',
          [('Contamos el camino', 'Impresiones, clics, solicitudes, ventas'),
           ('Hallamos el corte caro', 'D\u00f3nde se pierde m\u00e1s dinero'),
           ('Cambiamos una cosa', 'As\u00ed se ve qu\u00e9 funcion\u00f3 de verdad'),
           ('Repetimos', 'El siguiente paso sigue a la medici\u00f3n')],
          ['De d\u00f3nde viene el tr\u00e1fico ahora', 'Solicitudes y ventas al mes',
           'Qu\u00e9 ya intent\u00f3 cambiar'],
          'No damos un porcentaje de crecimiento por adelantado: sin medir eso '
          'es una promesa, no un c\u00e1lculo.',
          'Analizar el embudo'),
 'pt': _б('H\u00e1 tr\u00e1fego, mas n\u00e3o h\u00e1 receita',
          'Seguimos o caminho da impress\u00e3o at\u00e9 o pagamento e achamos em que passo '
          'as pessoas saem. Consertamos a quebra mais cara, n\u00e3o a mais vis\u00edvel.',
          [('Contamos o caminho', 'Impress\u00f5es, cliques, solicita\u00e7\u00f5es, vendas'),
           ('Achamos a quebra cara', 'Onde se perde mais dinheiro'),
           ('Mudamos uma coisa', 'Assim d\u00e1 para ver o que funcionou'),
           ('Repetimos', 'O pr\u00f3ximo passo segue a medi\u00e7\u00e3o')],
          ['De onde vem o tr\u00e1fego hoje', 'Solicita\u00e7\u00f5es e vendas por m\u00eas',
           'O que voc\u00ea j\u00e1 tentou mudar'],
          'N\u00e3o damos uma porcentagem de crescimento antes: sem medir isso \u00e9 '
          'promessa, n\u00e3o c\u00e1lculo.',
          'Analisar o funil'),
 'de': _б('Traffic kommt, Umsatz nicht',
          'Wir gehen den Weg von der Einblendung bis zur Zahlung und suchen den '
          'Schritt, an dem Leute abspringen. Wir beheben den teuersten Bruch.',
          [('Weg z\u00e4hlen', 'Einblendungen, Klicks, Anfragen, Verk\u00e4ufe'),
           ('Teuren Bruch finden', 'Wo das meiste Geld verloren geht'),
           ('Eines \u00e4ndern', 'So ist klar, was wirklich gewirkt hat'),
           ('Wiederholen', 'Der n\u00e4chste Schritt folgt der Messung')],
          ['Woher der Traffic heute kommt', 'Anfragen und Verk\u00e4ufe pro Monat',
           'Was Sie schon ge\u00e4ndert haben'],
          'Eine Wachstumszahl nennen wir nicht im Voraus: ohne Messung ist das '
          'ein Versprechen, keine Rechnung.',
          'Den Funnel durchgehen'),
}

БЛОКИ['accounting'] = {
 'ru': _б('Книги отстали, а сроки — нет',
          'Сначала понимаем, за какой период и что именно не закрыто. '
          'Потом — что горит по срокам, а что можно разобрать спокойно.',
          [('Смотрим период', 'За сколько месяцев книги не в порядке'),
           ('Отделяем срочное', 'Что с дедлайнами, что без'),
           ('Разбираем завал', 'По порядку, а не всё сразу'),
           ('Ставим учёт', 'Чтобы это не повторилось в следующем году')],
          ['Форма компании и штат', 'За какой период не закрыто',
           'Есть ли письма от налоговой'],
          'Мы не оказываем лицензированных налоговых и юридических консультаций. '
          'Где нужен CPA или юрист, мы это говорим, а не заменяем их собой.',
          'Разобрать ситуацию'),
 'en': _б('The books are behind, the deadlines are not',
          'First we work out which period is open and what exactly is missing. '
          'Then what is urgent and what can be cleaned up calmly.',
          [('Look at the period', 'How many months are not in order'),
           ('Separate the urgent', 'What has deadlines and what does not'),
           ('Clear the backlog', 'In order, not all at once'),
           ('Set up bookkeeping', 'So next year does not repeat this')],
          ['Entity type and headcount', 'Which period is open',
           'Whether letters from the tax authority arrived'],
          'We do not provide licensed tax or legal advice. Where a CPA or a '
          'lawyer is needed, we say so instead of standing in for them.',
          'Work through the situation'),
 'es': _б('La contabilidad est\u00e1 atrasada, los plazos no',
          'Primero vemos qu\u00e9 per\u00edodo est\u00e1 abierto y qu\u00e9 falta exactamente. '
          'Luego qu\u00e9 es urgente y qu\u00e9 se puede ordenar con calma.',
          [('Vemos el per\u00edodo', 'Cu\u00e1ntos meses no est\u00e1n en orden'),
           ('Separamos lo urgente', 'Qu\u00e9 tiene plazo y qu\u00e9 no'),
           ('Ordenamos el atraso', 'Por partes, no todo a la vez'),
           ('Montamos el registro', 'Para que el pr\u00f3ximo a\u00f1o no se repita')],
          ['Forma jur\u00eddica y plantilla', 'Qu\u00e9 per\u00edodo est\u00e1 abierto',
           'Si llegaron cartas de Hacienda'],
          'No damos asesor\u00eda fiscal ni legal licenciada. Donde hace falta un CPA '
          'o un abogado, lo decimos en vez de sustituirlos.',
          'Analizar la situaci\u00f3n'),
 'pt': _б('A contabilidade atrasou, os prazos n\u00e3o',
          'Primeiro vemos qual per\u00edodo est\u00e1 aberto e o que exatamente falta. '
          'Depois o que \u00e9 urgente e o que d\u00e1 para organizar com calma.',
          [('Vemos o per\u00edodo', 'Quantos meses est\u00e3o fora de ordem'),
           ('Separamos o urgente', 'O que tem prazo e o que n\u00e3o tem'),
           ('Organizamos o atraso', 'Por partes, n\u00e3o tudo de uma vez'),
           ('Montamos o registro', 'Para o pr\u00f3ximo ano n\u00e3o repetir')],
          ['Forma jur\u00eddica e equipe', 'Qual per\u00edodo est\u00e1 aberto',
           'Se chegaram cartas do fisco'],
          'N\u00e3o prestamos consultoria fiscal ou jur\u00eddica licenciada. Onde \u00e9 preciso '
          'um contador ou advogado, dizemos isso em vez de substitu\u00ed-los.',
          'Analisar a situa\u00e7\u00e3o'),
 'de': _б('Die B\u00fccher sind im R\u00fcckstand, die Fristen nicht',
          'Zuerst kl\u00e4ren wir, welcher Zeitraum offen ist und was genau fehlt. '
          'Dann, was eilt und was in Ruhe aufger\u00e4umt werden kann.',
          [('Zeitraum ansehen', 'Wie viele Monate nicht in Ordnung sind'),
           ('Dringendes trennen', 'Was Fristen hat und was nicht'),
           ('R\u00fcckstand aufr\u00e4umen', 'Der Reihe nach, nicht alles auf einmal'),
           ('Buchhaltung aufsetzen', 'Damit sich das n\u00e4chstes Jahr nicht wiederholt')],
          ['Rechtsform und Mitarbeiterzahl', 'Welcher Zeitraum offen ist',
           'Ob Schreiben vom Finanzamt kamen'],
          'Wir leisten keine lizenzierte Steuer- oder Rechtsberatung. Wo ein CPA '
          'oder Anwalt n\u00f6tig ist, sagen wir das, statt sie zu ersetzen.',
          'Die Lage durchgehen'),
}


БЛОКИ['infrastructure'] = {
 'ru': _б('Функции, ради которых нанимать дорого',
          'Смотрим, какие задачи возникают регулярно, но не набирают на полную '
          'ставку. Их закрывают инструментом или частичной занятостью.',
          [('Считаем объём', 'Сколько часов в месяц это правда занимает'),
           ('Отделяем повторяемое', 'Что можно описать правилом, а что нет'),
           ('Берём инструмент', 'Там, где он дешевле и надёжнее человека'),
           ('Оставляем человеку', 'То, где нужно решение, а не исполнение')],
          ['Какие задачи возникают регулярно', 'Сколько времени они занимают',
           'Что сейчас используете'],
          'Мы не агентство по найму и не кадровое сопровождение: подбором '
          'сотрудников и оформлением мы не занимаемся.',
          'Разобрать задачи'),
 'en': _б('Functions too small to hire for',
          'We look at which tasks come back regularly but never add up to a '
          'full role. Those are covered by a tool or part-time help.',
          [('Count the volume', 'How many hours a month it really takes'),
           ('Separate the repeatable', 'What can be written as a rule and what cannot'),
           ('Use a tool', 'Where it is cheaper and steadier than a person'),
           ('Leave to a person', 'Where judgement is needed, not execution')],
          ['Which tasks come back regularly', 'How much time they take',
           'What you use now'],
          'We are not a recruiting agency and do not handle hiring or employment '
          'paperwork.',
          'Work through the tasks'),
 'es': _б('Funciones por las que contratar sale caro',
          'Vemos qu\u00e9 tareas vuelven con regularidad pero no llegan a un puesto '
          'completo. Esas se cubren con una herramienta o jornada parcial.',
          [('Contamos el volumen', 'Cu\u00e1ntas horas al mes lleva de verdad'),
           ('Separamos lo repetible', 'Qu\u00e9 se puede escribir como regla'),
           ('Tomamos una herramienta', 'Donde sale m\u00e1s barata y estable'),
           ('Dejamos a la persona', 'Donde hace falta criterio, no ejecuci\u00f3n')],
          ['Qu\u00e9 tareas vuelven con regularidad', 'Cu\u00e1nto tiempo llevan',
           'Qu\u00e9 usa ahora'],
          'No somos agencia de selecci\u00f3n ni gestionamos contrataci\u00f3n ni n\u00f3minas.',
          'Analizar las tareas'),
 'pt': _б('Fun\u00e7\u00f5es caras demais para contratar',
          'Vemos quais tarefas voltam com regularidade mas n\u00e3o chegam a um cargo '
          'inteiro. Essas s\u00e3o cobertas por ferramenta ou meio per\u00edodo.',
          [('Contamos o volume', 'Quantas horas por m\u00eas isso leva de fato'),
           ('Separamos o repet\u00edvel', 'O que d\u00e1 para escrever como regra'),
           ('Usamos ferramenta', 'Onde sai mais barata e est\u00e1vel'),
           ('Deixamos \u00e0 pessoa', 'Onde \u00e9 preciso crit\u00e9rio, n\u00e3o execu\u00e7\u00e3o')],
          ['Quais tarefas voltam sempre', 'Quanto tempo levam',
           'O que voc\u00ea usa hoje'],
          'N\u00e3o somos ag\u00eancia de recrutamento e n\u00e3o cuidamos de contrata\u00e7\u00e3o.',
          'Analisar as tarefas'),
 'de': _б('Aufgaben, f\u00fcr die Einstellen zu teuer ist',
          'Wir sehen, welche Aufgaben regelm\u00e4\u00dfig wiederkommen, aber keine ganze '
          'Stelle f\u00fcllen. Die deckt ein Tool oder Teilzeit ab.',
          [('Umfang z\u00e4hlen', 'Wie viele Stunden im Monat es wirklich kostet'),
           ('Wiederholbares trennen', 'Was sich als Regel schreiben l\u00e4sst'),
           ('Tool nehmen', 'Wo es g\u00fcnstiger und stabiler ist als ein Mensch'),
           ('Mensch lassen', 'Wo Urteil n\u00f6tig ist, nicht Ausf\u00fchrung')],
          ['Welche Aufgaben regelm\u00e4\u00dfig wiederkommen', 'Wie viel Zeit sie kosten',
           'Was Sie heute nutzen'],
          'Wir sind keine Personalagentur und \u00fcbernehmen weder Einstellung noch '
          'Arbeitspapiere.',
          'Die Aufgaben durchgehen'),
}

БЛОКИ['fulfillment'] = {
 'ru': _б('Вы переросли отгрузку своими силами',
          'Считаем, во что обходится текущая схема, и сравниваем с тем, что '
          'дают склад или 3PL под ваш объём и географию.',
          [('Считаем объём', 'Заказы в месяц, вес, габариты, сезонность'),
           ('Смотрим географию', 'Куда везёте и откуда разумнее'),
           ('Сравниваем схемы', 'Свои силы, склад, 3PL — по деньгам и срокам'),
           ('Переносим', 'Поэтапно, чтобы не встать на переходе')],
          ['Сколько заказов в месяц', 'Откуда и куда отгружаете',
           'Что именно не устраивает сейчас'],
          'Мы не перевозчик и не таможенный брокер: тарифы и сроки определяет '
          'подрядчик, а не мы.',
          'Разобрать отгрузку'),
 'en': _б('You have outgrown shipping it yourself',
          'We count what the current setup really costs and compare it with what '
          'a warehouse or 3PL gives at your volume and geography.',
          [('Count the volume', 'Orders per month, weight, size, seasonality'),
           ('Look at geography', 'Where you ship and where from makes sense'),
           ('Compare setups', 'In-house, warehouse, 3PL — by cost and time'),
           ('Move', 'In stages, so nothing stops mid-transition')],
          ['Orders per month', 'Where you ship from and to',
           'What exactly does not work now'],
          'We are not a carrier or a customs broker: rates and transit times are '
          'set by the provider, not by us.',
          'Work through shipping'),
 'es': _б('Ya no da abasto enviar por su cuenta',
          'Calculamos cu\u00e1nto cuesta de verdad el esquema actual y lo comparamos '
          'con lo que dan un almac\u00e9n o un 3PL a su volumen.',
          [('Contamos el volumen', 'Pedidos al mes, peso, tama\u00f1o, temporada'),
           ('Miramos la geograf\u00eda', 'A d\u00f3nde env\u00eda y desde d\u00f3nde conviene'),
           ('Comparamos esquemas', 'Propio, almac\u00e9n, 3PL — en dinero y plazos'),
           ('Migramos', 'Por etapas, para no parar en la transici\u00f3n')],
          ['Pedidos al mes', 'Desde d\u00f3nde y hacia d\u00f3nde env\u00eda',
           'Qu\u00e9 no funciona ahora'],
          'No somos transportista ni agente de aduanas: tarifas y plazos los fija '
          'el proveedor, no nosotros.',
          'Analizar el env\u00edo'),
 'pt': _б('Voc\u00ea j\u00e1 passou do envio por conta pr\u00f3pria',
          'Calculamos quanto custa de fato o esquema atual e comparamos com o que '
          'um armaz\u00e9m ou 3PL oferece no seu volume.',
          [('Contamos o volume', 'Pedidos por m\u00eas, peso, tamanho, sazonalidade'),
           ('Olhamos a geografia', 'Para onde envia e de onde faz sentido'),
           ('Comparamos esquemas', 'Pr\u00f3prio, armaz\u00e9m, 3PL — em dinheiro e prazo'),
           ('Migramos', 'Por etapas, para n\u00e3o parar na transi\u00e7\u00e3o')],
          ['Pedidos por m\u00eas', 'De onde e para onde envia',
           'O que exatamente n\u00e3o funciona hoje'],
          'N\u00e3o somos transportadora nem despachante: tarifas e prazos quem define '
          '\u00e9 o fornecedor, n\u00e3o n\u00f3s.',
          'Analisar o envio'),
 'de': _б('Selbst versenden reicht nicht mehr',
          'Wir rechnen, was das heutige Vorgehen wirklich kostet, und vergleichen '
          'es mit Lager oder 3PL bei Ihrem Volumen.',
          [('Volumen z\u00e4hlen', 'Bestellungen pro Monat, Gewicht, Gr\u00f6\u00dfe, Saison'),
           ('Geografie ansehen', 'Wohin Sie liefern und von wo es sinnvoll ist'),
           ('Varianten vergleichen', 'Selbst, Lager, 3PL — nach Geld und Zeit'),
           ('Umziehen', 'In Etappen, damit nichts im \u00dcbergang stehenbleibt')],
          ['Bestellungen pro Monat', 'Von wo und wohin Sie versenden',
           'Was heute konkret nicht passt'],
          'Wir sind weder Spediteur noch Zollagent: Tarife und Laufzeiten bestimmt '
          'der Dienstleister, nicht wir.',
          'Den Versand durchgehen'),
}


# Внутренние статусы партнёрств клиенту не показываются: ему важно, что
# будет дальше, а не кто у нас в каком состоянии согласования. Пока по
# направлению нет подтверждённой передачи, следующий шаг — наш разбор, и
# так это и написано, без объяснения причин.
#
# Что передача действительно доступна, решает routing.delivery по реестру:
# на сайте это отражается формулировкой, а не названием провайдера.
БЕЗ_ПЕРЕДАЧИ = {
    'ru': ' Разберём задачу и определим доступный следующий шаг.',
    'en': ' We will work through the task and determine the next step available.',
    'es': ' Analizaremos la tarea y determinaremos el siguiente paso disponible.',
    'pt': ' Vamos analisar a tarefa e determinar o pr\u00f3ximo passo dispon\u00edvel.',
    'de': ' Wir gehen die Aufgabe durch und bestimmen den verf\u00fcgbaren n\u00e4chsten Schritt.',
}
for _язык, _фраза in БЕЗ_ПЕРЕДАЧИ.items():
    if _фраза not in БЛОКИ['funding'][_язык]['limits']:
        БЛОКИ['funding'][_язык]['limits'] += _фраза
