import asyncio
import settings

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.utils import executor
from aiogram.types.message import ParseMode

from scraper import fetch_delivery_price


# Initialize bot and dispatcher
bot = Bot(settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States for "start" command
class Form(StatesGroup):
    address = State()
    max_price = State()


def _is_float(value):
    value = value.replace(',', '.')
    try:
        float(value)
        return True
    except Exception:
        return False


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
            await message.answer(
                f'Could not find delivery price with given address *{address}*. '
                f'Stopped fetching.',
                parse_mode=ParseMode.MARKDOWN
            )
            break
        price_str = format(price, '.2f')
        if price < max_price:
            await message.answer(
                f'Current delivery price is {price_str} €. '
                f'Time to order! 🍕 https://kotipizza.fi'
            )
            break
        await state.update_data(latest_price=price_str)
        await asyncio.sleep(60 * 10)
    await state.reset_state()


@dp.message_handler(commands=['start'])
async def cmd_start(message):
    await Form.address.set()
    await message.reply('Hi there! What\'s the delivery address?')


@dp.message_handler(state=Form.address)
async def process_address(message, state):
    await state.update_data(address=message.text)
    await Form.next()
    await message.reply('OK! What\'s the maximum limit for the price of delivery? (e.g. "5.1" or "5,1")')


@dp.message_handler(lambda message: not _is_float(message.text), state=Form.max_price)
async def process_max_price_invalid(message):
    return await message.reply('Price has to be a number. Try again.')


@dp.message_handler(lambda message: _is_float(message.text), state=Form.max_price)
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
        await message.answer(
            f'Alright! I\'ll notify you when the delivery price is below {data["max_price"]} € '
            f'for address *{data["address"]}*.',
            parse_mode=ParseMode.MARKDOWN
        )


@dp.message_handler(commands=['showlatestprice'])
async def cmd_latest_price(message):
    data = await dp.current_state().get_data()
    price = data['latest_price']
    if not price:
        await message.answer('I haven\'t fetched latest price yet. Try again later.')
    else:
        await message.answer(f'Latest delivery price: {price} €')


@dp.message_handler(commands=['stop'])
async def cmd_stop(message):
    await dp.current_state().update_data(poll_price=False)
    await message.answer('Stopped fetching.')


@dp.message_handler(commands=['help'])
async def cmd_help(message):
    await message.answer(
        f'/start - Fetches every 10 minutes the current delivery price\n'
        f'/stop - Stops fetching delivery price\n'
        f'/showlatestprice - Shows latest delivery price'
    )


async def on_startup(dp):
    await bot.set_webhook(settings.WEBHOOK_URL)


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()


'''
NOTE: With webhook, you should call SendMessage function
instead of message.answer

executor.start_webhook(
    dispatcher=dp,
    webhook_path=settings.WEBHOOK_PATH,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host=settings.WEBAPP_HOST,
    port=settings.WEBAPP_PORT
)
'''
executor.start_polling(dp, skip_updates=True)
