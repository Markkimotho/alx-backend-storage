#!/usr/bin/env python3
"""Module for Implementing an expiring web cache and tracker"""
import requests
import redis
import time
from typing import Optional


redis_conn = redis.Redis()


def get_page(url: str) -> Optional[str]:
    """Function to check if the URL content is cached
    """
    cached_content = redis_conn.get(url)
    if cached_content:
        redis_conn.incr(f"count:{url}")
        return cached_content.decode()

    # Make the request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Cache the content with a 10-second expiration
        redis_conn.setex(url, 10, response.text)

        # Track the number of times the URL was accessed
        redis_conn.incr(f"count:{url}")

        return response.text

    return None
