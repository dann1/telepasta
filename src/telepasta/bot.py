#!/usr/bin/env python

import os
import asyncio
import yaml
import telegram

from . import centro_cambiario
from . import exchangerate_api

def load_conf():
    conf_file = os.path.expanduser("~/.telepasta")

    with open(conf_file, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return conf

async def run_bot():
    CONF = load_conf()
    bot = telegram.Bot(CONF['telegram']['bot_token'])

    currencies_desired = centro_cambiario.CURRENCIES
    currency_ref = centro_cambiario.CURRENCY
    rates_ref_key = CONF['providers']['exchange_rate_api']['key']

    messages = []

    if CONF['lang'] == 'spa':
        messages.append(exchangerate_api.mostrar_tasas(currency_ref, currencies_desired, rates_ref_key))
        messages.append(centro_cambiario.mostrar_ofertas())
        messages.append(exchangerate_api.mostrar_diferencia(centro_cambiario.CURRENCY, centro_cambiario.now_rates))
    else:
        messages.append(exchangerate_api.show_rates(currency_ref, currencies_desired, rates_ref_key))
        messages.append(centro_cambiario.show_deals())
        messages.append(exchangerate_api.show_diff(centro_cambiario.CURRENCY, centro_cambiario.now_rates))


    for message in messages:
        async with bot:
            await bot.send_message(text=message, chat_id=CONF['telegram']['chat_id'])

def run_bot_wrapper():
    'python kekw'
    # <coroutine object main at 0x10b5ae5c0>
    # sys:1: RuntimeWarning: coroutine 'main' was never awaited
    # RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    asyncio.run(run_bot())

if __name__ == '__main__':
    run_bot_wrapper()
