import asyncio
import i18n

from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot import TelegramBot
from utils import Message
from utils import is_float
from utils import get_coordinates
from utils import get_nearby_restaurants


class StartForm(StatesGroup):
    address = State()
    max_price = State()


async def _poll_price(message, data):
    address = data['address']
    max_price = data['max_price']
    coordinates = get_coordinates(data['address'])
    state = None
    # Poll two hours at max
    for _ in range(12):
        results = await get_nearby_restaurants(coordinates)
        state = TelegramBot.dp.current_state()
        data = await state.get_data()
        if not data['poll_price']:
            break
        if not results:
            await Message.answer(
                message, i18n['poll_failure'].format(
                    address=address
                ),
                escape_text=False, bot=TelegramBot.bot
            )
            break
        # TODO: Multiple restaurants info, new text when
        # some restaurant's delivery fee is below limit
        price = results[0]['deliveryFee']
        price_str = format(price, '.2f')
        if price < max_price:
            await Message.answer(
                message, i18n['poll_success'].format(
                    price_str=price_str
                ),
                bot=TelegramBot.bot
            )
            break
        await state.update_data(latest_price=price_str)
        await asyncio.sleep(60 * 10)
    await state.reset_state()


# @dp.message_handler(commands=['start'])
async def cmd_start(message):
    await StartForm.address.set()
    return await Message.reply(message, i18n['start'])


# @dp.message_handler(state=Form.address)
async def process_start_address(message, state):
    await state.update_data(address=message.text)
    await StartForm.next()
    return await Message.reply(message, i18n['process_address'])


# @dp.message_handler(lambda message: not is_float(message.text), state=Form.max_price)
async def process_max_price_invalid(message):
    return await Message.reply(message, i18n['process_max_price_invalid'])


# @dp.message_handler(lambda message: is_float(message.text), state=Form.max_price)
async def process_max_price(message, state):
    await state.update_data(
        max_price=float(message.text.replace(',', '.')),
        poll_interval=60 * 10,  # seconds
        poll_price=True,
        latest_price=None
    )
    await StartForm.next()
    async with state.proxy() as data:
        asyncio.create_task(_poll_price(message, data))
        price_str = str(data['max_price']).replace('.', '\\.')
        return await Message.answer(
            message, i18n['process_max_price'].format(
                price_str=price_str,
                address=data['address']
            ),
            escape_text=False
        )


def setup_start(dp):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(process_start_address, state=StartForm.address)
    dp.register_message_handler(
        process_max_price_invalid,
        lambda message: not is_float(message.text),
        state=StartForm.max_price
    )
    dp.register_message_handler(
        process_max_price,
        lambda message: is_float(message.text),
        state=StartForm.max_price
    )
