import asyncio
import logging
import settings

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils import executor
from aiogram.types.message import ParseMode

from scraper import fetch_delivery_price
from utils import Message
from utils import is_float

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(settings.TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States for "start" command
class Form(StatesGroup):
    address = State()
    max_price = State()


async def _poll_price(message, data):
    address = data['address']
    max_price = data['max_price']
    state = None
    # Poll two hours at max
    for _ in range(20):
        result = await asyncio.gather(fetch_delivery_price(address))
        state = dp.current_state()
        data = await state.get_data()
        if not data['poll_price']:
            break
        price = result[0]
        if not price:
            await Message.answer(
                message,
                f'Could not find delivery price with given address *{address}*. '
                f'Stopped fetching.',
                escape_text=False, bot=bot
            )
            break
        price_str = format(price, '.2f')
        if price < max_price:
            await Message.answer(
                message,
                f'Current delivery price is {price_str} €. '
                f'Time to order! 🍕 https://kotipizza.fi',
                bot=bot
            )
            break
        await state.update_data(latest_price=price_str)
        await asyncio.sleep(60 * 10)
    await state.reset_state()


@dp.message_handler(commands=['start'])
async def cmd_start(message):
    await Form.address.set()
    return await Message.reply(message, 'Hi there! What\'s the delivery address?')


@dp.message_handler(state=Form.address)
async def process_address(message, state):
    await state.update_data(address=message.text)
    await Form.next()
    return await Message.reply(
        message,
        'OK! What\'s the maximum limit for the price of delivery? (e.g. "5.1" or "5,1")'
    )


@dp.message_handler(lambda message: not is_float(message.text), state=Form.max_price)
async def process_max_price_invalid(message):
    return await Message.reply(message, 'Price has to be a number. Try again.')


@dp.message_handler(lambda message: is_float(message.text), state=Form.max_price)
async def process_max_price(message, state):
    await state.update_data(
        max_price=float(message.text.replace(',', '.')),
        poll_interval=60 * 10,  # seconds
        poll_price=True,
        latest_price=None
    )
    await Form.next()
    async with state.proxy() as data:
        asyncio.create_task(_poll_price(message, data))
        price_str = str(data['max_price']).replace('.', '\\.')
        return await Message.answer(
            message,
            f'Alright\\! I\'ll notify you when the delivery price is below {price_str} € '
            f'for address *{data["address"]}*\\.',
            escape_text=False
        )


@dp.message_handler(commands=['showlatestprice'])
async def cmd_latest_price(message):
    data = await dp.current_state().get_data()
    price = data.get('latest_price')
    if not price:
        return await Message.answer(message, 'I haven\'t fetched latest price yet. Try again later.')
    else:
        return await Message.answer(message, f'Latest delivery price: {price} €')


@dp.message_handler(commands=['stop'])
async def cmd_stop(message):
    await dp.current_state().update_data(poll_price=False)
    return await Message.answer(message, 'Stopped fetching.')


@dp.message_handler(commands=['help'])
async def cmd_help(message):
    return await Message.answer(
        message,
        f'/start - Fetches every 10 minutes the current delivery price\n'
        f'/stop - Stops fetching delivery price\n'
        f'/showlatestprice - Shows latest delivery price'
    )


@dp.message_handler()
async def echo(message):
    print(message)


async def on_startup(dp):
    pass
    # await bot.set_webhook(settings.WEBHOOK_URL)


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()


def run():
    if settings.MODE == 'webhook':
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=settings.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=settings.WEBAPP_HOST,
            port=settings.WEBAPP_PORT
        )
    if settings.MODE == 'polling':
        executor.start_polling(dp, skip_updates=True)


run()
