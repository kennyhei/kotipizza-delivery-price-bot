import os
from dotenv import load_dotenv

load_dotenv()

# Webhook settings
WEBHOOK_HOST = 'localhost'
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# Webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 5000

# Token
TOKEN = os.getenv('TOKEN')
