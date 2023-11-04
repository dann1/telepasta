import requests
from bs4 import BeautifulSoup

CURRENCY = 'MXN'
CURRENCIES = ['USD', 'EUR', 'CAD', 'GBP']
SITE = "https://www.efectivodivisas.com.mx/index.php"
NAME = 'Centro Cambiario Efectivo'


def show_deals():
    return f"{NAME} exchange rates at {SITE} as of now:\n{to_text_message(scrap(), 'eng')}"


def mostrar_ofertas():
    return f"Tasas de cambio de {NAME} en {SITE} ahora:\n{to_text_message(scrap())}"


def scrap():
    response = requests.get(SITE)
    if response.status_code == 200:
        # Extracting currency values based on the <font> tag with class 'precios'
        soup = BeautifulSoup(response.content, 'html.parser')
        exchange_rates = soup.find_all('font', class_='precios')

        dict = {}
        i = 0

        for currency in CURRENCIES:
            dict[currency] = {}

            dict[currency]['Buy'] = float(exchange_rates[i].text.strip())
            dict[currency]['Sell'] = float(exchange_rates[i+1].text.strip())

            i += 2

        global now_rates
        now_rates = dict
        return dict
    else:
        return {response.status_code: response.json()}


def diff(scrap_data_new, scrap_data_old):
    diff_dict = {}

    for currency, rates in scrap_data_new.items():
        if currency in scrap_data_old:
            buy_diff = (scrap_data_old[currency]["Buy"]) - (rates["Buy"])
            sell_diff = (scrap_data_old[currency]["Sell"]) - (rates["Sell"])

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


def _show_deals_static():
    return f"{NAME} exchange rates at {SITE} as of now:\n{to_text_message(scrap(), 'eng')}"


def _mostrar_ofertas_static():
    return f"Tasas de cambio del {NAME} en {SITE}:\n{to_text_message(_data_15102023)}"


_data_15102023 = {
    "USD": {"Buy": 17.35, "Sell": 17.55},
    "EUR": {"Buy": 18.95, "Sell": 19.35},
    "CAD": {"Buy": 12.65, "Sell": 13.25},
    "GBP": {"Buy": 22.55, "Sell": 23.35}
}
