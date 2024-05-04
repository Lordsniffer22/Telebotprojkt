import asyncio
import logging
import sys
import os
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from pytube import YouTube
from aiogram import types

from aiogram.types import Message

# Bot token can be obtained via https:/Command/t.me/BotFather
#TOKEN = getenv("API_TOKEN")
TOKEN = '7139989240:AAEtHvE6aNfY2Nsjh7ufl-vtxJroGVLFoUo'

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message()
async def All_commands(message: Message) -> None:
    """
    This handler receives text messages and checks if they contain a YouTube link
    """
    text = message.text.strip()
    if text.startswith('https://www.youtube.com/') or text.startswith('https://youtu.be/'):
        try:
            # Download the video
            yt = YouTube(text)
            video_title = yt.title
            stream = yt.streams.filter(only_audio=True).first()
            if stream:
                file_path = stream.download()
                mp3_file = f"{video_title}.mp3"
                os.rename(file_path, mp3_file)
                return mp3_file
            else:
                return None

            # Send the MP3 audio file back to the user
            with open(mp3_file, 'rb') as h:
                caption = "Hey your music is here.\n\n➤Bot: @tubyDoo_Bot \n│\n╰┈➤Join @udpcustom"
                await message.answer(h, caption)
            os.remove(mp3_file)  # Remove the MP3 file after sending

        except Exception as e:
            await message.answer(f"An error occurred: {e}")
    if message.text.startswith('/help'):
        help_message = """
        Here are the available commands:
        /start - Start the bot
        /help - Display this help message
        """
        await message.answer(help_message)
    elif message.text == 'olwa':
        fik = """
        I loved you too much yesterday
        """
        await message.answer(fik)



async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And then run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
