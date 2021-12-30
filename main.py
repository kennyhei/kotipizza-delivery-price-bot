import logging
import settings

from aiogram.utils import executor
from bot.bot import TelegramBot


def main():
    logging.basicConfig(level=logging.INFO)
    if settings.MODE == 'webhook':
        executor.start_webhook(
            dispatcher=TelegramBot.dp,
            webhook_path=settings.WEBHOOK_PATH,
            on_startup=TelegramBot.on_startup,
            on_shutdown=TelegramBot.on_shutdown,
            skip_updates=True,
            host=settings.WEBAPP_HOST,
            port=settings.WEBAPP_PORT
        )
    if settings.MODE == 'polling':
        executor.start_polling(
            dispatcher=TelegramBot.dp,
            on_startup=TelegramBot.on_startup,
            skip_updates=True
        )


main()
