import os

import requests


def download_image_from_url(url: str, filename: str, directory: str = "./img/"):
    """Downloads an image from a specific URL. Saves it to the filename parameter in the directory parameter.
    Directory defaults to ./

    Args:
        url: The url to download the image from
        filename: The name of the file to save as
        directory: The directory to save the file into. Defaults to ./
    """
    r = requests.get(url)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"{directory}{filename}", 'wb') as f:
        f.write(r.content)
