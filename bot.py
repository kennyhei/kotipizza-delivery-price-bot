import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.types.message import ParseMode

from config import settings
from scraper import fetch_delivery_price


# Initialize bot and dispatcher
bot = Bot(settings.TOKEN)
dp = Dispatcher(bot)


def _get_config(message):
    return settings.get_config(message['from']['id'])


async def _poll_price(message, conf):
    address = conf.DELIVERY_ADDRESS
    max_price = conf.DELIVERY_MAX_PRICE
    for _ in range(1000):
        result = await asyncio.gather(fetch_delivery_price(address))
        if not conf.POLL_PRICE:
            break
        price = result[0]
        if not price:
            await message.answer(
                f'Could not find delivery price with given address *{address}*. '
                'Stopped fetching.'
            )
            break
        price_str = format(price, '.2f')
        if price < max_price:
            await message.answer(
                f'Current delivery price is {price_str} €. '
                f'Time to order! 🍕 https://kotipizza.fi'
            )
            break
        conf.DELIVERY_LATEST_PRICE = price_str
        await asyncio.sleep(conf.POLL_INTERVAL)
    settings.remove_config(conf)


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
        asyncio.create_task(_poll_price(message, conf))
        await message.answer(
            f'Alright! I\'ll notify you when the delivery price is below {max_price} € '
            f'for address *{address}*.',
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        await message.answer('Could not parse max price from answer. Try again.')


@dp.message_handler(commands=['start'])
async def cmd_start(message):
    conf = _get_config(message)
    conf.POLL_PRICE = True
    address = ' '.join(message.text.split()[1:])
    conf.DELIVERY_ADDRESS = address
    if address:
        await message.answer('OK. Next set the maximum limit for the price of delivery (e.g. "5.1" or "5,1").')
    else:
        await message.answer('Please give a delivery address.')


@dp.message_handler(commands=['showlatestprice'])
async def cmd_latest_price(message):
    conf = _get_config(message)
    price = conf.DELIVERY_LATEST_PRICE
    if not price:
        await message.answer('I haven\'t fetched latest price yet. Try again later.')
    else:
        await message.answer(f'Latest delivery price: {price} €')


@dp.message_handler(commands=['stop'])
async def cmd_stop(message):
    settings.remove_config(message['from']['id'])
    await message.answer('Stopped fetching.')


@dp.message_handler(commands=['help'])
async def cmd_help(message):
    await message.answer(
        f'/start - Fetches every 10 minutes the current delivery price\n'
        f'/stop - Stops fetching delivery price\n'
        f'/showlatestprice - Shows latest delivery price'
    )


@dp.message_handler()
async def echo(message):
    conf = _get_config(message)
    if not conf.DELIVERY_ADDRESS:
        await _handle_address(message, conf)
    elif conf.DELIVERY_MAX_PRICE < 0:
        await _handle_max_price(message, conf)


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
