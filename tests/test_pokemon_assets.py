import os

import src.pokemon_assets

from src import config
from src.pokemon_assets import output_dir, saved_file_type, silhouette_image_suffix, original_image_suffix


def test_pad_pokemon_id():
    assert src.pokemon_assets.pad_pokemon_id(1) == "001"
    assert src.pokemon_assets.pad_pokemon_id(23) == "023"
    assert src.pokemon_assets.pad_pokemon_id(144) == "144"


def test_get_pokemon_image_url():
    assert src.pokemon_assets.get_pokemon_assets_image_url(
        1) == f"{src.config['pokemon_assets_url']}001.png"


def test_get_pokemon_orig_filename():
    assert src.pokemon_assets.get_pokemon_orig_filename("bulbasaur") == f"{output_dir}bulbasaur{original_image_suffix}{saved_file_type}"


def test_get_pokemon_silhouette_filename():
    assert src.pokemon_assets.get_pokemon_silhouette_filepath("bulbasaur") == f"{output_dir}bulbasaur{silhouette_image_suffix}{saved_file_type}"


def test_get_pokemon_img():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    src.pokemon_assets.download_img_from_pokemon_assets(1)
    os.remove(f"{output_dir}bulbasaur{original_image_suffix}{saved_file_type}")
    os.remove(f"{output_dir}bulbasaur{silhouette_image_suffix}{saved_file_type}")
    os.removedirs(output_dir)


def test_download_all_pokemon_img():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    src.pokemon_assets.download_all_pokemon_img()

    # Checks that we downloaded the number of files = to max pokemon id
    # REMOVED THIS CHECK AS WE DELETE THEM AFTER CREATION

    # assert len([f for f in os.listdir(output_dir)
    #             if os.path.isfile(os.path.join(f"{output_dir}", f))]) == config["max_pokemon_id"] * 2

    # Removes all the pokemon downloaded
    test = os.listdir(output_dir)
    for item in test:
        if item.endswith(".png"):
            os.remove(os.path.join(output_dir, item))
    os.removedirs(output_dir)  # Removes directory


def test_get_pokemon_name_from_id():
    assert src.pokemon_assets.get_pokemon_name_from_id(1) == "bulbasaur"
    assert src.pokemon_assets.get_pokemon_name_from_id(700) == "sylveon"
