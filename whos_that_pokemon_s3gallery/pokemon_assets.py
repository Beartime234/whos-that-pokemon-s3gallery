import pokepy

from multiprocessing import Pool

import whos_that_pokemon_s3gallery.util
from whos_that_pokemon_s3gallery import config


def download_all_pokemon_img() -> None:
    """Downloads all pokemon from the pokemon assets website

    Returns:
        None
    """
    pool = Pool()  # Creates a multiprocessing pool based on CPU's you have
    pool.map(download_img_from_pokemon_assets, range(1, config["max_pokemon_id"] + 1))


def download_img_from_pokemon_assets(pokemon_id: int):
    """Downloads the pokemon's image from the pokemon assets database

    Args:
        pokemon_id: The pokemon's id
    """
    pokemon_name = get_pokemon_name_from_id(pokemon_id)
    whos_that_pokemon_s3gallery.util.download_image_from_url(get_pokemon_assets_image_url(pokemon_id),
                                                             get_pokemon_filename(pokemon_name))


def get_pokemon_name_from_id(pokemon_id: int) -> str:
    """Gets a pokemon's name from ID

    Args:
        pokemon_id: The pokemon's id from its pokedex id

    Returns:
        The pokemon's name as a string
    """
    return pokepy.V2Client().get_pokemon(pokemon_id).name


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
