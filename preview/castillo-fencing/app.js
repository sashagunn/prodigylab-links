import {company} from './company.js';
import {createBrief} from './configurator.js';
const form = document.querySelector('form');
const output = document.querySelector('#brief');
const copy = document.querySelector('#copy');
const status = document.querySelector('#status');
for (const material of company.materials) { const option = document.createElement('option'); option.value = material; option.textContent = material; form.elements.material.append(option); }
form.addEventListener('input', () => { output.value = ''; copy.disabled = true; status.textContent = 'Selections changed. Generate a new brief.'; });
form.addEventListener('submit', event => {
  event.preventDefault();
  try { output.value = createBrief(Object.fromEntries(new FormData(form))); copy.disabled = false; status.textContent = 'Your brief is ready. Nothing has been sent.'; output.focus(); }
  catch (error) { output.value = ''; copy.disabled = true; status.textContent = error.message; }
});
copy.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(output.value); status.textContent = 'Brief copied. Nothing has been sent.'; }
  catch { output.focus(); output.select(); status.textContent = 'Select and copy the brief manually (Ctrl+C or Command+C).'; }
});

// Срок доступа (§2). Страница статическая, поэтому проверка клиентская: это
// вежливое закрытие для адресата, а не замок — кто захочет, посмотрит исходник.
// Серверная отсечка появится, когда демо переедут на динамические маршруты.
const срок = document.querySelector('meta[name="pf-expires"]')?.content;
if (срок && Date.now() >= Date.parse(срок)) {
  for (const s of document.querySelectorAll('main > section')) s.hidden = true;
  const блок = document.querySelector('#expired');
  if (блок) blockShow(блок);
}
function blockShow(el) { el.hidden = false; }
