#!/usr/bin/env python

import sys
import asyncio
import telegram

from . import centro_cambiario

if sys.argv.__len__() < 2:
    print("Missing bot TOKEN argument", file=sys.stderr)
    sys.exit(1)
elif sys.argv.__len__() < 3:
    print("Missing chat ID argument", file=sys.stderr)
    sys.exit(1)


TOKEN = sys.argv[1]
CHAT_ID = sys.argv[2]

async def run_bot():
    bot = telegram.Bot(TOKEN)

    if sys.argv.__len__() > 3:
        if sys.argv[3] != 'spa':
            data = centro_cambiario.show_deals()
        else:
            data = centro_cambiario.mostrar_ofertas()
    else:
        data = centro_cambiario.mostrar_ofertas()

    async with bot:
        await bot.send_message(text=data, chat_id=CHAT_ID)

def run_bot_wrapper():
    'python kekw'
    # <coroutine object main at 0x10b5ae5c0>
    # sys:1: RuntimeWarning: coroutine 'main' was never awaited
    # RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    asyncio.run(run_bot())

if __name__ == '__main__':
    run_bot_wrapper()
