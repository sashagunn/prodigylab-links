/**
 * ai-referrals.js — определение переходов из AI-систем.
 *
 * Зачем: в обычной аналитике переход из ChatGPT или Perplexity выглядит как
 * "прямой заход" или теряется в referral-мусоре, и канал невозможно оценить.
 * Скрипт помечает первый источник и передаёт его как событие Meta Pixel.
 *
 * Что НЕ собирается: ничего персонального. Только домен источника и адрес
 * страницы входа. Ни email, ни телефон, ни содержимое форм.
 */
(function () {
  'use strict';

  // Домены AI-систем. Список публичный и проверяемый — выдуманных здесь нет.
  var SOURCES = [
    ['chatgpt.com', 'ChatGPT'],
    ['chat.openai.com', 'ChatGPT'],
    ['openai.com', 'OpenAI'],
    ['perplexity.ai', 'Perplexity'],
    ['copilot.microsoft.com', 'Microsoft Copilot'],
    ['bing.com', 'Bing'],
    ['claude.ai', 'Claude'],
    ['gemini.google.com', 'Gemini'],
    ['you.com', 'You.com'],
    ['phind.com', 'Phind'],
    ['poe.com', 'Poe'],
    ['duckduckgo.com', 'DuckDuckGo']
  ];

  var KEY = 'pl_ai_src';

  function detect() {
    var qs = new URLSearchParams(location.search);

    // 1. Явная UTM-метка, если её проставили (ChatGPT иногда передаёт utm_source=chatgpt.com)
    var utm = (qs.get('utm_source') || '').toLowerCase();
    if (utm) {
      for (var i = 0; i < SOURCES.length; i++) {
        if (utm.indexOf(SOURCES[i][0].split('.')[0]) !== -1) {
          return { name: SOURCES[i][1], how: 'utm', raw: utm };
        }
      }
    }

    // 2. Referrer
    var ref = document.referrer || '';
    if (ref) {
      var host = '';
      try { host = new URL(ref).hostname.replace(/^www\./, ''); } catch (e) { host = ''; }
      for (var j = 0; j < SOURCES.length; j++) {
        if (host === SOURCES[j][0] || host.indexOf('.' + SOURCES[j][0]) !== -1) {
          return { name: SOURCES[j][1], how: 'referrer', raw: host };
        }
      }
    }
    return null;
  }

  function store(hit) {
    // Первое касание не перезаписывается: важно, откуда человек пришёл впервые,
    // а не с какой вкладки вернулся.
    try {
      if (localStorage.getItem(KEY)) return JSON.parse(localStorage.getItem(KEY));
      var rec = { source: hit.name, how: hit.how, raw: hit.raw, landing: location.pathname, ts: new Date().toISOString() };
      localStorage.setItem(KEY, JSON.stringify(rec));
      return rec;
    } catch (e) { return null; }
  }

  var hit = detect();
  if (hit) {
    var rec = store(hit) || { source: hit.name, landing: location.pathname };
    // Своё событие в пикселе — чтобы AI-канал был виден в отчётах Meta
    // и его можно было сопоставить с Lead / CompleteRegistration / Purchase.
    if (typeof window.fbq === 'function') {
      window.fbq('trackCustom', 'AIReferral', {
        ai_source: rec.source,
        landing_page: rec.landing,
        detection: hit.how
      });
    }
    document.documentElement.setAttribute('data-ai-source', rec.source);
  }

  // Доступ для отладки и для передачи в форму/бота при желании.
  window.prodigyAISource = function () {
    try { return JSON.parse(localStorage.getItem(KEY)); } catch (e) { return null; }
  };
})();
