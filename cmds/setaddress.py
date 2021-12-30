from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from bot import i18n
from lib.api import get_coordinates
from lib.utils import Message


class Form(StatesGroup):
    address = State()


async def cmd_setaddress(message):
    await Form.address.set()
    return await Message.answer(message, i18n['set_address'])


async def process_setaddress_address_invalid(message, state):
    return await Message.answer(message, i18n['address_not_found'])


async def process_setaddress_address(message, state):
    address = message.text
    coordinates = get_coordinates(address)
    await state.update_data(
        address=address,
        coordinates=coordinates
    )
    await Form.next()
    return await Message.answer(
        message, i18n['thanks']
    )


def setup_setaddress(dp):
    dp.register_message_handler(cmd_setaddress, commands=['setaddress'])
    dp.register_message_handler(
        process_setaddress_address_invalid,
        lambda message: get_coordinates(message.text) is None,
        state=Form.address
    )
    dp.register_message_handler(
        process_setaddress_address,
        lambda message: get_coordinates(message.text) is not None,
        state=Form.address
    )
