import os
from dotenv import load_dotenv

load_dotenv()

# Webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 5000

# Webhook settings
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f'{WEBAPP_HOST}{WEBHOOK_PATH}'

# Token
TOKEN = os.getenv('TOKEN')

# Bot mode ("polling" or "webhook")
MODE = os.getenv('MODE', 'polling')
