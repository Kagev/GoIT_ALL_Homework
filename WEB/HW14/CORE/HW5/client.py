# client.py
import asyncio, websockets, json


async def handle_user_input():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri, ping_interval=20, ping_timeout=10) as websocket:
        while True:
            message = input("Enter your message: ")
            await websocket.send(message)
            response = await websocket.recv()
            process_response(response)


def process_response(response):
    try:
        rates = json.loads(response)
        for rate_data in rates:
            for date_str, exchange_rate in rate_data.items():
                print(f"Exchange Rates for {date_str}:")
                for currency, rates in exchange_rate.items():
                    sale_rate = rates.get("sale")
                    purchase_rate = rates.get("purchase")
                    print(f"{currency}: Sale Rate - {sale_rate}, Purchase Rate - {purchase_rate}")
                print()
    except json.JSONDecodeError:
        print(response)


if __name__ == "__main__":
    asyncio.run(handle_user_input())
