import asyncio
import bot.i18n as i18n

from bot.bot import TelegramBot
from lib.utils import Message
from lib.utils import build_restaurants_str
from lib.api import get_nearby_restaurants


async def _get_price(message, address, coordinates):
    results = await get_nearby_restaurants(coordinates)
    await asyncio.sleep(1)
    if not results:
        return await Message.answer(
            message, i18n['poll_failure'].format(
                address=address
            ),
            escape_text=False, bot=TelegramBot.bot
        )
    return await Message.answer(
        message, build_restaurants_str(address, results)
    )


async def cmd_price(message):
    data = await TelegramBot.dp.current_state().get_data()
    if not data.get('address') or not data.get('coordinates'):
        return await Message.reply(message, i18n['address_missing'])
    asyncio.create_task(_get_price(message, data['address'], data['coordinates']))
    return await Message.answer(
        message, 'Haetaan...'
    )


def setup_price(dp):
    dp.register_message_handler(cmd_price, commands=['price'])
