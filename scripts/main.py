from modules import youtube_parser, whisper_transcribe, predict

# 1. Сілтемелерді жүктеу
links = youtube_parser.load_links("data/example_links.txt")

# 2. Әрбір сілтеме бойынша өңдеу
for link in links:
    print(f"\n🔗 Сілтеме өңделуде: {link}")

    # Комментарийлерді алу
    comments_text = youtube_parser.process(link)
    print("\n💬 Комментарийлер:")
    print(comments_text)

    # Аудионы мәтінге айналдыру
    audio_text = whisper_transcribe.process_audio(link)
    print("\n🗣 Видео транскрипциясы:")
    print(audio_text)

    # Комментарий + аудио біріктіру
    final_text = comments_text + "\n" + audio_text

    # Классификация (осында өзгерту керек)
    result, predicted_class = predict.predict(final_text)

    # Нәтиже шығару
    print("\n📋 Пайыздар:")
    for k, v in result.items():
        print(f"  - {k}: {v}%")
    
    print(f"\n🏆 Негізгі класс: {predicted_class}")
