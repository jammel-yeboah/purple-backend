import time
import shelve

class CacheManager:
    def __init__(self, filename="cache.db"):
        # This filename will be used to store our cached entries on disk.
        self.filename = filename

    def get_cached_data(self, key):
        """Return the cached response if it's within TTL, else None."""
        with shelve.open(self.filename) as cache:
            if key in cache:
                entry = cache[key]
                elapsed = time.time() - entry["timestamp"]
                if elapsed < entry["ttl"]:
                    return entry["data"]
                else:
                    # Entry expired, remove it
                    del cache[key]
        return None

    def cache_data(self, key, value, ttl=30):
        """Store the response with a timestamp and TTL."""
        with shelve.open(self.filename, writeback=True) as cache:
            cache[key] = {
                "data": value,
                "timestamp": time.time(),
                "ttl": ttl
            }
