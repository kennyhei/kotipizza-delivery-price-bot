import os
from dotenv import load_dotenv

load_dotenv()


class UserConfig:

    POLL_PRICE = False
    POLL_INTERVAL = 10 * 60
    DELIVERY_MAX_PRICE = -1
    DELIVERY_LATEST_PRICE = None
    DELIVERY_ADDRESS = None


class Settings:

    # User configs
    configs = {}

    # Webhook settings
    WEBHOOK_HOST = 'localhost'
    WEBHOOK_PATH = '/webhook'
    WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

    # Webserver settings
    WEBAPP_HOST = 'localhost'  # or ip
    WEBAPP_PORT = 5000

    # Token
    TOKEN = os.getenv('TOKEN')

    def get_config(self, user_id):
        if not self.configs.get(user_id):
            self.configs[user_id] = UserConfig()
        return self.configs.get(user_id)

    def remove_config(self, user_id):
        self.configs.pop(user_id, None)


settings = Settings()
