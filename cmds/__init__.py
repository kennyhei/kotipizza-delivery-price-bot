from cmds.notify import setup_notify
from cmds.poll import setup_poll
from cmds.price import setup_price
from cmds.help import setup_help
from cmds.stop import setup_stop
from cmds.echo import setup_echo


def setup_handlers(dp):
    setup_notify(dp)
    setup_poll(dp)
    setup_price(dp)
    setup_help(dp)
    setup_stop(dp)
    setup_echo(dp)
