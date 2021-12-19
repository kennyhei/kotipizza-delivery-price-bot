import asyncio
import i18n

from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot import TelegramBot
from utils import Message
from utils import format_price
from utils import is_float
from utils import get_coordinates
from utils import get_nearby_restaurants


class StartForm(StatesGroup):
    address = State()
    max_price = State()


async def _poll_price(message, data):
    asyncio.sleep(1)
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
        # Stop looping if all nearby restaurants are closed
        if all(x['openForDeliveryStatus'] == 'CLOSED' for x in results):
            await Message.answer(
                message, i18n['restaurants_closed'],
                bot=TelegramBot.bot
            )
            break
        found_restaurant = False
        for restaurant in results:
            if (
                restaurant['openForDeliveryStatus'] != 'CLOSED' and
                restaurant['deliveryFee'] < max_price
            ):
                found_restaurant = True
                price = format_price(restaurant['deliveryFee'])
                await Message.answer(
                    message, i18n['poll_success'].format(
                        price=price,
                        estimate=restaurant['currentDeliveryEstimate']
                    ),
                    bot=TelegramBot.bot
                )
                break
        # Stop looping if we found restaurant with acceptable delivery fee
        if found_restaurant:
            break
        # TODO: Put restaurants dict in memory (latest_restaurants_info or something like that)
        # await state.update_data(latest_price=price_str)
        await asyncio.sleep(60 * 10)
    await state.reset_state()


# @dp.message_handler(commands=['notify'])
async def cmd_notify(message):
    await StartForm.address.set()
    return await Message.reply(message, i18n['notify'])


# @dp.message_handler(state=Form.address)
async def process_notify_address(message, state):
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
        price = format_price(data['max_price'])
        return await Message.answer(
            message, i18n['process_max_price'].format(
                price=price,
                address=data['address']
            ),
            escape_text=False
        )


def setup_notify(dp):
    dp.register_message_handler(cmd_notify, commands=['notify'])
    dp.register_message_handler(process_notify_address, state=StartForm.address)
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
