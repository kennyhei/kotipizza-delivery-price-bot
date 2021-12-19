import aiohttp
import googlemaps
import settings

from bot import TelegramBot


# https://developers.google.com/maps/documentation/geocoding/overview
gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_TOKEN)


def get_coordinates(address):
    # Geocoding an address
    results = gmaps.geocode(address, region='fi')
    if not results:
        return None
    location = results[0]['geometry']['location']
    return location['lat'], location['lng']


async def get_nearby_restaurants(coordinates):
    if not coordinates:
        return None
    session = TelegramBot.session
    if session is None:
        session = aiohttp.ClientSession(raise_for_status=True)
    lat, lng = coordinates
    params = {
        'type': 'DELIVERY',
        'coordinates': '{},{}'.format(lat, lng)
    }
    async with session.get(
        settings.RESTAURANTS_API_URL,
        params=params
    ) as resp:
        return await resp.json()
