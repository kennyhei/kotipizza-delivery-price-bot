from cmds.getaddress import setup_getaddress
from cmds.notify import setup_notify
from cmds.poll import setup_poll
from cmds.price import setup_price
from cmds.help import setup_help
from cmds.setaddress import setup_setaddress
from cmds.start import setup_start
from cmds.stop import setup_stop
from cmds.echo import setup_echo


def setup_handlers(dp):
    setup_start(dp)
    setup_notify(dp)
    setup_poll(dp)
    setup_price(dp)
    setup_getaddress(dp)
    setup_setaddress(dp)
    setup_help(dp)
    setup_stop(dp)
    setup_echo(dp)
