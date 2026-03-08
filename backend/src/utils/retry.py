"""Retry logic with exponential backoff"""

import asyncio
import logging
from typing import Callable, TypeVar, Optional, Type
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')


async def retry_with_backoff(
    func: Callable[..., T],
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
) -> T:
    """
    Retry a function with exponential backoff
    
    Args:
        func: Async function to retry
        max_attempts: Maximum number of attempts (default: 3)
        initial_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay in seconds (default: 10.0)
        exponential_base: Base for exponential backoff (default: 2.0)
        exceptions: Tuple of exceptions to catch (default: all exceptions)
        on_retry: Optional callback function called on each retry
    
    Returns:
        Result of the function call
    
    Raises:
        The last exception if all attempts fail
    """
    last_exception = None
    delay = initial_delay
    
    for attempt in range(1, max_attempts + 1):
        try:
            return await func()
        except exceptions as e:
            last_exception = e
            
            if attempt == max_attempts:
                logger.error(
                    f"All {max_attempts} attempts failed for {func.__name__}: {str(e)}"
                )
                raise
            
            # Call retry callback if provided
            if on_retry:
                on_retry(e, attempt)
            
            logger.warning(
                f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {str(e)}. "
                f"Retrying in {delay:.2f}s..."
            )
            
            await asyncio.sleep(delay)
            
            # Calculate next delay with exponential backoff
            delay = min(delay * exponential_base, max_delay)
    
    # This should never be reached, but just in case
    if last_exception:
        raise last_exception
    raise RuntimeError("Retry logic failed unexpectedly")


def with_retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator for retrying async functions with exponential backoff
    
    Usage:
        @with_retry(max_attempts=3, initial_delay=1.0)
        async def my_function():
            # Your code here
            pass
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async def call_func():
                return await func(*args, **kwargs)
            
            return await retry_with_backoff(
                call_func,
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                max_delay=max_delay,
                exponential_base=exponential_base,
                exceptions=exceptions
            )
        return wrapper
    return decorator


# Specific retry decorators for common services

def retry_ollama(max_attempts: int = 3):
    """Retry decorator specifically for Ollama API calls"""
    return with_retry(
        max_attempts=max_attempts,
        initial_delay=2.0,
        max_delay=10.0,
        exceptions=(Exception,)  # Catch all exceptions for AI service
    )


def retry_database(max_attempts: int = 3):
    """Retry decorator specifically for database operations"""
    return with_retry(
        max_attempts=max_attempts,
        initial_delay=0.5,
        max_delay=5.0,
        exceptions=(Exception,)  # Catch database-specific exceptions
    )


def retry_s3(max_attempts: int = 3):
    """Retry decorator specifically for S3 operations"""
    return with_retry(
        max_attempts=max_attempts,
        initial_delay=1.0,
        max_delay=10.0,
        exceptions=(Exception,)  # Catch S3-specific exceptions
    )
