import time
import functools
from typing import Type, Union, Tuple
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException
)
from utils.exceptions import TwitchTestError

def retry_on_exception(
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = (TimeoutException, StaleElementReferenceException),
    max_attempts: int = 3,
    delay: float = 1.0
):
    """
    Retry decorator for handling flaky elements
    
    Args:
        exceptions: Exception(s) to catch and retry on
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        continue
            raise last_exception
        return wrapper
    return decorator 