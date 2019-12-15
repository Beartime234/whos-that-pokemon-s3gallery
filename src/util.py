import errno
import os
import signal
from functools import wraps

import requests


def download_image_from_url(url: str, path: str) -> None:
    """Downloads an image from a specific URL. Saves it to the filename parameter in the directory parameter.
    Directory defaults to ./

    Args:
        url: The url to download the image from
        path: The name of the file to save as
    """
    r = requests.get(url)

    with open(path, 'wb') as f:
        f.write(r.content)


def create_directory(directory: str) -> None:
    """Creates a directory if it doesnt exist

    Args:
        directory: The dire

    Returns:
        None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    """Will timeout a function if it takes too long

    References:
        https://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish

    Args:
        seconds: How long it should timeout
        error_message: The error message it should produce

    Returns:

    """
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
