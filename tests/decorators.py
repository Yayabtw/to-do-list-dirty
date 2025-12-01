"""Test case decorators for tracking test numbers."""

import functools
from typing import Callable


def tc(test_number: str) -> Callable:
    """
    Test Case decorator to associate a test number with a test method.

    This decorator marks a test method with its corresponding test number
    from the test plan (CAHIER_TESTS.md and test_list.yaml).

    Args:
        test_number: The test number as a string (e.g., "1", "2", "3")

    Returns:
        A decorator function that wraps the test method

    Example:
        @tc("1")
        def test_index_view(self):
            '''Test the index view (/).'''
            response = self.client.get(reverse('list'))
            self.assertEqual(response.status_code, 200)

    The test number is stored as an attribute on the test method,
    which can be accessed by test runners or reporting tools.
    """
    def decorator(func: Callable) -> Callable:
        """
        Decorator that adds test number metadata to the test method.

        Args:
            func: The test method to decorate

        Returns:
            The wrapped test method with test number metadata
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function that executes the test."""
            return func(*args, **kwargs)

        # Store the test number as an attribute on the function
        wrapper.test_number = test_number

        # Also store it in a way that's compatible with Django's test discovery
        wrapper.__test_number__ = test_number

        return wrapper

    return decorator


def get_test_number(test_method: Callable) -> str:
    """
    Retrieve the test number from a decorated test method.

    Args:
        test_method: The test method decorated with @tc

    Returns:
        The test number as a string, or None if not decorated

    Example:
        test_number = get_test_number(self.test_index_view)
        print(f"Running test #{test_number}")
    """
    return getattr(test_method, 'test_number', None) or \
           getattr(test_method, '__test_number__', None)
