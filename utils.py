import aiohttp
import googlemaps
import settings

from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.markdown import escape_md

from bot import TelegramBot


# https://developers.google.com/maps/documentation/geocoding/overview
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_TOKEN)


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
        price = format_price(restaurant['deliveryFee'])
        estimate = restaurant['currentDeliveryEstimate']
        is_closed = restaurant['openForDeliveryStatus'] == 'CLOSED'
        text += f'\n{idx + 1}. {name}'
        if is_closed:
            text += f'\n    - SULJETTU'
        else:
            text += f'({estimate} min.)'
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


def get_coordinates(address):
    # Geocoding an address
    results = gmaps.geocode(address, region='fi')
    if not results:
        return None
    location = results[0]['geometry']['location']
    return location['lat'], location['lng']


async def get_nearby_restaurants(coordinates):
    if not coordinates:
        return None
    session = TelegramBot.session
    if session is None:
        session = aiohttp.ClientSession(raise_for_status=True)
    lat, lng = coordinates
    params = {
        'type': 'DELIVERY',
        'coordinates': '{},{}'.format(lat, lng)
    }
    async with session.get(
        settings.RESTAURANTS_API_URL,
        params=params
    ) as resp:
        return await resp.json()
