import asyncio
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.types.message import ParseMode
from dotenv import load_dotenv

from config import settings
from poll import poll_price


load_dotenv()

TOKEN = os.getenv('TOKEN')
# Initialize bot and dispatcher
bot = Bot(TOKEN)
dp = Dispatcher(bot)


def get_config(message):
    return settings.get_config(message['from']['id'])


def extract_args(args):
    return args.split()[1:]


@dp.message_handler(commands=['start'])
async def cmd_start(message):
    conf = get_config(message)
    conf.POLL_PRICE = True
    address = ' '.join(extract_args(message.text))
    conf.DELIVERY_ADDRESS = address
    if address:
        await message.answer('OK. Next set the maximum limit for the price of delivery (e.g. "5.1" or "5,1").')
    else:
        await message.answer('Please give a delivery address.')


@dp.message_handler(commands=['showlatestprice'])
async def cmd_latest_price(message):
    conf = get_config(message)
    price = conf.DELIVERY_LATEST_PRICE
    if not price:
        await message.answer('I haven\'t fetched latest price yet. Try again later.')
    else:
        await message.answer(f'Latest delivery price: {price} €')


@dp.message_handler(commands=['stop'])
async def cmd_stop(message):
    settings.remove_config(message['from']['id'])
    await message.answer('Stopped polling.')


@dp.message_handler(commands=['help'])
async def cmd_help(message):
    await message.answer(
        f'/start - Fetches every 10 minutes the current delivery price\n'
        f'/stop - Stops fetching delivery price\n'
        f'/showlatestprice - Shows latest delivery price'
    )


async def _handle_address(message, conf):
    address = message.text
    if not address:
        await message.answer('You did not give an address. Try again.')
        return
    conf.DELIVERY_ADDRESS = address
    await message.answer('OK. Next set the maximum allowed price for the delivery (e.g. "5.1" or "5,1").')


async def _handle_max_price(message, conf):
    try:
        text = message.text.replace(',', '.').strip()
        max_price = float(text)
        address = conf.DELIVERY_ADDRESS
        conf.DELIVERY_MAX_PRICE = max_price
        asyncio.create_task(poll_price(message, conf))
        await message.answer(
            f'Alright! I\'ll notify you when the delivery price is below {max_price} € '
            f'for address *{address}*.',
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        await message.answer('Could not parse max price from answer. Try again.')


@dp.message_handler()
async def echo(message):
    conf = get_config(message)
    if not conf.DELIVERY_ADDRESS:
        await _handle_address(message, conf)
    elif conf.DELIVERY_MAX_PRICE < 0:
        await _handle_max_price(message, conf)


executor.start_polling(dp, skip_updates=True)
