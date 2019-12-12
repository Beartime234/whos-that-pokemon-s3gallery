from multiprocessing import Pool

import whos_that_pokemon_s3gallery.util
from whos_that_pokemon_s3gallery import config


def download_all_pokemon_img() -> None:
    """Downloads all pokemon from the pokemon assets website

    Returns:
        None
    """
    pool = Pool()
    pool.map(download_img_from_pokemon_assets, all_pokemon_img)

def all_pokemon_img():
    """The generator function that is passed to the download_all_pokemon_img function
    JOSH NOT  A GENERATOR YOU WANT A ITERABLE GOOGLE HOW TO MAKE AN INTERABLE
    Returns:

    """
    for i in range(1, config["max_pokemon_id"] + 1):
        yield i



def download_img_from_pokemon_assets(pokemon_id: int):
    """Downloads the pokemon's image from the pokemon assets database

    Args:
        pokemon_id: The pokemon's id
    """
    whos_that_pokemon_s3gallery.util.download_image_from_url(get_pokemon_assets_image_url(pokemon_id),
                                                             get_pokemon_filename(str(pokemon_id)))


def get_pokemon_assets_image_url(pokemon_id: int) -> str:
    """Generates the pokemon image url

    Args:
        pokemon_id: The pokemon's id

    Returns:
        The full pokemon assets url
    """
    return f"{config['pokemon_assets_url']}{pad_pokemon_id(pokemon_id)}.png"


def pad_pokemon_id(pokemon_id: int) -> str:
    """Pads a pokemon's id with 0's.

    Examples:
        1 -> 001
        23 -> 023
        144 -> 144

    Args:
        pokemon_id: The pokemon's id

    Returns:
        A string with padded 0's in front.
    """
    return f"{pokemon_id:03}"


def get_pokemon_filename(pokemon_name: str):
    """Creates the pokemon filename

    Args:
        pokemon_name: The pokemon's name
    """
    return f"{pokemon_name}.png"
