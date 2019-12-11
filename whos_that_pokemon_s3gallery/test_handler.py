import pytest
import os

from whos_that_pokemon_s3gallery import handler


def test_download_image_from_url():
    handler.download_image_from_url(
        "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png", "google.png")
    os.remove("./google.png")


def test_pad_pokemon_id():
    assert handler.pad_pokemon_id(1) == "001"
    assert handler.pad_pokemon_id(23) == "023"
    assert handler.pad_pokemon_id(144) == "144"
