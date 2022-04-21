import json
import requests

rates_filename = 'rates.json'


def retrieve_usd_change_rates(currency_code: str) -> dict:
    api_url = f'http://www.floatrates.com/daily/usd.json'
    r = requests.get(api_url)
    data = json.loads(r.text)[currency_code.lower()]

    return {data['code']: {'rate': data['rate'], 'inverseRate': data['inverseRate']}}


def save_usd_rates_to_json(data):
    with open(rates_filename, 'w') as f:
        json.dump(data, f)


def load_usd_rates_from_json():
    with open(rates_filename, 'r') as f:
        rates = json.load(f)
    return rates


def init_data(currency_code: str):
    data = retrieve_usd_change_rates('EUR')
    rates = {'USD': {}, 'EUR': data['EUR']}
    if currency_code.upper() != 'USD':
        data = retrieve_usd_change_rates(currency_code)
        rates[currency_code.upper()] = data[currency_code.upper()]

    save_usd_rates_to_json(rates)


def calculate_amount(currency_code: str, output_currency_code: str, amount: float, cache_rates: dict) -> float:
    if currency_code.upper() == 'USD':
        output_amount = cache_rates[output_currency_code.upper()]['rate'] * amount
    else:
        output_amount = cache_rates[currency_code.upper()]['inverseRate'] * amount
        output_amount *= cache_rates[output_currency_code.upper()]['rate']
    return output_amount


def main():
    currency_code = input()
    init_data(currency_code)

    while (output_currency_code := input()) != '':
        amount = float(input())
        print("Checking the cache...")
        cache_rates = load_usd_rates_from_json()
        if output_currency_code.upper() in cache_rates:
            print("Oh! It is in the cache!")
            if output_currency_code.upper() == 'USD':
                if currency_code.upper() == 'USD':
                    output_amount = cache_rates[output_currency_code.upper()]['rate'] * amount
                else:
                    output_amount = cache_rates[currency_code.upper()]['inverseRate'] * amount
            else:
                output_amount = calculate_amount(currency_code, output_currency_code, amount, cache_rates)
        else:
            print("Sorry, but it is not in the cache!")
            data = retrieve_usd_change_rates(output_currency_code)
            cache_rates[output_currency_code.upper()] = data[output_currency_code.upper()]
            output_amount = calculate_amount(currency_code, output_currency_code, amount, cache_rates)

            save_usd_rates_to_json(cache_rates)

        print(f"You received {output_amount:.2f} {output_currency_code.upper()}.")


if __name__ == '__main__':
    main()
