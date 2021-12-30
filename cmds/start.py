from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

import bot.i18n as i18n

from lib.api import get_coordinates
from lib.utils import Message


class StartForm(StatesGroup):
    address = State()


async def cmd_start(message):
    await StartForm.address.set()
    await Message.answer(message, i18n['help'])
    await Message.delay(message, 1)
    return await Message.answer(message, i18n['start'])


async def process_start_address_invalid(message, state):
    return await Message.answer(message, i18n['address_not_found'])


async def process_start_address(message, state):
    address = message.text
    await Message.delay(message, 0)
    coordinates = get_coordinates(address)
    await state.update_data(
        address=address,
        coordinates=coordinates
    )
    await StartForm.next()
    return await Message.answer(
        message, i18n['process_address']
    )


def setup_start(dp):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(
        process_start_address_invalid,
        lambda message: get_coordinates(message.text) is None,
        state=StartForm.address
    )
    dp.register_message_handler(
        process_start_address,
        lambda message: get_coordinates(message.text) is not None,
        state=StartForm.address
    )
