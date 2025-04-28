# telegram_parser.py
from telethon import TelegramClient
import asyncio
import os

# ТВОЙ API_ID и API_HASH
api_id = 29805977
api_hash = 'bcccc03da521f223d08ff14ea5663885'

# Клиентті дайындау
client = TelegramClient('session_name', api_id, api_hash)

async def process_telegram_link(link):
    """Телеграм сілтемесін өңдеу"""
    await client.start()

    # Сілтемеден канал және пост ID бөліп алу
    if '/c/' in link:
        # Приват топтар үшін
        parts = link.split('/c/')[1].split('/')
        chat_id = int('-100' + parts[0])
        message_id = int(parts[1])
    else:
        # Публичный каналдар үшін
        parts = link.split('/')
        chat_username = parts[3]
        message_id = int(parts[4])

    try:
        message = await client.get_messages(chat_username if '/c/' not in link else chat_id, ids=message_id)
        
        text = message.text or ""
        
        # Егер аудио/видео болса
        if message.audio or message.voice or message.video:
            media_type = 'audio' if (message.audio or message.voice) else 'video'
            print(f"⬇ Медианы жүктеп жатырмыз... ({media_type})")

            path = await message.download_media(file="temp_media")
            print(f"✅ Медиа жүктелді: {path}")
            return text.strip(), path
        else:
            return text.strip(), None

    except Exception as e:
        print(f"❌ Қате орын алды: {e}")
        return "", None

async def close_client():
    await client.disconnect()
