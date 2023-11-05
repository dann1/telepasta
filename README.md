# telepasta

A Currency Scrapper Telegram Bot

Providers

- [ExchangeRate-API](https://app.exchangerate-api.com)
- [Centro Cambiario](https://www.efectivodivisas.com.mx)

## Install

Clone the repository and install the pip package to get the executable `telepasta`

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

The bot is a CLI command that on each execution will pull information from the providers and send a text message with such information. There is no periodic scrapping.

### Configure

Configure the bot execution at `~/.telepasta`, it's a YAML file.

```yaml
telegram:
  bot_token: a_string
  chat_id: an_integer
lang: 'spa'_or_another_one
providers:
  exchange_rate_api:
    key: '3e84238eb2fe87d67d69abbc'
```

- Replace `BOT_TOKEN` with your bot instance token.
- Replace `CHAT_ID` with your conversation ID.
- Language that will be used for text messages sent by the bot. Currently `spa` and `eng`
- [exchange_rate_api_key](https://app.exchangerate-api.com/dashboard) to get the clean rate reference.

In order to get your BOT_TOKEN and CHAT_ID check out the [Python Telegram API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API). The token is your own bot instance ID and the chat id refers to the group or conversation where your bot instance is intended to respond.

### Run

Execute the command

```bash
telepasta
```

### Schedule

Setup a cronjob to get a daily execution, at 7am, for example.

```bash
crontab -e
```

Then add the following line

```text
0       7       *       *       *       telepasta
```

## TODO

- Daily diff: compare now vs before, requires tmpfile with before value
- Implement OOP for
  - References: The currency exchange clean rates
    - currency reference will be loaded from config
    - providers can be blacklisted from conf
    - create schema with example

```json
{
    "MXN": {
        "USD": 17.46, "EUR": 18.74, "CAD": 12.77, "GBP": 21.6
    }
}
```

  - Providers: The currency exchange providers data
    - supported currencies
    - create schema with example

```json
{
    "USD": {"Buy": 17.35, "Sell": 17.55},
    "EUR": {"Buy": 18.95, "Sell": 19.35},
    "CAD": {"Buy": 12.65, "Sell": 13.25},
    "GBP": {"Buy": 22.55, "Sell": 23.35}
}
```

  - Bot: To abstract the communication with telegram
    - will improve testing by separating bot usage from provider usage
    - message formatting
    - language detection
    - alerts when change is postive
      - from reference
      - from provider
    - formatting
      - bold for providers and references
      - underline for alerts ?
    - commands
      - `/rates` and `/tasas` command to get current rates (providers and clean)
      - `/diff` to get diff (compare vs previous and provider vs reference delta)
