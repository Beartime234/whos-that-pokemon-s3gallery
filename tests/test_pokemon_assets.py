import os
import shutil
from typing import Tuple

import src.pokemon_assets
from src.pokemon_assets import output_dir, saved_file_type, silhouette_image_suffix, original_image_suffix, \
    original_image_s3_path, silhouette_image_s3_path


def test_pad_pokemon_id():
    assert src.pokemon_assets.pad_pokemon_id(1) == "001"
    assert src.pokemon_assets.pad_pokemon_id(23) == "023"
    assert src.pokemon_assets.pad_pokemon_id(144) == "144"


def test_get_pokemon_image_url():
    assert src.pokemon_assets.get_pokemon_assets_image_url(
        1) == f"{src.config['pokemon_assets_url']}001.png"


def test_get_pokemon_orig_fileinfo():
    assert src.pokemon_assets.get_pokemon_orig_fileinfo("bulbasaur") == (
    f"{output_dir}{original_image_s3_path}bulbasaur{original_image_suffix}{saved_file_type}",
    f"bulbasaur{original_image_suffix}{saved_file_type}")


def test_get_pokemon_silhouette_fileinfo():
    src.pokemon_assets.get_pokemon_silhouette_fileinfo("bulbasaur")


def test_download_img_from_pokemon_assets():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(output_dir + original_image_s3_path):
        os.makedirs(output_dir + original_image_s3_path)
    if not os.path.exists(output_dir + silhouette_image_s3_path):
        os.makedirs(output_dir + silhouette_image_s3_path)
    src.pokemon_assets.download_img_from_pokemon_assets(1)
    shutil.rmtree(output_dir)


# def test_download_all_pokemon_img():
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     src.pokemon_assets.multi_download_all_pokemon_img()
#
#     # assert len([f for f in os.listdir(output_dir)
#     #             if os.path.isfile(os.path.join(f"{output_dir}", f))]) == config["max_pokemon_id"] * 2
#
#     os.removedirs(output_dir)  # Removes directory


def test_get_pokemon_name_from_id():
    assert src.pokemon_assets.get_pokemon_name_from_id(1) == "bulbasaur"
    assert src.pokemon_assets.get_pokemon_name_from_id(700) == "sylveon"
    assert src.pokemon_assets.get_pokemon_name_from_id(550) == "basculin"
    assert src.pokemon_assets.get_pokemon_name_from_id(772) == "type: null"
