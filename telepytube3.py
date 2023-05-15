import telebot
import pytube
import subprocess
import os

# Initialize the Telegram bot using the bot token
bot = telebot.TeleBot("6252170415:AAGAbum5zUJwprkuFZSjV_CKZKvIp9cwSp8")

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I'm a YouTube downloader bot. Send me the URL of the YouTube video you want to download.")

# Handler for receiving a message with a YouTube video URL
@bot.message_handler(func=lambda message: True)
def download_video(message):
    try:
        # Create a YouTube object using the URL
        youtube = pytube.YouTube(message.text)

        # Display the available video formats and resolutions
        available_formats = "\n".join([str(stream) for stream in youtube.streams])
        bot.send_message(message.chat.id, f"Available formats and resolutions:\n{available_formats}")

        # Prompt the user to select a resolution and format
        msg = bot.send_message(message.chat.id, "Enter the resolution (e.g., 1080p): ")
        bot.register_next_step_handler(msg, select_resolution)

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Handler for receiving the selected resolution, and prompting for the format
def select_resolution(message):
    try:
        resolution = message.text

        msg = bot.send_message(message.chat.id, "Enter the format (e.g., mp4): ")
        bot.register_next_step_handler(msg, lambda format_message: download_selected_format(resolution, format_message))

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Handler for receiving the selected format, downloading the video, and sending it to the user
def download_selected_format(resolution, message):
    try:
        format = message.text

        # Filter the streams based on the user's inputs for resolution and format
        stream = pytube.YouTube(video_url).streams.filter(res=resolution, file_extension=format).first()

        # Download the selected stream
        if stream is not None:
            filename = stream.download()
            
            # If the desired format is mp3, convert it to audio with a minimum bitrate of 198kbps
            if format == "mp3":
                audio = stream.audio_only()
                audio_file = audio.download()
                command = f"ffmpeg -i {audio_file} -b:a 198k -vn audio.mp3"
                subprocess.call(command, shell=True)
                filename = "audio.mp3"
            
            # Send the downloaded file to the user
            with open(filename, "rb") as f:
                bot.send_document(message.chat.id, f)

            # Delete the downloaded file after sending
            os.remove(filename)

        else:
            bot.reply_to(message, "Invalid selection.")

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Start the bot
bot.polling()



