// static/generate.js
// Скрипт отправляет POST /api/generate с JSON { url: "..." }
// Ожидается ответ JSON: { course: {...} } или { error: "..." }

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('create-course');
  const btnText = document.getElementById('create-course-text');
  const input = document.getElementById('video-url');
  const resultBox = document.getElementById('generator-result');

  if (!btn || !input || !resultBox) return;

  function showResult(content, isError = false) {
    resultBox.classList.remove('hidden');
    resultBox.innerHTML = '';
    if (isError) {
      resultBox.classList.add('border-red-200', 'text-red-700');
    } else {
      resultBox.classList.remove('border-red-200', 'text-red-700');
    }
    if (typeof content === 'string') {
      resultBox.textContent = content;
    } else {
      // pretty-print JSON or render basic structure
      const pre = document.createElement('pre');
      pre.className = 'whitespace-pre-wrap text-sm';
      pre.textContent = JSON.stringify(content, null, 2);
      resultBox.appendChild(pre);
    }
  }

  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    const url = input.value && input.value.trim();
    if (!url) {
      showResult('Пожалуйста, вставьте ссылку на YouTube видео.', true);
      return;
    }

    // Блокируем кнопку и показываем спиннер
    btn.disabled = true;
    const oldText = btnText.textContent;
    btnText.innerHTML = '<span class="spinner" style="color:inherit"></span> Генерация...';

    try {
      const resp = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });

      if (!resp.ok) {
        let errText = `Ошибка ${resp.status}`;
        try {
          const errJson = await resp.json();
          errText += ': ' + (errJson.error || JSON.stringify(errJson));
        } catch (_) {}
        showResult(errText, true);
        return;
      }

      const data = await resp.json();
      if (data.error) {
        showResult(data.error, true);
        return;
      }

      if (data.course) {
        // Показываем получённый курс (можно изменить под ваш формат)
        showResult(data.course, false);
      } else {
        showResult('Сервер вернул пустой ответ или неверный формат.', true);
      }
    } catch (err) {
      showResult('Сетевая ошибка: ' + (err.message || String(err)), true);
    } finally {
      btn.disabled = false;
      btnText.textContent = oldText;
    }
  });
});
