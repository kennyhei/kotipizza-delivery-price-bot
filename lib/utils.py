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

    @staticmethod
    async def delay(message, seconds):
        await asyncio.sleep(seconds)
        await Message.answer(message, '...')
        await asyncio.sleep(seconds)


def build_restaurants_str(address, restaurants):
    text = f'Kuljetusosoite:\n{address}\n\n'
    text += 'Ravintolat:\n'
    for idx, restaurant in enumerate(restaurants):
        name = restaurant['displayName']
        price = format_price(
            restaurant.get('dynamicDeliveryFee', restaurant['deliveryFee'])
        )
        estimate = restaurant['currentDeliveryEstimate']
        delivery_status = restaurant['openForDeliveryStatus']
        text += f'\n{idx + 1}. {name}'
        if delivery_status in ['CLOSED', 'TEMPORARILY_UNAVAILABLE']:
            text += {
                'CLOSED': f'\n    - SULJETTU',
                'TEMPORARILY_UNAVAILABLE': f'\n    - VÄLIAIKAISESTI SULJETTU'
            }.get(delivery_status, '')
        else:
            text += f' ({estimate} min.)'
            text += f'\n    - Kotiinkuljetus {price} €'
    return text


def format_price(value):
    return format(value, '.2f').replace('.', ',')


def is_float(value):
    value = value.replace(',', '.')
    try:
        float(value)
        return True
    except Exception:
        return False
