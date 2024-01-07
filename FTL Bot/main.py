import os
from downloader import bot_downloader
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import logging

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

wait_gif = 'files\\wait.gif'
TOKEN = os.getenv('Token')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
Send a link of any of the following and you'll get your file:

1) Youtube video
2) Youtube Shorts
3) Instagram Reels
4) Pinterest Image
5) Pinterest Video
"""

    await context.bot.send_message(update.effective_chat.id,msg)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
This Bot was created on Jan 2024 and is currently under
Development By the Developer. \U0001F642

The Beta feature supports the following:

1) Youtube Video (10min or less)
2) Youtube Shorts
3) Instagram reels
4) Pinterest Videos
5) Pinterest Photos

Just send the link of any of the above and wait.
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wait_msg = await context.bot.send_animation(chat_id=update.effective_chat.id, animation=wait_gif, reply_to_message_id=update.message.id, caption='Please wait while i fetch your files')
    await handle_link(update, context)
    await context.bot.delete_message(update.effective_chat.id, wait_msg.message_id)

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    downloader = bot_downloader()

    try:
        if url.startswith('https://youtu'):
            path = downloader.Download_video_YT(url)
            await context.bot.send_video(chat_id=update.effective_chat.id, video=path, caption='Here is your Youtube video')
            await context.bot.send_document(chat_id=update.effective_chat.id, document=path, caption='Here is your Youtube video in docs just in case the aspect ratio is not good')
            os.remove(path)

        elif url.startswith('https://www.instagram.com/reel/'):
            path = downloader.Download_video_Insta(url)
            await context.bot.send_video(chat_id=update.effective_chat.id, video=path, caption='Here is your Instagram Reel')
            os.remove(path)

        elif url.startswith('https://pin'):
            path = downloader.Download_Pinterest(url)
            if path.endswith('.png'):
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=path, caption='Here is your Pinterest Pin')
            else:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=path, caption='Here is your Pinterest Video')
            os.remove(path)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,text='Sorry My developer is lazy he hasn\'t made me capable of chating yet, Please send a valid link only',reply_to_message_id=update.message.id)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()


    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_reel))

    application.run_polling()
