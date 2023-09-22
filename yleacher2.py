import os
from pytube import YouTube
from telegram import Bot
from telegram import InputFile
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '6675228824:AAFdQYBLNl8OYQ581dOlZLv0mcqK4c4iP9U'

def download_and_send_video(update, context):
    chat_id = update.effective_chat.id
    video_url = update.message.text

    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    if stream:
        video_path = stream.download()
        with open(video_path, 'rb') as video_file:
            context.bot.send_video(chat_id=chat_id, video=InputFile(video_file))
        os.remove(video_path)
    else:
        context.bot.send_message(chat_id=chat_id, text='No suitable video stream found.')

def start(update, context):
    update.message.reply_text("Send a YouTube video link and I'll download and send it to you!")

def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_and_send_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
