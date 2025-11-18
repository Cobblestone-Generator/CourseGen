from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_processor import process_text
import logging

# Инициализация приложения Flask (static_folder и template_folder по умолчанию 'static' и 'templates')
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Разрешаем запросы с фронтенда (можно настроить конкретные origin)

# Простой логгер
logging.basicConfig(level=logging.INFO)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """
    Ожидает JSON: { "url": "<youtube_url>" }
    Возвращает JSON: { "course": ... } или { "error": "..." }
    """
    if not request.is_json:
        return jsonify({"error": 'Ожидается JSON с полем "url"'}), 400

    data = request.get_json()
    url = data.get("url") or data.get("video_url") or data.get("videoUrl")
    if not url:
        return jsonify({"error": 'Поле "url" не передано'}), 400

    try:
        # Важно: ai_processor.process_text может ожидать raw text.
        # Если он ожидает текст, добавьте на сервере шаг извлечения транскрипта из YouTube,
        # например с помощью yt-transcript-api или youtube-dl, и передавайте текст сюда.
        course = process_text(url)
        return jsonify({"course": course}), 200
    except Exception as e:
        logging.exception("Ошибка при генерации курса")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Запускаем на 0.0.0.0 для доступа извне (локально оставьте 127.0.0.1 при необходимости)
    app.run(host="0.0.0.0", port=5000, debug=True)
