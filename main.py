from flask import Flask, request, session, jsonify, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import logging
from ai_processor import process_text

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = 'your_secret_key'
CORS(app)
logging.basicConfig(level=logging.INFO)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_users_table():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

create_users_table()

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({"error": "Заполните все поля"}), 400
    
    hashed_password = generate_password_hash(password)
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Регистрация успешна!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Пользователь с таким email или именем уже существует"}), 409

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return jsonify({"message": "Вход выполнен успешно", "username": user["username"]}), 200
    else:
        return jsonify({"error": "Неверные почта или пароль"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Успешный выход"}), 200

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
        course = process_text(url)
        return jsonify({"course": course}), 200
    except Exception as e:
        logging.exception("Ошибка при генерации курса")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
