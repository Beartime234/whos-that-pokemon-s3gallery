import os

import whos_that_pokemon_s3gallery.pokemon_assets

from whos_that_pokemon_s3gallery import config

dir_name = "./img/"


def test_pad_pokemon_id():
    assert whos_that_pokemon_s3gallery.pokemon_assets.pad_pokemon_id(1) == "001"
    assert whos_that_pokemon_s3gallery.pokemon_assets.pad_pokemon_id(23) == "023"
    assert whos_that_pokemon_s3gallery.pokemon_assets.pad_pokemon_id(144) == "144"


def test_get_pokemon_image_url():
    assert whos_that_pokemon_s3gallery.pokemon_assets.get_pokemon_assets_image_url(
        1) == f"{whos_that_pokemon_s3gallery.config['pokemon_assets_url']}001.png"


def test_get_pokemon_filename():
    assert whos_that_pokemon_s3gallery.pokemon_assets.get_pokemon_filename("bulbasaur") == "bulbasaur.png"


def test_get_pokemon_img():
    whos_that_pokemon_s3gallery.pokemon_assets.download_img_from_pokemon_assets(1)
    os.remove(f"{dir_name}bulbasaur.png")


def test_download_all_pokemon_img():
    whos_that_pokemon_s3gallery.pokemon_assets.download_all_pokemon_img()

    # Checks that we downloaded the number of files = to max pokemon id
    assert len([f for f in os.listdir(dir_name)
                if os.path.isfile(os.path.join(f"{dir_name}", f))]) == config["max_pokemon_id"]

    # Removes all the pokemon downloaded
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".png"):
            os.remove(os.path.join(dir_name, item))
    os.removedirs(dir_name)  # Removes directory


def test_get_pokemon_name_from_id():
    assert whos_that_pokemon_s3gallery.pokemon_assets.get_pokemon_name_from_id(1) == "bulbasaur"
    assert whos_that_pokemon_s3gallery.pokemon_assets.get_pokemon_name_from_id(700) == "sylveon"
