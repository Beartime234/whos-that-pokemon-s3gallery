from time import sleep
from multiprocessing import Process, Pipe

import pokepy
import os

import src.img_transform
import src.s3
import src.util
from src import config, s3_bucket

output_dir = "/tmp/img/"
original_image_suffix = "-orig"
silhouette_image_suffix = "-bw"
saved_file_type = ".png"


def multi_download_all_pokemon_img() -> None:
    """Downloads all pokemon from the pokemon assets website

    Returns:
        None
    """
    # create a list to keep all processes
    processes = []

    # create a list to keep connections
    parent_connections = []

    # create a process per instance
    for i in range(1, config["max_pokemon_id"] + 1):
        download_img_from_pokemon_assets(i)
    #     # create a pipe for communication
    #     parent_conn, child_conn = Pipe()
    #     parent_connections.append(parent_conn)
    #
    #     # create the process, pass instance and connection
    #     process = Process(target=multi_download_img_from_pokemon_assets, args=(i, child_conn))
    #     processes.append(process)
    #
    # # start all processes
    # for process in processes:
    #     process.start()
    #     sleep(3)
    #
    # # make sure that all processes have finished
    # for process in processes:
    #     process.join()


def multi_download_img_from_pokemon_assets(pokemon_id: int, conn):
    """This is a simple wrapper that takes the function and wraps it in a connection so that it can be
    run by the multiprocessing pipe

    Args:
        pokemon_id: The pokemon's id
        conn: The multi processing connection

    Returns:

    """
    download_img_from_pokemon_assets(pokemon_id)
    conn.close()


async def download_img_from_pokemon_assets(pokemon_id: int):
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
    src.s3.upload_image_to_s3(orig_pokemon_filepath, s3_bucket)
    os.remove(orig_pokemon_filepath)
    src.s3.upload_image_to_s3(bw_pokemon_filepath, s3_bucket)
    os.remove(bw_pokemon_filepath)


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
    """Generates the pokemon orig file_path

    Args:
        pokemon_name: The pokemon's name
    """
    return f"{output_dir}{pokemon_name}{original_image_suffix}{saved_file_type}"


def get_pokemon_silhouette_filepath(pokemon_name: str) -> str:
    """Generates the pokemon silhouette file_path

    Args:
        pokemon_name: The pokemon's name

    Returns:
        A string with the pokemon's file_path
    """
    return f"{output_dir}{pokemon_name}{silhouette_image_suffix}{saved_file_type}"
