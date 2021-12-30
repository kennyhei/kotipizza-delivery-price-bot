import asyncio
import bot.i18n as i18n

from bot.bot import TelegramBot
from lib.api import get_nearby_restaurants
from lib.utils import Message
from lib.utils import build_restaurants_str


async def _poll_price(message, address, coordinates):
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
        await Message.answer(
            message, build_restaurants_str(address, results)
        )
        await asyncio.sleep(60 * 10)
    await state.reset_state()


async def cmd_poll(message):
    state = TelegramBot.dp.current_state()
    data = await state.get_data()
    if not data.get('address') or not data.get('coordinates'):
        return await Message.reply(message, i18n['address_missing'])
    await state.update_data(
        poll_price=True
    )
    asyncio.create_task(_poll_price(message, data['address'], data['coordinates']))
    return await Message.answer(
        message, i18n['poll'].format(address=data['address']),
        escape_text=False, bot=TelegramBot.bot
    )


def setup_poll(dp):
    dp.register_message_handler(cmd_poll, commands=['poll'])
