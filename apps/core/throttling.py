import time
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from django.conf import settings

class TokenBucketThrottle(BaseThrottle):
    """
    Token Bucket Rate Limiting implementation.
    Each bucket has a maximum capacity and a refill rate.
    """
    scope = None
    
    def __init__(self):
        if not self.scope:
            self.scope = "default"
        
        # Pull configuration from settings or use defaults
        throttle_config = getattr(settings, "REST_FRAMEWORK", {}).get("DEFAULT_THROTTLE_RATES", {})
        config_str = throttle_config.get(self.scope, "10/m") # Default 10 tokens per minute
        
        # Parse capacity/rate from string like "10/m" or "100/h"
        num, period = config_str.split("/")
        self.capacity = int(num)
        
        periods = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        self.refill_period = periods.get(period[0].lower(), 60)
        self.refill_rate = self.capacity / self.refill_period

    def get_cache_key(self, request, view):
        """
        By default, use the user ID if authenticated, else IP.
        """
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return f"throttle_{self.scope}_{ident}"

    def allow_request(self, request, view):
        key = self.get_cache_key(request, view)
        if key is None:
            return True

        now = time.time()
        bucket = cache.get(key, {
            "tokens": float(self.capacity),
            "last_updated": now
        })

        # Calculate refill
        elapsed = now - bucket["last_updated"]
        new_tokens = bucket["tokens"] + (elapsed * self.refill_rate)
        bucket["tokens"] = min(float(self.capacity), new_tokens)
        bucket["last_updated"] = now

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            cache.set(key, bucket, timeout=self.refill_period)
            return True

        return False

    def wait(self):
        """
        Optional: returns how long to wait before trying again.
        """
        return None

class AuthThrottle(TokenBucketThrottle):
    scope = "auth"

class TaskCreateThrottle(TokenBucketThrottle):
    scope = "task_create"

class TaskListThrottle(TokenBucketThrottle):
    scope = "task_list"
