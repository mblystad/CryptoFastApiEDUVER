import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time

# -------------------------
# Configuration
# -------------------------
API_URL = "http://127.0.0.1:8000/api/v1/crypto-metadata/"
COINGECKO_TOP_COINS = "https://api.coingecko.com/api/v3/coins/markets"
COINGECKO_DETAIL = "https://api.coingecko.com/api/v3/coins/{}"
COINGECKO_TREND = "https://api.coingecko.com/api/v3/coins/{}/market_chart"

NEWS_SOURCES = [
    "https://news.google.com/search?q={}%20cryptocurrency",
    "https://www.bing.com/news/search?q={}+cryptocurrency",
    "https://duckduckgo.com/?q={}+cryptocurrency&ia=news",
    "https://www.startpage.com/sp/search?q={}+cryptocurrency"
]

TOP_N = 10
VS_CURRENCY = "usd"

def get_top_coin_ids(limit=10):
    try:
        response = requests.get(COINGECKO_TOP_COINS, params={
            "vs_currency": VS_CURRENCY,
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1
        })
        response.raise_for_status()
        return [coin["id"] for coin in response.json()]
    except Exception as e:
        print(f"❌ Failed to fetch top coins: {e}")
        return []

def get_price_trend(coin_id: str, days: int = 7) -> str:
    try:
        response = requests.get(COINGECKO_TREND.format(coin_id), params={
            "vs_currency": VS_CURRENCY,
            "days": days
        })
        response.raise_for_status()
        prices = response.json().get("prices", [])
        if len(prices) < 2:
            return "Insufficient data"
        start_price = prices[0][1]
        end_price = prices[-1][1]
        pct_change = ((end_price - start_price) / start_price) * 100
        return f"Change over {days} days: {pct_change:.2f}%"
    except Exception as e:
        print(f"⚠️ Trend fetch failed for {coin_id}: {e}")
        return "Trend unavailable"

def get_recent_headline_link(coin_name: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    for template in NEWS_SOURCES:
        try:
            url = template.format(coin_name.replace(" ", "+"))
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)
            for link in links:
                href = link["href"]
                if "http" in href and "google" not in href:
                    return href
        except Exception:
            continue
    return "No link found"

def fetch_metadata(coin_id: str) -> dict | None:
    try:
        response = requests.get(COINGECKO_DETAIL.format(coin_id))
        response.raise_for_status()
        data = response.json()
        cs = data["market_data"]["circulating_supply"]
        ms = data["market_data"]["max_supply"]
        return {
            "crypto_name": data["name"],
            "crypto_symbol": data["symbol"].upper(),
            "market_cap_rank": data.get("market_cap_rank"),
            "circulating_supply": int(cs) if cs is not None else None,
            "max_supply": int(ms) if ms is not None else None,
            "listed_exchange": "Binance",
            "notes": data["description"]["en"][:200] if data["description"]["en"] else None,
            "trend_info": get_price_trend(coin_id),
            "recent_headline": get_recent_headline_link(data["name"])
        }
    except Exception as e:
        print(f"❌ Metadata fetch failed for {coin_id}: {e}")
        return None

def upsert_metadata(payload: dict):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        existing = response.json()
        match = next((coin for coin in existing if coin["crypto_symbol"] == payload["crypto_symbol"]), None)

        if match:
            metadata_id = match["crypto_metadata_id"]
            put_response = requests.put(f"{API_URL}{metadata_id}/", json=payload)
            if put_response.status_code == 200:
                print(f"🔁 Updated {payload['crypto_symbol']}")
            else:
                print(f"❌ Failed to update {payload['crypto_symbol']}: {put_response.status_code}")
        else:
            post_response = requests.post(API_URL, json=payload)
            if post_response.status_code == 201:
                print(f"✅ Created {payload['crypto_symbol']}")
            else:
                print(f"❌ Failed to create {payload['crypto_symbol']}: {post_response.status_code}")
    except Exception as e:
        print(f"❌ Error during upsert of {payload.get('crypto_symbol', 'unknown')}: {e}")


if __name__ == "__main__":
    print(f"🚀 Fetching metadata for top {TOP_N} coins...")
    top_coins = get_top_coin_ids(TOP_N)
    for coin_id in top_coins:
        payload = fetch_metadata(coin_id)
        if payload:
            upsert_metadata(payload)
        time.sleep(20)  # ⏳ Delay to avoid 429 errors