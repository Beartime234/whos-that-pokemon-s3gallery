import os

import whos_that_pokemon_s3gallery.img_transform

test_input_image = "./sneasel.png"
test_output_image_silhouette = "./sneasel-bw.png"


def test_create_silhouette_of_img():
    whos_that_pokemon_s3gallery.img_transform.create_silhouette_of_img(test_input_image, test_output_image_silhouette)
    os.remove(test_output_image_silhouette)
