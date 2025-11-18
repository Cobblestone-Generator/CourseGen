from text_extractor import extract_text
from course_generator import generate_course
from file_utils import download_youtube_audio, is_youtube_url

def main():
    print("Введите путь к файлу или ссылку на YouTube:")
    source = input("> ").strip()

    if is_youtube_url(source):
        print("Скачиваю аудио с YouTube...")
        file_path = download_youtube_audio(source)
        print("Аудио скачано:", file_path)
    else:
        file_path = source

    print("Извлекаю текст...")
    text = extract_text(file_path)

    print("Создаю курс...")
    course = generate_course(text)

    print("\n===== ГОТОВЫЙ КУРС =====\n")
    print(course)


if name == "main":
    main()
