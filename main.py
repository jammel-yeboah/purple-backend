# main.py
import json

# Import the endpoint functions directly from endpoints.py
from api.endpoints import (
    get_coins,
    get_coin_metadata,
    get_coin_market,
    get_top_posts,
    get_top_news,
    get_top_creators
)

def test_endpoints():
    print("=== Testing /api/coins ===")
    coins_response = get_coins(sort="social_volume_24h", limit=5, page=0)
    print("Coins Response:", json.dumps(coins_response, indent=2))

    print("\n=== Testing /api/coin/btc ===")
    btc_metadata = get_coin_metadata("BTC")
    btc_market = get_coin_market("BTC")
    print("BTC Metadata:", json.dumps(btc_metadata, indent=2))
    print("BTC Market:", json.dumps(btc_market, indent=2))

    print("\n=== Testing /api/posts ===")
    posts_data = get_top_posts(category="cryptocurrencies")
    print("Posts Data:", json.dumps(posts_data, indent=2))

    print("\n=== Testing /api/news ===")
    news_data = get_top_news(category="cryptocurrencies")
    print("News Data:", json.dumps(news_data, indent=2))

    print("\n=== Testing /api/creators ===")
    creators_data = get_top_creators(category="cryptocurrencies")
    print("Creators Data:", json.dumps(creators_data, indent=2))

if __name__ == "__main__":
    test_endpoints()