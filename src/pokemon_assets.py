from multiprocessing import Pool

import pokepy

import src.img_transform
import src.s3
import src.util
from src import config, s3_bucket

output_dir = "/tmp/img/"
original_image_suffix = "-orig"
silhouette_image_suffix = "-bw"
saved_file_type = ".png"


def upload_all_pokemon_img() -> None:
    """Uploads all the pokemon images to S3

    Returns:
        None
    """
    src.s3.upload_folder_to_s3(output_dir, s3_bucket)


def download_all_pokemon_img() -> None:
    """Downloads all pokemon from the pokemon assets website

    Returns:
        None
    """
    src.util.create_directory(output_dir)
    pool = Pool()  # Creates a multiprocessing pool based on CPU's you have
    pool.map(download_img_from_pokemon_assets, range(1, config["max_pokemon_id"] + 1))


def download_img_from_pokemon_assets(pokemon_id: int):
    """Downloads the pokemon's image from the pokemon assets database. It will also create bw versions.

    Args:
        pokemon_id: The pokemon's id
    """
    pokemon_name = get_pokemon_name_from_id(pokemon_id)

    orig_pokemon_filepath = get_pokemon_orig_filename(pokemon_name)
    bw_pokemon_filepath = get_pokemon_silhouette_filepath(pokemon_name)

    # Download the image
    src.util.download_image_from_url(get_pokemon_assets_image_url(pokemon_id),
                                     orig_pokemon_filepath)
    # Create the silhouette img
    src.img_transform.create_silhouette_of_img(orig_pokemon_filepath, bw_pokemon_filepath)


def get_pokemon_name_from_id(pokemon_id: int) -> str:
    """Gets a pokemon's name from ID

    Args:
        pokemon_id: The pokemon's id from its pokedex id

    Returns:
        The pokemon's name as a string
    """
    pokemon_name = pokepy.V2Client().get_pokemon(pokemon_id).name
    return pokemon_name.split(':')[0]  # This gets everything before the first hyphen as some of them


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


def get_pokemon_orig_filename(pokemon_name: str) -> str:
    """Generates the pokemon orig path

    Args:
        pokemon_name: The pokemon's name
    """
    return f"{output_dir}{pokemon_name}{original_image_suffix}{saved_file_type}"


def get_pokemon_silhouette_filepath(pokemon_name: str) -> str:
    """Generates the pokemon silhouette path

    Args:
        pokemon_name: The pokemon's name

    Returns:
        A string with the pokemon's path
    """
    return f"{output_dir}{pokemon_name}{silhouette_image_suffix}{saved_file_type}"
