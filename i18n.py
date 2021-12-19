import settings
import sys

i18n = {
    'fi': {
        'start': 'Hei siellä! Syötä katuosoitteesi ja kaupunkisi.',
        'process_address': 'Kiitos! Syötä vielä ylin sallittu hinta kuljetukselle (esim. 5,9 tai 5.9).',
        'process_max_price_invalid': 'Hinnan täytyy olla luku. Yritä uudestaan.',
        'process_max_price': (
            'Valmista\\! Ilmoitan sinulle heti, kun kuljetushinta on alle {price_str} € ' +
            'osoitteelle *{address}*\\.'
        ),
        'latest_price_invalid': 'En ole vielä hakenut kuljetushintaa. Yritä hetken päästä uudestaan.',
        'latest_price': 'Viimeisin kuljetushinta: {price} €',
        'stop': 'Kuljetushinnan haku lopetettu.',
        'poll_failure': 'En löytänyt kuljetushintaa osoitteelle *{address}*\\. Haku lopetettu\\.',
        'poll_success': 'Viimeisin kuljetushinta on {price_str} €. Aika tilata! 🍕 https://kotipizza.fi',
        'help': (
            '/start - Ilmoittaa, kun kuljetushinta on alle määritellyn maksimihinnan\n' +
            '/poll - Ilmoittaa 10 minuutin välein viimeisimmän kuljetushinnan\n' +
            '/price - Näyttää viimeisimmän kuljetushinnan\n' +
            '/stop - Lopettaa kuljetushinnan haun\n'
        )
    },
    'en': {
        'start': 'Hi there! What\'s the delivery address?',
        'process_address': 'OK! What\'s the maximum limit for the price of delivery? (e.g. "5.1" or "5,1")',
        'process_max_price_invalid': 'Price has to be a number. Try again.',
        'process_max_price': (
            'Alright\\! I\'ll notify you when the delivery price is below {price_str} € ' +
            'for address *{address}*\\.'
        ),
        'latest_price_invalid': 'I haven\'t fetched latest price yet. Try again later.',
        'latest_price': 'Latest delivery price: {price} €',
        'stop': 'Stopped fetching',
        'poll_failure': 'Could not find delivery price with given address *{address}*\\. Stopped fetching\\.',
        'poll_success': 'Current delivery price is {price_str} €. Time to order! 🍕 https://kotipizza.fi',
        'help': (
            '/start - Notifies when delivery price is below the given limit\n' +
            '/poll - Notifies every 10 minutes the current delivery price\n' +
            '/price - Shows latest delivery price\n' +
            '/stop - Stops fetching delivery price'
        )
    }
}[settings.LANGUAGE]

sys.modules[__name__] = i18n
