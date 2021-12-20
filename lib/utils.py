import asyncio
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


def build_restaurants_str(restaurants):
    text = 'Ravintolat:\n'
    for idx, restaurant in enumerate(restaurants):
        name = restaurant['displayName']
        price = format_price(
            restaurant.get('dynamicDeliveryFee', restaurant['deliveryFee'])
        )
        estimate = restaurant['currentDeliveryEstimate']
        is_closed = restaurant['openForDeliveryStatus'] == 'CLOSED'
        text += f'\n{idx + 1}. {name}'
        if is_closed:
            text += f'\n    - SULJETTU'
        else:
            text += f' ({estimate} min.)'
            text += f'\n    - Kotiinkuljetus {price} €'
    return text


async def delay(seconds, message):
    await asyncio.sleep(seconds)
    await Message.answer(message, '...')
    await asyncio.sleep(seconds)


def format_price(value):
    return format(value, '.2f').replace('.', ',')


def is_float(value):
    value = value.replace(',', '.')
    try:
        float(value)
        return True
    except Exception:
        return False
