import asyncio
from splinter import Browser


'''
OBSOLETE, REPLACED BY api.py
'''


async def _fill_delivery_address(browser, address):
    """
    Phase 1:
    Fills user's delivery address in
    autocompletion form.
    """
    input_location_address = browser.find_by_id('address-autocomplete')
    if input_location_address.is_empty():
        print('Couldn\'t find address delivery form.')
        return False
    input_location_address = input_location_address.first
    input_location_address.fill(address)
    # Wait for Google Maps autocomplete form to appear
    await asyncio.sleep(5)
    return True


async def _click_outside_delivery_address_input(browser):
    """
    Phase 2:
    Clicks any element except the input we just filled,
    this activates the address search and lists closest
    restaurants.
    """
    el = browser.find_by_css('.primary').first  # some random element in the page
    el.click()
    # Wait for the page to search and display closest restaurants
    await asyncio.sleep(5)


def _parse_delivery_price(browser):
    """
    Phase 3:
    Parses delivery price from the page now that the
    delivery options should be loaded and displayed in the page.
    """
    div_price = browser.find_by_css('.sc-dkmKpi')
    if div_price.is_empty():
        return None
    div_price = div_price.first
    price = ' '.join(div_price.text.split())
    price = price.replace(',', '.').replace('€', '').strip()
    price = float(price)
    return price


async def fetch_delivery_price(address):
    url = 'https://www.kotipizza.fi/'
    browser = Browser('chrome', headless=True)
    browser.visit(url)
    # Wait that page is fully loaded as it's mostly
    # dynamically created using Javascript
    await asyncio.sleep(5)
    is_filled = await _fill_delivery_address(browser, address)
    if not is_filled:
        browser.quit()
    await _click_outside_delivery_address_input(browser)
    price = _parse_delivery_price(browser)
    browser.quit()
    return price
