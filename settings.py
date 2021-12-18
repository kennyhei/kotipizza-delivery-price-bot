import os
from dotenv import load_dotenv

load_dotenv()

# Environment (development / production)
ENV = os.getenv('ENV', 'development')

# Webserver settings
WEBAPP_HOST = os.getenv('WEBAPP_HOST', 'localhost')
WEBAPP_PORT = int(os.getenv('WEBAPP_PORT', 5000))

# Webhook settings
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')
WEBHOOK_URL = f'{WEBAPP_HOST}{WEBHOOK_PATH}'

# Token
TOKEN = os.getenv('TOKEN')

# Bot mode ("polling" or "webhook")
MODE = os.getenv('MODE', 'polling')
