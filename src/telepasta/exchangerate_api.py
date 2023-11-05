import requests

SITE = 'https://app.exchangerate-api.com'
NAME = 'ExchangeRate-API'


def show_rates(currency_ref, currencies_desired, api_key, invert=True):
    message = to_text_message(
        currency_ref, currencies_desired, api_key, invert=invert)
    return f"{NAME} exchange rates at {SITE} as of now:\n{message}"


def mostrar_tasas(currency_ref, currencies_desired, api_key, invert=True):
    message = to_text_message(
        currency_ref, currencies_desired, api_key, invert=invert)
    return f"Tasas de cambio de {NAME} en {SITE} ahora:\n{message}"


def show_diff(currency_ref, rates_provider):
    deltas = diff(currency_ref, rates_provider)
    message = diff_to_text_message(deltas, lang='eng')
    return f"Clean Rate difference:\n{message}"


def mostrar_diferencia(currency_ref, rates_provider):
    deltas = diff(currency_ref, rates_provider)
    message = diff_to_text_message(deltas, lang='spa')
    return f"Diferencia vs Tasa Limpia:\n{message}"

def currency_rates(api_key, currency):
    """Returns every exchange rate for a given currency

    Args:
        api_key (String): exchangerate-api.com key tied to your user account
        currency (String): 3 character representation of the currency

    Returns:
        Dict: Conversion rate for each supported currency given the reference currency
    """

    endpoint = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()['conversion_rates']
    else:
        return {response.status_code: 'Unable to fetch rates'}


def currency_rates_filtered(currency_reference, rates_all, currencies, invert):
    """Filters SITE rates for a given reference currency

    Args:
        currency_reference (String): Currency to get rates to
        rates_all (dict): Every exchange rate from SITE
        currencies (_type_): What currencies to get the rate from
        invert (_type_): from currency reference to currencies or backwards

    Returns:
        _type_: _description_
    """
    rates_filtered = {
        currency_reference: {}
    }

    for currency in currencies:
        if invert:
            rates_filtered[currency_reference][currency] = round(
                1/rates_all[currency], 2)
        else:
            rates_filtered[currency_reference][currency] = round(
                rates_all[currency], 2)

    global now_rates
    now_rates = rates_filtered
    return rates_filtered


def to_text_message(currency_ref, currencies_desired, api_key, invert):
    rates = currency_rates(api_key, currency_ref)
    rates_desired = currency_rates_filtered(
        currency_ref, rates, currencies_desired, invert=invert)

    rates_spaced = ''

    for currency in currencies_desired:
        rates_spaced += f"{currency}: -> {rates_desired[currency_ref][currency]}\n"

    return rates_spaced


def diff(currency_ref, rates_provider):
    deltas = {}

    for currency, rates in rates_provider.items():
        deltas[currency] = {
            "Buy": round(rates["Buy"] - now_rates[currency_ref][currency], 2),
            "Sell": round(rates["Sell"] - now_rates[currency_ref][currency], 2)
        }

    return deltas


def diff_to_text_message(scrap_data, lang='spa'):
    rates_spaced = ''

    for currency, rates in scrap_data.items():
        buy_rate = rates.get("Buy", "N/A")
        sell_rate = rates.get("Sell", "N/A")

        if lang == 'spa':
            rates_spaced += f"{currency}: Compra -> {buy_rate}  Venta -> {sell_rate}\n"
        else:
            rates_spaced += f"{currency}: Buy -> {buy_rate}  Sell -> {sell_rate}\n"

    return rates_spaced

# example scrap data
_data_mxn_04112023 = {'MXN': {
    'USD': 17.46, 'EUR': 18.74, 'CAD': 12.77, 'GBP': 21.6
}}
