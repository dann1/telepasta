# telepasta

A Telegram currency scrapper Bot that parses exchange rate information from online services.

Providers

- [Centro Cambiario](https://www.efectivodivisas.com.mx)

## How to use

Execute the bot

```bash
./bot.py BOT_TOKEN CHAT_ID
```

In order to get your BOT_TOKEN and CHAT_ID check out the [Python Telegram API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API). The token is your own bot instance ID and the chat id refers to the group or conversation where your bot instance is intended to respond.

Setup a cronjob to get a daily execution, at 7am.

```bash
crontab -e
```

## Install

```bash
pip install bs4 requests python-telegram-bot
```

Assuming you intalled the bot at `/opt/CurrencyScrapper` add the following line.

```text
0       7       *       *       *       /opt/CurrencyScrapper/bot.py BOT_TOKEN CHAT_ID
```

## TODO

- Daily diff: compare now vs before, requires tmpfile with before value
- Google diff: compare rates vs google rate
