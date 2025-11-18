from flask import Flask, request, jsonify
from upload import save_uploaded_file
from ai_processor import process_text

app = Flask(name)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Файл не отправлен"}), 400

    file = request.files["file"]
    path = save_uploaded_file(file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    course = process_text(text)
    return jsonify({"course": course})

if name == "main":
    app.run(host="127.0.0.1", port=5000, debug=True)
