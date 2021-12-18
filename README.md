## Setup

Steps:

1. `brew install geckodriver`
2. `brew install chromedriver`
3. `cd /usr/local/Caskroom/chromedriver`
4. `xattr -d com.apple.quarantine chromedriver`
5. `python -m venv venv`
6. `source venv/bin/activate`
7. `pip install -r requirements.txt`

Run `python bot.py`

## Modes

#### Polling

Enable infinite polling by adding `MODE=polling` to your `.env` file.

This way you can test commands directly by typing them to Telegram Bot in the chat.

#### Webhook

Enable webhook mode by adding `MODE=webhook` to your `.env` file.

You can check that the Webhook API works by sending `update` request as JSON to the webhook path (check update examples section from [here](https://core.telegram.org/bots/webhooks)). By default webhook path is set as `http://localhost:5000/webhook` in `settings.py`.

Example request:

```
POST http://localhost:5000/webhook
Content-Type: application/json

{
    "update_id": 10000,
    "message": {
        "chat": {
            "id": 1111111,
            "type": "private"
        },
        "message_id": 1365,
        "from": {
            "id": 1111111,
            "is_bot": false,
            "first_name": "Test",
            "username": "Test",
        },
        "text": "/help"
    }
}
```

Aiogram should return HTTP 200 with JSON body that has the bot's answer in it:

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 240

{
  "method": "sendMessage",
  "chat_id": 1111111,
  "text": "/start \\- Fetches every 10 minutes the current delivery price\n/stop \\- Stops fetching delivery price\n/showlatestprice \\- Shows latest delivery price",
  "parse_mode": "markdownv2"
}
```
