# main_telegram.py
import asyncio
from modules import telegram_parser, whisper_transcribe, predict

def classify_text(full_text):
    print("\n🤖 Классификация басталды...")
    result, predicted_class = predict.predict(full_text)

    print("\n📋 Пайыздар:")
    for k, v in result.items():
        print(f"  - {k}: {v}%")

    print(f"\n🏆 Негізгі класс: {predicted_class}")

async def main():
    print("🚀 Телеграм сілтемесін енгізіңіз:")
    link = input(">>> ")

    text, media_path = await telegram_parser.process_telegram_link(link)

    audio_text = ""
    if media_path:
        print("\n🗣 Аудионы текстке айналдырып жатырмыз...")
        audio_text = whisper_transcribe.process_audio(media_path)
        if os.path.exists(media_path):
            os.remove(media_path)

    final_text = text.strip() + "\n" + audio_text.strip()

    if not final_text.strip():
        print("⚠ Контент табылмады (пост та, аудио/видео да жоқ).")
    else:
        classify_text(final_text)

    await telegram_parser.close_client()

if __name__ == "__main__":
    asyncio.run(main())
