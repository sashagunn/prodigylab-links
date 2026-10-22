/**
 * Lead form attribution and success handling for the localized home pages.
 * The normal Formspree action remains as a fallback when JavaScript is unavailable.
 */
(function () {
  'use strict';

  var attributionKeys = [
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_content',
    'utm_term',
    'fbclid'
  ];

  function setField(form, name, value) {
    var field = form.querySelector('[name="' + name + '"]');
    if (field) field.value = value || '';
  }

  function init() {
    var params = new URLSearchParams(window.location.search);

    document.querySelectorAll('form[data-lead-form]').forEach(function (form) {
      attributionKeys.forEach(function (key) {
        setField(form, key, params.get(key));
      });
      setField(form, 'landing_page', window.location.href);
      setField(form, 'referrer', document.referrer);

      if (typeof window.prodigyAISource === 'function') {
        var aiSource = window.prodigyAISource();
        setField(form, 'ai_source', aiSource && aiSource.source);
      }

      form.addEventListener('submit', async function (event) {
        event.preventDefault();
        if (!form.reportValidity()) return;

        var button = form.querySelector('[type="submit"]');
        var status = form.querySelector('[data-form-status]');
        var success = document.querySelector('[data-lead-success]');
        var idleLabel = button.textContent;
        button.disabled = true;
        button.textContent = button.dataset.sending || 'Sending…';
        if (status) status.textContent = '';

        try {
          var response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { Accept: 'application/json' }
          });
          if (!response.ok) throw new Error('Lead form request failed');

          if (typeof window.fbq === 'function') {
            window.fbq('track', 'Lead', {
              content_name: 'initial_business_assessment',
              content_category: 'business_diagnosis'
            });
          }

          form.reset();
          form.classList.add('hidden');
          if (success) {
            success.classList.remove('hidden');
            success.setAttribute('tabindex', '-1');
            success.focus();
          }
        } catch (error) {
          button.disabled = false;
          button.textContent = idleLabel;
          if (status) {
            status.textContent = form.dataset.error || 'Could not send the request. Please try again.';
          }
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
