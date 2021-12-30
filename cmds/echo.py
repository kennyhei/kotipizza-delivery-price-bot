

async def cmd_echo(message):
    print(message)


def setup_echo(dp):
    dp.register_message_handler(cmd_echo)
