import settings
import sys

i18n = {
    'fi': {
        'poll': (
            'Selvä\\! Ilmoitan sinulle 10 minuutin välein lähiravintoloidesi dynaamiset ' +
            'kuljetushinnat osoitteelle *{address}*\\.'
        ),
        'get_address': 'Asettamasi kuljetusosoite on *{address}*\\.',
        'set_address': 'Syötä katuosoitteesi ja kaupunkisi.',
        'set_max_price': 'Syötä ylin sallittu hinta kuljetukselle (esim. 5,9 tai 5.9).',
        'process_address': (
            'Kiitos! Kokeile hakea lähiravintoloidesi kuljetushinnat komennolla /price. ' +
            'Mikäli kohtaat ongelmia, voit aina katsoa käyttöohjeeni uudestaan komennolla /help.'
        ),
        'process_max_price_invalid': 'Hinnan täytyy olla luku. Yritä uudestaan.',
        'process_max_price': (
            'Valmista\\! Ilmoitan sinulle heti, kun kuljetushinta on alle {price} € ' +
            'osoitteelle *{address}*\\.'
        ),
        'start': 'Aloita syöttämällä katuosoitteesi ja kaupunkisi.',
        'stop': 'Kuljetushinnan haku lopetettu.',
        'poll_failure': 'En löytänyt kuljetushintoja osoitteelle *{address}*\\. Haku lopetettu\\.',
        'poll_success': 'Viimeisin kuljetushinta on {price} € ({estimate} min.). Aika tilata! 🍕 https://kotipizza.fi',
        'help': (
            'Hei! Olen Kotipizza Botti. Pystyn kertomaan sinulle lähialueesi ravintoloiden dynaamiset kuljetushinnat.\n\n'
            'Voit ohjata minua seuraavilla komennoilla:\n\n'
            '/notify - Ilmoitan, kun lähiravintolan kuljetushinta on alle määrittelemäsi maksimihinnan\n' +
            '/poll - Ilmoitan 10 minuutin välein lähiravintoloiden kuljetushinnat\n' +
            '/price - Ilmoitan lähiravintoloiden viimeisimmät kuljetushinnat\n' +
            '/getaddress - Näytän asettamasi kuljetusosoitteen\n' +
            '/setaddress - Aseta kuljetusosoitteesi\n' +
            '/stop - Lopetan kuljetushintojen haun\n' +
            '/help - Näytän sinulle nämä käyttöohjeet'
        ),
        'restaurants_closed': 'Kaikki lähialueen ravintolat ovat suljettu. Kuljetushintojen haku lopetettu.',
        'address_missing': 'Kuljetusosoite puuttuu. Syötä kuljetusosoite komennolla /setaddress.',
        'address_not_found': 'Syöttämääsi osoitetta ei löytynyt osoitepalvelusta. Yritä uudestaan jollakin toisella osoitteella.',
        'thanks': 'Kiitos!'
    },
    'en': {
        'poll': (
            'Alright\\! I\'ll notify you every 10 minutes the dynamic delivery ' +
            'prices of your nearby restaurants for address *{address}*\\.'
        ),
        'get_address': 'Your delivery address is *{address}*\\.',
        'set_address': 'What\'s the delivery address?',
        'set_max_price': 'OK! What\'s the maximum limit for the price of delivery? (e.g. "5.1" or "5,1")',
        'process_address': (
            'Thank you! Try to fetch latest prices of your nearby restaurants with command /price. ' +
            'If you have any troubles, you can always check the instructions with command /help.'
        ),
        'process_max_price_invalid': 'Price has to be a number. Try again.',
        'process_max_price': (
            'Alright\\! I\'ll notify you when the delivery price is below {price} € ' +
            'for address *{address}*\\.'
        ),
        'start': 'Start by writing your street address and city.',
        'stop': 'Stopped fetching.',
        'poll_failure': 'Could not find delivery price with given address *{address}*\\. Stopped fetching\\.',
        'poll_success': 'Current delivery price is {price} € ({estimate} min.). Time to order! 🍕 https://kotipizza.fi',
        'help': (
            'Hi! I\'m Kotipizza Bot. I can tell you the dynamic delivery fees of your nearby restaurants.\n\n'
            'You can control me by sending these commands:\n\n'
            '/notify - Notifies when delivery price is below the given limit\n' +
            '/poll - Notifies every 10 minutes the current delivery price\n' +
            '/price - Shows latest delivery price\n' +
            '/getaddress - Shows your delivery address\n' +
            '/setaddress - Set your delivery address\n' +
            '/stop - Stops fetching delivery price' +
            '/help - I\'ll show you this instruction manual'
        ),
        'restaurants_closed': 'All nearby restaurants are closed. Stopped fetching.',
        'address_missing': 'Delivery address is missing. Please set delivery address using command /setaddress',
        'address_not_found': 'Delivery address was not found from address registry. Please try again with another address.',
        'thanks': 'Thank you!'
    }
}[settings.LANGUAGE]

sys.modules[__name__] = i18n
