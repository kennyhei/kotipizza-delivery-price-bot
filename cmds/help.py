import i18n

from utils import Message


# @dp.message_handler(commands=['stop'])
async def cmd_help(message):
    return await Message.answer(message, i18n['help'])


def setup_help(dp):
    dp.register_message_handler(cmd_help, commands=['help'])