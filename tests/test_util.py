import os

import src.util


def test_download_image_from_url():
    src.util.download_image_from_url(
        "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png", "./google.png")
    os.remove("./google.png")
