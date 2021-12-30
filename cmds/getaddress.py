import bot.i18n as i18n

from bot.bot import TelegramBot
from lib.utils import Message


async def cmd_getaddress(message):
    data = await TelegramBot.dp.current_state().get_data()
    address = data.get('address')
    if not address:
        return await Message.answer(message, i18n['address_missing'])
    return await Message.answer(
        message, i18n['get_address'].format(address=address),
        escape_text=False, bot=TelegramBot.bot
    )


def setup_getaddress(dp):
    dp.register_message_handler(cmd_getaddress, commands=['getaddress'])
