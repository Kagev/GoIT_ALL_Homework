import aiofile, aiohttp, asyncio, argparse
import sys, websockets, json, logging
from tabulate import tabulate
from datetime import datetime, timedelta
from faker import Faker

API_URL = "https://api.privatbank.ua/p24api/exchange_rates"
LOG_FILE = "exchange_log.txt"


async def fetch_exchange_rate(session, date_str, currency_codes):
    params = {
        "date": date_str,
        "json": "",
        "coursid": 5
    }

    async with session.get(API_URL, params=params) as response:
        data = await response.json()
        rates = {rate["currency"]: {"sale": rate.get("saleRate"), "purchase": rate.get("purchaseRate")} for rate in
                 data["exchangeRate"] if rate["currency"] in currency_codes}
        return rates


async def get_exchange_rates(days, currency_codes):
    async with aiohttp.ClientSession() as session:
        rates = []
        today = datetime.now().date()
        for i in range(days):
            date_str = (today - timedelta(days=i)).strftime("%d.%m.%Y")
            exchange_rate = await fetch_exchange_rate(session, date_str, currency_codes)
            if exchange_rate:
                rates.append({date_str: exchange_rate})
        return rates


def print_exchange_rates(rates):
    for rate_data in rates:
        for date_str, exchange_rate in rate_data.items():
            headers = ["Currency", "Sale Rate", "Purchase Rate"]
            rows = []
            for currency, rates in exchange_rate.items():
                row = [currency, rates["sale"], rates["purchase"]]
                rows.append(row)
            print(f"Exchange Rates for {date_str}:")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            print("\n")


async def log_exchange_command(days):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: exchange {days}\n"
    async with aiofile.async_open(LOG_FILE, "a") as file:
        await file.write(log_entry)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Get exchange rates from PrivatBank API.")
    parser.add_argument("-d", "--days", type=int, required=False, default=1,
                        help="Number of days for which to get exchange rates (1-10).")
    parser.add_argument("-c", "--curr", dest="currencies", nargs="*", default=["USD", "EUR"],
                        help="Currency codes to include in the exchange rates.")
    return parser.parse_args()


async def get_exchange_rates_from_args():
    args = parse_arguments()

    if args.days > 10 or args.days < 1:
        print("Error: The number of days must be between 1 and 10.")
        sys.exit(1)

    currency_codes = args.currencies
    await get_and_print_exchange_rates(args.days, currency_codes)


async def get_and_print_exchange_rates(days, currency_codes):
    async with aiohttp.ClientSession() as session:
        exchange_rates = await get_exchange_rates(days, currency_codes)
        print_exchange_rates(exchange_rates)


def get_currency_codes(message):
    parts = message.split(' ')
    currency_codes = []
    for part in parts[1:]:
        currency_codes.append(part.upper())
    return currency_codes


async def handle_exchange_command(websocket, path):
    fake = Faker()
    client_name = fake.name()
    try:
        async for message in websocket:
            if message.startswith("exchange"):
                days, *currency_codes = get_currency_codes(message)
                if len(currency_codes) > 0 and days.isdigit() and 0 < int(days) <= 10:
                    rates = await get_exchange_rates(int(days), currency_codes)
                    await log_exchange_command(days)
                    response = json.dumps(rates)
                    await websocket.send(response)
                else:
                    await websocket.send(
                        "Invalid command. Usage: exchange <number_of_days> <currency_code1> <currency_code2> ...")
            elif message == "EXIT":
                await websocket.close()
                print(f"Client {client_name} disconnected by request.")
                break
            else:
                response = f"{client_name}: {message}"
                await websocket.send(response)
    except websockets.exceptions.ConnectionClosedError:
        pass
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
    finally:
        print(f"Connection with {client_name} closed.")


async def main():
    server = await websockets.serve(handle_exchange_command, "localhost", 8765, ping_interval=20, ping_timeout=10)

    try:
        print("WebSocket server started. Listening on port 8765.")
        await server.wait_closed()
    except KeyboardInterrupt:
        print("WebSocket server stopped.")
        server.close()


if __name__ == "__main__":
    asyncio.run(main())
