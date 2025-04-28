import whisper
import os

# FFmpeg жолын көрсету
FFMPEG_PATH = r"D:\Hakaton\ffmpeg\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# Whisper моделін жүктеу
model = whisper.load_model("base")

# 🔥 Локал файлды транскрипция жасау
def process_audio_file(audio_file_path):
    if not os.path.exists(audio_file_path):
        print(f"❌ Файл табылмады: {audio_file_path}")
        return ""

    result = model.transcribe(audio_file_path)
    print(f"✅ Транскрипция аяқталды: {audio_file_path}")
    return result["text"]

# 🔥 YouTube/Instagram ссылкасынан аудио алу (арнайы YouTube үшін)
def download_audio(link, output_path="temp_audio.%(ext)s"):
    import yt_dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': False,
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    final_path = "temp_audio.mp3"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except Exception as e:
            print("❌ Аудионы жүктеу сәтсіз:", e)
            return None

    if os.path.exists(final_path):
        print("✅ Аудио сәтті жүктелді:", final_path)
        return final_path
    else:
        print("❌ Аудио файл табылмады.")
        return None

# 🔥 YouTube үшін толық процесс
def process_audio(link):
    audio_path = download_audio(link)
    if audio_path is None:
        return ""

    result = model.transcribe(audio_path)
    os.remove(audio_path)
    return result["text"]
