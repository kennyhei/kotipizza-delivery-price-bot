

# @dp.message_handler(commands=['stop'])
async def cmd_echo(message):
    print(message)
    message.text = 'jee'
    print(message)


def setup_echo(dp):
    dp.register_message_handler(cmd_echo)