import os
import json
import requests
import time
from datetime import datetime, timedelta, timezone

# =========================
# SETTINGS
# =========================

API_KEY = os.getenv("COINGECKO_API_KEY")

COINS = [
    "bitcoin",
    "ethereum",
    "tether",
    "binancecoin",
    "solana",
    "ripple",
    "usd-coin",
    "dogecoin",
    "cardano",
    "tron",
    "avalanche-2",
    "shiba-inu",
    "chainlink",
    "polkadot",
    "bitcoin-cash",
    "wrapped-bitcoin",
    "leo-token",
    "uniswap",
    "litecoin",
    "near",
    "dai",
    "internet-computer",
    "stellar",
    "monero",
    "aptos",
    "okb",
    "crypto-com-chain",
    "sui",
    "aave",
    "bittensor",
    "filecoin",
    "hedera-hashgraph",
    "arbitrum",
    "vechain",
    "mantle",
    "cosmos",
    "optimism",
    "the-graph",
    "maker",
    "algorand",
    "injective-protocol",
    "theta-token",
    "fantom",
    "flow",
    "elrond-erd-2",
    "kucoin-shares",
    "the-sandbox",
    "decentraland",
    "tezos",
    "axie-infinity",
    "lido-staked-ether",
    "rocket-pool",
    "immutable-x",
    "render-token",
    "kaspa",
    "cronos",
    "quant-network",
    "paxos-standard",
    "neo",
    "conflux-token",
    "jupiter-exchange-solana",
    "pancakeswap-token",
    "thorchain",
    "kava",
    "helium",
    "apecoin",
    "stacks",
    "gala",
    "chiliz",
    "eos",
    "mina-protocol",
    "curve-dao-token",
    "dydx",
    "zcash",
    "dash",
    "iota",
    "basic-attention-token",
    "enjincoin",
    "waves",
    "1inch",
    "compound-governance-token",
    "convex-finance",
    "blur",
    "synthetix-network-token",
    "yearn-finance",
    "lido-dao",
    "frax",
    "pax-dollar",
    "true-usd",
    "usdd",
    "paypal-usd",
    "first-digital-usd",
    "ondo-finance",
    "wormhole",
    "notcoin",
    "worldcoin-wld",
    "sei-network",
    "celestia",
    "bonk"
]

# 30 days
DAYS = 30

# CoinGecko gives hourly-level observations
# when the requested range is kept small.
CHUNK_DAYS = 30

OUTPUT_FILE = "crypto_hourly_full_load_100coins.json"

URL = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"


# =========================
# CHECK API KEY
# =========================

if not API_KEY:
    print("ERROR: COINGECKO_API_KEY is not set.")
    exit()


# =========================
# VALIDATE COINS
# =========================

print("\n========================================")
print("VALIDATING COIN IDS")
print("========================================")

valid_coins = []
invalid_coins = []

headers = {
    "x-cg-demo-api-key": API_KEY
}

for coin in COINS:

    print(f"Checking: {coin}")

    response = requests.get(
        URL.format(coin_id=coin),
        params={
            "vs_currency": "usd",
            "from": int(
                (datetime.now(timezone.utc) - timedelta(days=1)).timestamp()
            ),
            "to": int(datetime.now(timezone.utc).timestamp())
        },
        headers=headers,
        timeout=30
    )

    if response.status_code == 200:
        print(f"VALID: {coin}")
        valid_coins.append(coin)

    elif response.status_code == 404:
        print(f"INVALID: {coin}")
        invalid_coins.append(coin)

    else:
        print(f"ERROR {response.status_code}: {coin}")
        invalid_coins.append(coin)

    time.sleep(0.5)


print("\n========================================")
print("VALIDATION COMPLETE")
print("========================================")
print("Valid coins:", len(valid_coins))
print("Invalid coins:", len(invalid_coins))

if invalid_coins:
    print("\nInvalid coins:")
    for coin in invalid_coins:
        print("-", coin)

print("\nValid coins will be used for the Full Load.")


# =========================
# TIME RANGE
# =========================

end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=DAYS)


# =========================
# STORAGE
# =========================

all_data = []

seen = set()


# =========================
# COLLECT DATA
# =========================

for coin_number, coin in enumerate(valid_coins, start=1):

    print("\n========================================")
    print(f"Coin {coin_number}/{len(valid_coins)}: {coin}")
    print("========================================")

    coin_start = start_time

    while coin_start < end_time:

        coin_end = min(
            coin_start + timedelta(days=CHUNK_DAYS),
            end_time
        )

        from_timestamp = int(coin_start.timestamp())
        to_timestamp = int(coin_end.timestamp())

        print(
            f"Requesting {coin_start.date()} "
            f"to {coin_end.date()}..."
        )

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

            if response.status_code == 429:
                print("\nRATE LIMIT HIT.")
                print("Stopping safely.")
                print("Please wait before running again.")
                exit()

            if response.status_code != 200:
                print("ERROR:")
                print(response.text)

                # Move on instead of getting stuck
                coin_start = coin_end
                continue

            data = response.json()

            prices = data.get("prices", [])
            market_caps = data.get("market_caps", [])
            volumes = data.get("total_volumes", [])

            print("Observations:", len(prices))

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

            coin_start = coin_end

            time.sleep(1)

        except Exception as e:

            print("REQUEST ERROR:", e)

            # Skip failed chunk instead of infinite retry
            coin_start = coin_end


# =========================
# SAVE FILE
# =========================

output = {
    "source": "CoinGecko API",
    "load_type": "full",
    "frequency": "hourly",
    "number_of_coins": len(valid_coins),
    "coins": valid_coins,
    "start_time": start_time.isoformat(),
    "end_time": end_time.isoformat(),
    "data": all_data
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(output, file, indent=2)


# =========================
# SUMMARY
# =========================

print("\n")
print("========================================")
print("FULL LOAD COMPLETE")
print("========================================")
print("Requested coins:", len(COINS))
print("Valid coins:", len(valid_coins))
print("Invalid coins:", len(invalid_coins))
print("Total observations:", len(all_data))
print("Expected approximate observations:")
print(len(valid_coins) * DAYS * 24)
print("File:", OUTPUT_FILE)
print("========================================")