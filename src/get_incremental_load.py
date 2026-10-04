import os
import json
import requests
import time
from datetime import datetime, timedelta, timezone

API_KEY = os.getenv("COINGECKO_API_KEY")

FULL_LOAD_FILE = "crypto_hourly_full_load_100coins.json"
OUTPUT_FILE = "crypto_hourly_incremental_load_94coins.json"

URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"

INCREMENTAL_DAYS = 7

# CHECK API KEY

if not API_KEY:
    print("ERROR: COINGECKO_API_KEY is not set.")
    exit()

# READ COINS FROM FULL LOAD

if not os.path.exists(FULL_LOAD_FILE):
    print("ERROR: Full Load file not found:")
    print(FULL_LOAD_FILE)
    exit()

with open(FULL_LOAD_FILE, "r", encoding="utf-8") as file:
    full_load = json.load(file)

coins = full_load.get("coins", [])

if not coins:
    print("ERROR: No coins found in Full Load file.")
    exit()

print("INCREMENTAL LOAD GENERATOR")
print("Coins found in Full Load:", len(coins))
print("Incremental period:", INCREMENTAL_DAYS, "days")
print()

# TIME WINDOW

end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=INCREMENTAL_DAYS)

print("Start:", start_time.isoformat())
print("End:", end_time.isoformat())
print()

# API SETUP

headers = {
    "x-cg-demo-api-key": API_KEY
}

all_data = []
seen = set()

# DOWNLOAD DATA

for coin_number, coin in enumerate(coins, start=1):

    print(f"Coin {coin_number}/{len(coins)}: {coin}")

    from_timestamp = int(start_time.timestamp())
    to_timestamp = int(end_time.timestamp())

    params = {
        "vs_currency": "usd",
        "from": from_timestamp,
        "to": to_timestamp
    }

    try:

        response = requests.get(
            URL.format(coin_id=coin),
            params=params,
            headers=headers,
            timeout=30
        )

        print("Status:", response.status_code)

        # RATE LIMIT
       
        if response.status_code == 429:
            print()
            print("RATE LIMIT HIT.")
            print("Stopping safely.")
            print("Run the script again later.")
            exit()

        # OTHER ERRORS

        if response.status_code != 200:
            print("ERROR:")
            print(response.text)
            continue

        data = response.json()

        prices = data.get("prices", [])
        market_caps = data.get("market_caps", [])
        volumes = data.get("total_volumes", [])

        print("Observations:", len(prices))

        # STORE RECORDS
        for i, price_record in enumerate(prices):

            timestamp = price_record[0]
            price = price_record[1]

            market_cap = (
                market_caps[i][1]
                if i < len(market_caps)
                else None
            )

            volume = (
                volumes[i][1]
                if i < len(volumes)
                else None
            )

            unique_key = (coin, timestamp)

            if unique_key in seen:
                continue

            seen.add(unique_key)

            all_data.append({
                "coin_id": coin,
                "timestamp": timestamp,
                "price": price,
                "market_cap": market_cap,
                "total_volume": volume
            })

        time.sleep(1)

    except Exception as e:

        print("REQUEST ERROR:", e)
        continue


output = {
    "source": "CoinGecko API",
    "load_type": "incremental",
    "frequency": "hourly",
    "number_of_coins": len(coins),
    "coins": coins,
    "start_time": start_time.isoformat(),
    "end_time": end_time.isoformat(),
    "data": all_data
}

# SAVE FILE

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(output, file, indent=2)


# FINAL SUMMARY

print()
print("INCREMENTAL LOAD COMPLETE")
print("Coins:", len(coins))
print("Total observations:", len(all_data))
print("Expected approximately:", len(coins) * INCREMENTAL_DAYS * 24)
print("File:", OUTPUT_FILE)
