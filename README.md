## Setup

Steps:

1. `brew install chromedriver`
2. `cd /usr/local/Caskroom/chromedriver`
3. `xattr -d com.apple.quarantine chromedriver`
4. `python -m venv venv`
5. `source venv/bin/activate`
6. `pip install -r requirements.txt`

Run `python bot.py`

## Modes

#### Polling

Enable infinite polling by adding `MODE=polling` to your `.env` file.

This way you can test commands directly by typing them to Telegram Bot in the chat.

#### Webhook

Enable webhook mode by adding `MODE=webhook` to your `.env` file.

You can check that the Webhook API works by sending `update` request as JSON to the webhook path (check update examples section from [here](https://core.telegram.org/bots/webhooks)). By default webhook path is set as `http://localhost:5000/webhook` in `settings.py`.

Example request:

```javascript
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

```javascript
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

## TODO

- New command(s):
    - `/setaddress` - User can set address so that bot doesn't need to ask it again in /start, /poll and /price commands
    - `/setprice` - User can set maximum price for the delivery
    - `/config` - Show set address and max price
    - NOTE: These are helpful only if user info is not cleared from memory after (any) command has been executed
- Don't ask address again in `/start`, `/poll` etc. if it's found in the memory