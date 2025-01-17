import os

import src.img_transform

from tests import test_dir

test_input_image_orig = f"{test_dir}/sneasel.png"
test_output_image_silhouette = f"{test_dir}/sneasel-bw.png"


def test_create_silhouette_of_img():
    src.img_transform.create_silhouette_of_img(test_input_image_orig, test_output_image_silhouette)
    os.remove(test_output_image_silhouette)
