from PIL import Image

transparent_color = (255, 255, 255, 0)
black_color = (0, 0, 0, 255)


def create_silhouette_of_img(input_image_path: str, output_image_path: str) -> None:
    """Creates a silhouette image

    Args:
        input_image_path: The name of the image you want to create a silhouette
        output_image_path: The name of the file that you want to output the silhouette too

    Returns:
        None
    """
    picture = Image.open(input_image_path)  # Open the picture

    width, height = picture.size

    # Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = picture.getpixel((x, y))
            if current_color[3] > 0:  # If it's transparent color then we skip
                # If its not transparent then we change the color to black
                # to create a sort of silhouette image
                picture.putpixel((x, y), black_color)

    picture.save(output_image_path)
