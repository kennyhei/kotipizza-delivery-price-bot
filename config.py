class UserConfig:

    POLL_PRICE = False
    POLL_INTERVAL = 10 * 60
    DELIVERY_MAX_PRICE = -1
    DELIVERY_LATEST_PRICE = None
    DELIVERY_ADDRESS = None


class Settings:

    configs = {}

    def get_config(self, user_id):
        if not self.configs.get(user_id):
            self.configs[user_id] = UserConfig()
        return self.configs.get(user_id)

    def remove_config(self, user_id):
        self.configs.pop(user_id, None)


settings = Settings()
