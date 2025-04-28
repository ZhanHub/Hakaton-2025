# D:\Hakaton\scripts\main_instagram_batch.py

from modules import instagram_parser, whisper_transcribe, predict

def process_instagram_link(link):
    print(f"\n🔗 Сілтеме өңделуде: {link}")
    post_text, video_path = instagram_parser.process_instagram(link)

    audio_text = ""
    if video_path:
        print("\n🗣 Видео аудиосын транскрипция жасап жатырмыз...")
        audio_text = whisper_transcribe.process_audio(video_path)

    final_text = post_text.strip() + "\n" + audio_text.strip()

    if not final_text.strip():
        print("⚠ Контент табылмады (пост та, видео да жоқ). Өткізіп жіберілді.")
        return

    print("\n🤖 Классификация басталды...")
    result, predicted_class = predict.predict(final_text)

    print("\n📋 Пайыздар:")
    for k, v in result.items():
        print(f"  - {k}: {v}%")
    
    print(f"\n🏆 Негізгі класс: {predicted_class}")

def load_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]
    return links

if __name__ == "__main__":
    print("🚀 'data/instagram_links.txt' файлын оқып жатырмыз...")
    links = load_links('data/instagram_links.txt')

    if not links:
        print("⚠ Файл бос немесе сілтемелер табылмады!")
    else:
        for link in links:
            process_instagram_link(link)
