# telepasta

A Currency Scrapper Telegram Bot

Providers

- [Centro Cambiario](https://www.efectivodivisas.com.mx)

## Install

Clone the repository and install the package to get the executable

```bash
pip install .
```

### Virtual Env (Optional)

Alternatively check it out on a virtual env prior to installing it system wide

Bash

```bash
python3 -m venv venv
source venv/bin/activate # if using bash
source venv/bin/activate.fish # if using fish
pip install .
```

Deactivate virtual env after done checking

```bash
deactivate
```

## Usage

Execute the command

```bash
telepasta BOT_TOKEN CHAT_ID [OPTIONAL_LANGUAGE]
```

- Replace `BOT_TOKEN` with your bot instance token.
- Replace `CHAT_ID` with your conversation ID.
- The optional language parameter defaults to `spa` if not provided. You can use `eng`

In order to get your BOT_TOKEN and CHAT_ID check out the [Python Telegram API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API). The token is your own bot instance ID and the chat id refers to the group or conversation where your bot instance is intended to respond.

### Schedule

Setup a cronjob to get a daily execution, at 7am, for example.

```bash
crontab -e
```

Then add the following line

```text
0       7       *       *       *       telepasta BOT_TOKEN CHAT_ID
```

## TODO

- Daily diff: compare now vs before, requires tmpfile with before value
- Google diff: compare rates vs google rate
- `/rates` and `/tasas` command to get current rates
