def process_text(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    if not lines:
        return "Нет текста для обработки."

    chapter_size = max(3, len(lines) // 4)
    chapters = []

    for i in range(0, len(lines), chapter_size):
        part = lines[i:i + chapter_size]

        title = f"Глава {len(chapters) + 1}"
        body = "\n".join(part)
        summary = f"Краткое резюме: {part[-1]}"

        chapters.append(f"{title}\n\n{body}\n\n{summary}\n")

    return "\n".join(chapters)
