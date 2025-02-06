import requests
import os
import time
from api.caching import CacheManager
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
BASE_URL = "https://lunarcrush.com/api4"

class LunarCrushClient:
    def __init__(self):
        self.api_key = os.getenv("LUNARCRUSH_API_TOKEN")
        self.cache = CacheManager()

    def fetch(self, endpoint, params=None, ttl=300):
        """
        Fetch data from LunarCrush, with caching.
        
        :param endpoint: e.g. "public/coins/list/v2"
        :param params: optional dict of request parameters
        :param ttl: number of seconds to cache the response
        :return: JSON data
        """
        # Build a unique cache key based on endpoint + sorted params
        sorted_params = tuple(sorted(params.items())) if params else ()
        key = f"{endpoint}_{sorted_params}"

        # Check cache
        cached_response = self.cache.get_cached_data(key)
        if cached_response:
            return cached_response

        # Make the API call
        url = f"{BASE_URL}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        # Store in cache with the specified TTL
        self.cache.cache_data(key, data, ttl=ttl)
        
        return data
