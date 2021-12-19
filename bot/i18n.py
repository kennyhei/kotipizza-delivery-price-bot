import settings
import sys

i18n = {
    'fi': {
        'notify': 'Hei siellä! Syötä katuosoitteesi ja kaupunkisi.',
        'poll': 'Kiitos! Ilmoitan sinulle 10 minuutin välein lähiravintoloidesi kuljetushinnat.',
        'process_address': 'Kiitos! Syötä vielä ylin sallittu hinta kuljetukselle (esim. 5,9 tai 5.9).',
        'process_max_price_invalid': 'Hinnan täytyy olla luku. Yritä uudestaan.',
        'process_max_price': (
            'Valmista\\! Ilmoitan sinulle heti, kun kuljetushinta on alle {price} € ' +
            'osoitteelle *{address}*\\.'
        ),
        'latest_price_invalid': 'En ole vielä hakenut kuljetushintaa. Yritä hetken päästä uudestaan.',
        'latest_price': 'Viimeisin kuljetushinta: {price} €',
        'stop': 'Kuljetushinnan haku lopetettu.',
        'poll_failure': 'En löytänyt kuljetushintoja osoitteelle *{address}*\\. Haku lopetettu\\.',
        'poll_success': 'Viimeisin kuljetushinta on {price} € ({estimate} min.). Aika tilata! 🍕 https://kotipizza.fi',
        'help': (
            'Hei! Olen Kotipizza Botti. Pystyn kertomaan sinulle lähialueesi ravintoloiden kuljetushinnat.\n\n'
            'Voit ohjata minua seuraavilla komennoilla:\n\n'
            '/start - Ilmoittaa 10 minuutin välein lähiravintoloiden kuljetushinnat\n' +
            '/notify - Ilmoittaa, kun lähiravintolan kuljetushinta on alle määritellyn maksimihinnan\n' +
            '/price - Ilmoittaa lähiravintoloiden viimeisimmät kuljetushinnat\n' +
            '/stop - Lopettaa kuljetushintojen haun\n'
        ),
        'restaurants_closed': 'Kaikki lähialueen ravintolat ovat suljettu. Kuljetushinnan haku lopetettu.'
    },
    'en': {
        'notify': 'Hi there! What\'s the delivery address?',
        'poll': 'Thanks! I\'ll notify you every 10 minutes the delivery prices of your nearby restaurants.',
        'process_address': 'OK! What\'s the maximum limit for the price of delivery? (e.g. "5.1" or "5,1")',
        'process_max_price_invalid': 'Price has to be a number. Try again.',
        'process_max_price': (
            'Alright\\! I\'ll notify you when the delivery price is below {price} € ' +
            'for address *{address}*\\.'
        ),
        'latest_price_invalid': 'I haven\'t fetched latest price yet. Try again later.',
        'latest_price': 'Latest delivery price: {price} €',
        'stop': 'Stopped fetching.',
        'poll_failure': 'Could not find delivery price with given address *{address}*\\. Stopped fetching\\.',
        'poll_success': 'Current delivery price is {price} € ({estimate} min.). Time to order! 🍕 https://kotipizza.fi',
        'help': (
            'Hi! I\'m Kotipizza Bot. I can tell you the delivery fees of your nearby restaurants.\n\n'
            'You can control me by sending these commands:\n\n'
            '/start - Notifies every 10 minutes the current delivery price\n' +
            '/notify - Notifies when delivery price is below the given limit\n' +
            '/price - Shows latest delivery price\n' +
            '/stop - Stops fetching delivery price'
        ),
        'restaurants_closed': 'All nearby restaurants are closed. Stopped fetching.'
    }
}[settings.LANGUAGE]

sys.modules[__name__] = i18n
