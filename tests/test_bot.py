from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
from dotenv import load_dotenv

load_dotenv()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello, World!')

if __name__ == '__main__':
    application = Application.builder().token(os.environ.get('API_TOKEN')).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
