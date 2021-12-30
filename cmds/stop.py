import bot.i18n as i18n

from bot.bot import TelegramBot
from lib.utils import Message


async def cmd_stop(message):
    await TelegramBot.dp.current_state().update_data(poll_price=False)
    return await Message.answer(message, i18n['stop'])


def setup_stop(dp):
    dp.register_message_handler(cmd_stop, commands=['stop'])
