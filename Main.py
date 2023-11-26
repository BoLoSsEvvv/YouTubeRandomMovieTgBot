import telebot
import random
from googleapiclient.discovery import build
from telebot import types

TOKEN = " "

YOUTUBE_API_KEY = " "

bot = telebot.TeleBot(TOKEN)

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Функция для получения рандомного видео по запросу
def get_random_video(query):
    try:
        # Поиск видео на YouTube по запросу
        request = youtube.search().list(
            q=query,
            part='id',
            type='video',
            maxResults=5
        )
        response = request.execute()

        videos = [item['id']['videoId'] for item in response['items']]
        if videos:
            random_video_id = random.choice(videos)
            video_url = f'https://www.youtube.com/watch?v={random_video_id}'
            return video_url
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении видео: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Какое видео вы хотите посмотреть?")

@bot.message_handler(func=lambda message: True)
def handle_video_request(message):
    user_query = message.text
    try:
        video_url = get_random_video(user_query)
        if video_url:
            bot.send_message(message.chat.id, f"Вот видео по вашему запросу: {video_url}")
        else:
            bot.send_message(message.chat.id, "К сожалению, по вашему запросу ничего не найдено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при поиске видео: {e}")

# Запуск бота
bot.polling(none_stop=True)
