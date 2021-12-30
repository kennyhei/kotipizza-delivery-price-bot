import bot.i18n as i18n

from lib.utils import Message


async def cmd_help(message):
    return await Message.answer(message, i18n['help'])


def setup_help(dp):
    dp.register_message_handler(cmd_help, commands=['help'])
