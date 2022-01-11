import aiohttp
import settings

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.types.message import ParseMode


class TelegramBot:

    # Initialize bot and dispatcher
    bot = Bot(settings.TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
    storage = JSONStorage('./data.json')
    dp = Dispatcher(bot, storage=storage)
    # AIOHttp client session
    session = None

    @classmethod
    async def on_startup(cls, dp):
        from cmds import setup_handlers
        if settings.ENV == 'production' and settings.MODE == 'webhook':
            await TelegramBot.bot.set_webhook(settings.WEBHOOK_URL)
        TelegramBot.session = aiohttp.ClientSession(raise_for_status=True)
        setup_handlers(dp)

    @classmethod
    async def on_shutdown(cls, dp):
        # Remove webhook (not acceptable in some cases)
        await TelegramBot.bot.delete_webhook()
        await TelegramBot.session.close()
