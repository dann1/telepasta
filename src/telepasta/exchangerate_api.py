import requests

SITE = 'https://app.exchangerate-api.com'
NAME = 'ExchangeRate-API'

def show_rates(currency_ref, currencies_desired, api_key, invert = True):
    message = to_text_message(currency_ref, currencies_desired, api_key, invert=invert)
    return f"{NAME} exchange rates at {SITE} as of now:\n{message}"

def mostrar_tasas(currency_ref, currencies_desired, api_key, invert = True):
    message = to_text_message(currency_ref, currencies_desired, api_key, invert=invert)
    return f"Tasas de cambio de {NAME} en {SITE} ahora:\n{message}"

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
        return { response.status_code: 'Unable to fetch rates' }

def currency_rates_filtered(currency_reference, rates_currency_reference, currencies, invert):
    rates_filtered = {
        currency_reference: {}
    }

    for currency in currencies:
        if invert:
            rates_filtered[currency_reference][currency] = round(1/rates_currency_reference[currency], 2)
        else:
            rates_filtered[currency_reference][currency] = round(rates_currency_reference[currency], 2)

    return rates_filtered

def to_text_message(currency_ref, currencies_desired, api_key, invert):
    rates = currency_rates(api_key, currency_ref)
    rates_desired = currency_rates_filtered(currency_ref, rates, currencies_desired, invert=invert)

    rates_spaced = ''

    for currency in currencies_desired:
        rates_spaced += f"{currency}: -> {rates_desired[currency_ref][currency]}\n"

    return rates_spaced
