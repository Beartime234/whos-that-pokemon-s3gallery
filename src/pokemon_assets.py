import os
from multiprocessing import Pool
from typing import Tuple

import pokepy

import src.img_transform
import src.s3
import src.util
import src.dynamo
from src import config, s3_bucket

output_dir = "/tmp/img/"
original_image_suffix = "-orig"
silhouette_image_suffix = "-bw"
saved_file_type = ".png"
s3_url = f"https://{s3_bucket}.s3.amazonaws.com/"


def multi_download_all_pokemon_img() -> None:
    src.util.create_directory(output_dir)  # create a list to keep all processes
    pool = Pool()  # Creates a multiprocessing pool based on CPU's you have	    processes = []
    pool.map(download_img_from_pokemon_assets, range(1, config["max_pokemon_id"] + 1))


def download_img_from_pokemon_assets(pokemon_id: int):
    """Downloads the pokemon's image from the pokemon assets database. It will also create bw versions.

    Args:
        pokemon_id: The pokemon's id
    """
    pokemon_name = get_pokemon_name_from_id(pokemon_id)

    orig_pokemon_filepath, orig_pokemon_filename = get_pokemon_orig_fileinfo(pokemon_name)
    bw_pokemon_filepath, bw_pokemon_filename = get_pokemon_silhouette_fileinfo(pokemon_name)

    # Download the image
    src.util.download_image_from_url(get_pokemon_assets_image_url(pokemon_id),
                                     orig_pokemon_filepath)
    # Create the silhouette img
    src.img_transform.create_silhouette_of_img(orig_pokemon_filepath, bw_pokemon_filepath)
    src.s3.upload_image_to_s3(orig_pokemon_filepath, s3_bucket, orig_pokemon_filename)
    os.remove(orig_pokemon_filepath)
    src.s3.upload_image_to_s3(bw_pokemon_filepath, s3_bucket, bw_pokemon_filename)
    os.remove(bw_pokemon_filepath)
    src.dynamo.put_pokemon_data(pokemon_id, pokemon_name, get_pokemon_image_url(orig_pokemon_filename),
                                get_pokemon_image_url(bw_pokemon_filename))  # Finally load into databse


def get_pokemon_name_from_id(pokemon_id: int) -> str:
    """Gets a pokemon's name from ID

    Args:
        pokemon_id: The pokemon's id from its pokedex id

    Returns:
        The pokemon's name as a string
    """
    pokemon_name = pokepy.V2Client().get_pokemon(pokemon_id).name
    return pokemon_name.split('-')[0]  # This gets everything before the first hyphen as some of them


def get_pokemon_assets_image_url(pokemon_id: int) -> str:
    """Generates the pokemon image s3_url

    Args:
        pokemon_id: The pokemon's id

    Returns:
        The full pokemon assets s3_url
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


def get_pokemon_orig_fileinfo(pokemon_name: str) -> Tuple[str, str]:
    """Generates the pokemon orig file_path

    Args:
        pokemon_name: The pokemon's name

    Returns:
        filepath then filename
    """
    filename = f"{pokemon_name}{original_image_suffix}{saved_file_type}"
    return f"{output_dir}orig/{filename}", filename


def get_pokemon_silhouette_fileinfo(pokemon_name: str) -> Tuple[str, str]:
    """Generates the pokemon silhouette file_path

    Args:
        pokemon_name: The pokemon's name

    Returns:
        filepath then filename
    """
    filename = f"{pokemon_name}{silhouette_image_suffix}{saved_file_type}"
    return f"{output_dir}bw/{filename}", filename


def get_pokemon_image_url(file_name) -> str:
    """Gets the full image url for something being put in the S3 bucket

    Args:
        file_name: The files name

    Returns:

    """
    return f"{s3_url}{file_name}"
