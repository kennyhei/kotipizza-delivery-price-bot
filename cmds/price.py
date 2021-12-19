import asyncio
import i18n

from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot import TelegramBot
from utils import Message
from utils import build_restaurants_str
from utils import get_coordinates
from utils import get_nearby_restaurants


class PriceForm(StatesGroup):
    address = State()


async def _get_price(message, address):
    coordinates = get_coordinates(address)
    results = await get_nearby_restaurants(coordinates)
    if not results:
        return await Message.answer(
            message, i18n['poll_failure'].format(
                address=address
            ),
            escape_text=False, bot=TelegramBot.bot
        )
    return await Message.answer(
        message, build_restaurants_str(results),
        bot=TelegramBot.bot
    )


# @dp.message_handler(commands=['poll'])
async def cmd_price(message):
    data = await TelegramBot.dp.current_state().get_data()
    await PriceForm.address.set()
    if data.get('address'):
        message.text = data['address']
        state = TelegramBot.dp.current_state()
        return await process_address(message, state)
    return await Message.reply(message, i18n['start'])


# @dp.message_handler(state=Form.address)
async def process_address(message, state):
    await state.update_data(address=message.text)
    await PriceForm.next()
    async with state.proxy() as data:
        asyncio.create_task(_get_price(message, data['address']))
        return await Message.answer(
            message, 'Haetaan...'
        )


def setup_price(dp):
    dp.register_message_handler(cmd_price, commands=['price'])
    dp.register_message_handler(process_address, state=PriceForm.address)
