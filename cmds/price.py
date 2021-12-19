import asyncio
import i18n

from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot import TelegramBot
from scraper import fetch_delivery_price
from utils import Message


class PriceForm(StatesGroup):
    address = State()


async def _get_price(message, address):
    result = await asyncio.gather(fetch_delivery_price(address))
    price = result[0]
    if not price:
        await Message.answer(
            message, i18n['poll_failure'].format(
                address=address
            ),
            escape_text=False, bot=TelegramBot.bot
        )
        return
    price_str = format(price, '.2f')
    return await Message.answer(
        message, i18n['latest_price'].format(price=price_str),
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
