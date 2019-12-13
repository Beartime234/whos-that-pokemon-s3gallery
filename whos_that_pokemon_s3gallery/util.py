import os

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
