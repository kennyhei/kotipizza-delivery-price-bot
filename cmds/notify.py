import asyncio
import bot.i18n as i18n

from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot.bot import TelegramBot
from lib.utils import Message
from lib.utils import format_price
from lib.utils import is_float
from lib.api import get_nearby_restaurants


class StartForm(StatesGroup):
    max_price = State()


async def _poll_price(message, data):
    address = data['address']
    max_price = data['max_price']
    coordinates = data['coordinates']
    await Message.delay(message, 1)
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
        if all(x['openForDeliveryStatus'] in ['CLOSED', 'TEMPORARILY_UNAVAILABLE'] for x in results):
            await Message.answer(
                message, i18n['restaurants_closed'],
                bot=TelegramBot.bot
            )
            break
        found_restaurant = False
        for restaurant in results:
            price = restaurant.get('dynamicDeliveryFee', restaurant['deliveryFee'])
            if (
                restaurant['openForDeliveryStatus'] != 'CLOSED' and
                price < max_price
            ):
                found_restaurant = True
                price = format_price(price)
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
        await asyncio.sleep(60 * 10)
    await state.update_data(poll_price=False)


async def cmd_notify(message):
    data = await TelegramBot.dp.current_state().get_data()
    if not data.get('address') or not data.get('coordinates'):
        return await Message.reply(message, i18n['address_missing'])
    await StartForm.max_price.set()
    return await Message.reply(message, i18n['set_max_price'])


async def process_max_price_invalid(message):
    return await Message.reply(message, i18n['process_max_price_invalid'])


async def process_max_price(message, state):
    await state.update_data(
        max_price=float(message.text.replace(',', '.')),
        poll_price=True
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
