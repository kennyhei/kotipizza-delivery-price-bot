import asyncio
import bot.i18n as i18n

from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot import TelegramBot
from lib.utils import Message
from lib.utils import build_restaurants_str
from lib.utils import delay
from lib.api import get_coordinates
from lib.api import get_nearby_restaurants


class Form(StatesGroup):
    address = State()


async def _poll_price(message, address):
    coordinates = get_coordinates(address)
    await delay(1, message)
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
        await Message.answer(
            message, build_restaurants_str(results),
            bot=TelegramBot.bot
        )
        # TODO: Latest restaurants info
        # await state.update_data(latest_price=price_str)
        await asyncio.sleep(60 * 10)
    await state.reset_state()


# @dp.message_handler(commands=['poll'])
async def cmd_poll(message):
    await Form.address.set()
    return await Message.reply(message, i18n['notify'])


# @dp.message_handler(state=Form.address)
async def process_address(message, state):
    await state.update_data(
        address=message.text,
        poll_price=True
    )
    await Form.next()
    async with state.proxy() as data:
        asyncio.create_task(_poll_price(message, data['address']))
        return await Message.answer(
            message, i18n['poll']
        )


def setup_poll(dp):
    dp.register_message_handler(cmd_poll, commands=['poll'])
    dp.register_message_handler(process_address, state=Form.address)
