import asyncio

from config import settings
from scraper import fetch_delivery_price


async def poll_price(message, conf):
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
                'Stopped polling.'
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
