import aiohttp
import logging
import settings

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types.message import ParseMode


class TelegramBot:

    # Initialize bot and dispatcher
    bot = Bot(settings.TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    # AIOHttp client session
    session = None


async def on_startup(dp):
    from cmds import setup_handlers
    if settings.ENV == 'production':
        await TelegramBot.bot.set_webhook(settings.WEBHOOK_URL)
    TelegramBot.session = aiohttp.ClientSession(raise_for_status=True)
    setup_handlers(dp)


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    await TelegramBot.bot.delete_webhook()
    await TelegramBot.session.close()


def main():
    logging.basicConfig(level=logging.INFO)
    if settings.MODE == 'webhook':
        executor.start_webhook(
            dispatcher=TelegramBot.dp,
            webhook_path=settings.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=settings.WEBAPP_HOST,
            port=settings.WEBAPP_PORT
        )
    if settings.MODE == 'polling':
        executor.start_polling(TelegramBot.dp, on_startup=on_startup, skip_updates=True)
