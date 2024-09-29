import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import time
from requests.exceptions import RequestException

CURRENCY = 'MXN'
CURRENCIES = ['USD', 'EUR', 'CAD', 'GBP']
SITE = "https://www.efectivodivisas.com.mx/index.php"
NAME = 'Centro Cambiario Efectivo'
CACHE_PATH = f"/tmp/.{'_'.join(NAME.split(' '))}"
MAX_RETRIES = 3
TIMEOUT = 2
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"


def show_deals():
    return f"{NAME} exchange rates at {SITE}:\n{to_text_message(scrap(), 'eng')}"


def mostrar_ofertas():
    return f"Tasas de cambio de {NAME} en {SITE}:\n{to_text_message(scrap())}"


def mostrar_cambio():
    deltas = diff_previous()
    message = to_text_message(deltas, lang='spa')
    return f"Cambio de tasas de {NAME} respecto al análisis anterior:\n{message}"


def show_change():
    deltas = diff_previous()
    message = to_text_message(deltas, lang='spa')
    return f"Exchange rate change of {NAME} vs previous analysis:\n{message}"


def scrap():
    """Scrapes exchange rate information from SITE

    Returns:
        dict: Buy and Sell rates for each of the CURRENCIES, or error information
    """
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(SITE, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            soup = BeautifulSoup(response.content, 'html.parser')

            exchange_rates = {}

            for currency in CURRENCIES:
                exchange_rates[currency] = {}

                # Find the row containing the currency
                currency_row = soup.find('img', alt=currency)
                if currency_row:
                    row = currency_row.find_parent('tr')

                    # Extract buy and sell rates
                    buy_rate = row.find_all('h1')[0].text.strip()
                    sell_rate = row.find_all('h1')[1].text.strip()

                    # Remove '$' and convert to float
                    exchange_rates[currency]['Buy'] = float(
                        buy_rate.replace('$', '').replace(',', ''))
                    exchange_rates[currency]['Sell'] = float(
                        sell_rate.replace('$', '').replace(',', ''))
                else:
                    print(f"Warning: Could not find data for {currency}")

            global now_rates
            now_rates = exchange_rates

            return exchange_rates

        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)  # Wait for 2 seconds before retrying
            else:
                return {"error": f"Failed to retrieve data after {MAX_RETRIES} attempts: {str(e)}"}

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    return {"error": "Failed to retrieve data after maximum retries"}

def diff_previous(rates_current=None, rates_previous=None):
    if not rates_current:
        if 'now_rates' in globals():
            rates_current = now_rates
        else:
            err = "Current rates not provided"
            sys.stderr.write(err)
            exit(1)

    if rates_previous:
        return diff(rates_current, rates_previous)
    else:
        if os.path.exists(CACHE_PATH):
            rates_cached = load_cached_rates()
            if rates_cached:
                return diff(rates_current, rates_cached)
        else:
            err = "No previous value to compare provided nor cached"
            sys.stderr.write(err)
        return {}


def diff(scrap_data_new, scrap_data_old):
    """Returns the deltas between two sets of exchange rates

    Args:
        scrap_data_new (dict): The rates to substract from
        scrap_data_old (dict): The rates to be substracted

    Returns:
        dict: The rates delta
    """
    diff_dict = {}

    for currency, rates in scrap_data_new.items():
        if currency in scrap_data_old:
            buy_diff = rates["Buy"] - scrap_data_old[currency]["Buy"]
            sell_diff = rates["Sell"] - scrap_data_old[currency]["Sell"]

            diff_dict[currency] = {
                "Buy": round(buy_diff, 2),
                "Sell": round(sell_diff, 2)
            }

    return diff_dict


def to_text_message(scrap_data, lang='spa'):
    rates_spaced = ''

    for currency, rates in scrap_data.items():
        buy_rate = rates.get("Buy", "N/A")
        sell_rate = rates.get("Sell", "N/A")

        if lang == 'spa':
            rates_spaced += f"{currency}: Compra -> {buy_rate}  Venta -> {sell_rate}\n"
        else:
            rates_spaced += f"{currency}: Buy -> {buy_rate}  Sell -> {sell_rate}\n"

    return rates_spaced


def save_cache_rates(rates):
    with open(CACHE_PATH, 'w') as file:
        json.dump(rates, file, indent=4)


def load_cached_rates():
    try:
        with open(CACHE_PATH, 'r') as file:
            return json.load(file)
    except json.decoder.JSONDecodeError as e:
        sys.stderr.write(f"Error while reading {CACHE_PATH}: {e}")
    except FileNotFoundError:
        sys.stderr.write(f"{CACHE_PATH} not found.")
    except Exception as e:
        sys.stderr.write(e)


# example scrap data
_data_15102023 = {
    "USD": {"Buy": 17.35, "Sell": 17.55},
    "EUR": {"Buy": 18.95, "Sell": 19.35},
    "CAD": {"Buy": 12.65, "Sell": 13.25},
    "GBP": {"Buy": 22.55, "Sell": 23.35}
}


def _show_deals_static():
    return f"{NAME} exchange rates at {SITE} as of now:\n{to_text_message(scrap(), 'eng')}"


def _mostrar_ofertas_static():
    return f"Tasas de cambio del {NAME} en {SITE}:\n{to_text_message(_data_15102023)}"
