import os

import whos_that_pokemon_s3gallery.util


def test_download_image_from_url():
    whos_that_pokemon_s3gallery.util.download_image_from_url(
        "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png", "google.png")
    os.remove("./google.png")
