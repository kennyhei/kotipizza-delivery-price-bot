import os
from dotenv import load_dotenv

load_dotenv()

# Environment (development / production)
ENV = os.getenv('ENV', 'development')

# Webserver settings
WEBAPP_HOST = os.getenv('WEBAPP_HOST', 'localhost')  # TODO: Try with ips 0.0.0.0 or 127.0.0.1 in production
WEBAPP_PORT = int(os.getenv('PORT', 5000))

# Webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', WEBAPP_HOST)
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# Token
TOKEN = os.getenv('TOKEN')

# Bot mode (polling / webhook)
MODE = os.getenv('MODE', 'polling')

# Bot language
LANGUAGE = os.getenv('LANGUAGE', 'fi')

# Geocoding API token
GOOGLE_MAPS_TOKEN = os.getenv('GOOGLE_MAPS_TOKEN')

# Restaurants API
RESTAURANTS_API_URL = os.getenv('RESTAURANTS_API_URL')
