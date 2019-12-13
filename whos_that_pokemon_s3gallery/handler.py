import whos_that_pokemon_s3gallery.pokemon_assets

import logging

import datetime


def run(event, context):
    current_date = datetime.datetime.now()
    logging.debug(f"Running whos_that_pokemon_s3gallery: {current_date}")
    whos_that_pokemon_s3gallery.pokemon_assets.download_all_pokemon_img()
    whos_that_pokemon_s3gallery.pokemon_assets.upload_all_pokemon_img()
    logging.debug(f"Successfully completed; {current_date}")
