#!/usr/bin/env python3
"""Module that explores redis"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator function to track the call history of a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that retrieves the inputs and outputs of the method,
        and stores them in Redis.
        """
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(inputs_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    """
    Function to replay the call history of a method.
    """
    inputs_key = "{}:inputs".format(method.__qualname__)
    outputs_key = "{}:outputs".format(method.__qualname__)

    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for input_args, output in zip(inputs, outputs):
        print("{}{} -> {}".format(
            method.__qualname__, input_args.decode(), output.decode()))


class Cache:
    """
    Class representing a cache with Redis as the backend.
    """
    def __init__(self):
        """
        Initializes the Cache object and sets up the Redis connection.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the cache and returns a unique key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
                                                str, bytes, int, None]:
        """
        Retrieves the value associated with the given key from the cache.
        If a conversion function is provided, the value will be converted
        before returning.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves the value associated with the given key from the cache
        and converts it to a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves the value associated with the given key from the cache
        and converts it to an integer.
        """
        return self.get(key, fn=int)
