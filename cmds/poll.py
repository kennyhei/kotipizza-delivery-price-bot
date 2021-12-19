import asyncio
import i18n

from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot import TelegramBot
from scraper import fetch_delivery_price
from utils import Message


class Form(StatesGroup):
    address = State()


async def _poll_price(message, address):
    state = None
    # Poll one hour at max
    for _ in range(6):
        result = await asyncio.gather(fetch_delivery_price(address))
        state = TelegramBot.dp.current_state()
        data = await state.get_data()
        if not data['poll_price']:
            break
        price = result[0]
        if not price:
            await Message.answer(
                message, i18n['poll_failure'].format(
                    address=address
                ),
                escape_text=False, bot=TelegramBot.bot
            )
            break
        price_str = format(price, '.2f')
        await Message.answer(
            message, i18n['latest_price'].format(price=price_str),
            bot=TelegramBot.bot
        )
        await state.update_data(latest_price=price_str)
        await asyncio.sleep(60 * 10)
    await state.reset_state()


# @dp.message_handler(commands=['poll'])
async def cmd_poll(message):
    await Form.address.set()
    return await Message.reply(message, i18n['start'])


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
            message, 'Haetaan...'
        )


def setup_poll(dp):
    dp.register_message_handler(cmd_poll, commands=['poll'])
    dp.register_message_handler(process_address, state=Form.address)
