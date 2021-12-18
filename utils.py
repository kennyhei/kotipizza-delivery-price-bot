import settings

from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.markdown import escape_md


class Message:

    @staticmethod
    async def answer(message, value, escape_text=True, bot=None):
        if escape_text:
            value = escape_md(value)
        if settings.MODE == 'polling':
            return await message.answer(value)
        if settings.MODE == 'webhook':
            if bot:
                return await bot.send_message(message.chat.id, value)
            return SendMessage(message.chat.id, value)

    @staticmethod
    async def reply(message, value, escape_text=True, bot=None):
        if escape_text:
            value = escape_md(value)
        if settings.MODE == 'polling':
            return await message.reply(value)
        if settings.MODE == 'webhook':
            if bot:
                return await bot.send_message(message.chat.id, value, reply_to_message_id=message.id)
            return SendMessage(message.chat.id, value, reply_to_message_id=message.id)


def is_float(value):
    value = value.replace(',', '.')
    try:
        float(value)
        return True
    except Exception:
        return False
