import os

import whos_that_pokemon_s3gallery.pokemon_assets


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
    os.remove("bulbasaur.png")


def test_download_all_pokemon_img():
    whos_that_pokemon_s3gallery.pokemon_assets.download_all_pokemon_img()

    # Removes all the pokemon downloaded
    dir_name = "./"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".png"):
            os.remove(os.path.join(dir_name, item))
