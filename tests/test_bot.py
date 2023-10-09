from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
from dotenv import load_dotenv
import logging

load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')

if not API_TOKEN:
    raise EnvironmentError("API_TOKEN is not set in the environment variables.")

# 设置日志格式和级别
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello, World!')
    logger.info(f"Sent message to {update.effective_user['first_name']}")


async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "这里是帮助信息：\n"
        "/start - 启动机器人\n"
        "/github - 查看GitHub项目链接"
        # "/weather - 查询深圳天气"  # Uncomment this when you implement the weather command
    )

async def github_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "GitHub项目链接：\n"
        "https://github.com/ztm0929/TGBot"
    )

if __name__ == '__main__':
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('github', github_command))

    application.run_polling()