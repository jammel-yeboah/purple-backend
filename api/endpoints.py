from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import psycopg2
import time

from api.lunarcrush_client import LunarCrushClient

router = APIRouter()
client = LunarCrushClient()

# ---------------------
# CONNECT TO POSTGRES
# ---------------------
# DATABASE_URL = os.getenv("DATABASE_URL")  # Railway sets this automatically
DATABASE_URL = "postgresql://postgres:kMHdLTGqRYLyvaXurBlXMnRlEpMLKJBB@roundhouse.proxy.rlwy.net:51104/railway"

conn = psycopg2.connect(DATABASE_URL, sslmode="require")
conn.autocommit = True  # Ensures each statement executes immediately

# Create the table if it doesn't exist
with conn.cursor() as cur:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS waitlist (
        id SERIAL PRIMARY KEY,
        email TEXT NOT NULL,
        reason TEXT,
        wallet_address TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

# Pydantic model for request body
class WaitlistEntry(BaseModel):
    email: str
    reason: str
    wallet_address: str = None

# ------------- Data needed for search, coins, topics etc -------------
COIN_SET = set()  # coin symbols + names, both lowercased
COIN_CACHE_TTL = 3600
_last_coin_cache_update = 0

def update_coin_cache():
    global COIN_SET, _last_coin_cache_update

    current_time = time.time()
    if current_time - _last_coin_cache_update < COIN_CACHE_TTL:
        return

    response = client.fetch("public/coins/list/v2", params={"limit": 1000}, ttl=3600)
    if "data" in response:
        symbols = {coin["symbol"].lower() for coin in response["data"]}
        names = {coin["name"].lower() for coin in response["data"]}
        COIN_SET = symbols | names

    _last_coin_cache_update = current_time


@router.get("/api/search")
def search(query: str):
    """
    Decide if 'query' is a coin or a topic.
    Return JSON: { type: 'coin' | 'topic', value: ... }
    """
    update_coin_cache()
    query_lower = query.lower()

    if query_lower in COIN_SET:
        return {"type": "coin", "value": query_lower}
    else:
        return {"type": "topic", "value": query_lower}


# ------------------- Waitlist Route --------------------
@router.post("/api/waitlist")
def add_to_waitlist(entry: WaitlistEntry):
    """
    Inserts user data into the 'waitlist' table.
    Example JSON:
      { "email": "joe@xyz.com", "reason": "I love AI!", "wallet_address": "someSolanaAddress" }
    """
    if not entry.email:
        raise HTTPException(status_code=400, detail="Email is required")

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO waitlist (email, reason, wallet_address)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (entry.email, entry.reason, entry.wallet_address),
            )
            row_id = cur.fetchone()[0]
        return {"message": "Successfully added to waitlist!", "id": row_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------- HOME PAGE ENDPOINTS --------------------- #

@router.get("/api/coins")
def get_coins(sort: str = "market_cap_rank", limit: int = 100, page: int = 0):
    params = {"sort": sort, "limit": limit, "page": page}
    return client.fetch("public/coins/list/v2", params=params, ttl=300)

@router.get("/api/posts")
def get_top_posts(category: str = "cryptocurrencies"):
    endpoint = f"public/category/{category}/posts/v1"
    return client.fetch(endpoint, ttl=3600)

@router.get("/api/news")
def get_top_news(category: str = "cryptocurrencies"):
    endpoint = f"public/category/{category}/news/v1"
    return client.fetch(endpoint, ttl=3600)

@router.get("/api/creators")
def get_top_creators(category: str = "cryptocurrencies"):
    endpoint = f"public/category/{category}/creators/v1"
    return client.fetch(endpoint, ttl=3600)


# --------------------- COIN DETAILS --------------------- #

@router.get("/api/coin/{coin_id}/meta")
def get_coin_metadata(coin_id: str):
    return client.fetch(f"public/coins/{coin_id}/meta/v1", ttl=3600)

@router.get("/api/coin/{coin_id}/market")
def get_coin_market(coin_id: str):
    return client.fetch(f"public/coins/{coin_id}/v1", ttl=300)

@router.get("/api/coin/{coin_id}/time-series")
def get_coin_timeseries(coin_id: str):
    return client.fetch(
        f"public/coins/{coin_id}/time-series/v2",
        params={"interval": "1d"},
        ttl=600
    )


# --------------------- TOPIC DETAILS --------------------- #

@router.get("/api/topic/{topic}/posts")
def get_topic_posts(topic: str):
    endpoint = f"public/topic/{topic}/posts/v1"
    return client.fetch(endpoint, ttl=3600)

@router.get("/api/topic/{topic}/news")
def get_topic_news(topic: str):
    endpoint = f"public/topic/{topic}/news/v1"
    return client.fetch(endpoint, ttl=3600)

@router.get("/api/topic/{topic}/creators")
def get_topic_creators(topic: str):
    endpoint = f"public/topic/{topic}/creators/v1"
    return client.fetch(endpoint, ttl=3600)

@router.get("/api/topic/{topic}/summary")
def get_topic_summary(topic: str):
    endpoint = f"public/topic/{topic}/v1"
    return client.fetch(endpoint, ttl=3600)

@router.get("/api/topic/{topic}/time-series/v1")
def get_topic_timeseries(topic: str):
    endpoint = f"/public/topic/{topic}/time-series/v1"
    return client.fetch(endpoint, ttl=3600)
