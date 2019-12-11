import requests

pokemon_assets_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/detail/"


def lambda_handler(event, context):
    pass


def download_img_from_pokemon_assets(pokemon_id: int):
    """

    Args:
        pokemon_id:
    """
    pass


def get_pokemon_image_url(pokemon_id: int):
    """Generates the pokemon image url

    Args:
        pokemon_id:

    Returns:

    """
    return f"{pokemon_assets_url}{pad_pokemon_id(pokemon_id)}.png"


def pad_pokemon_id(pokemon_id: int) -> str:
    """Pads a pokemon's id with 0's.

    Examples:
        1 -> 001
        23 -> 023
        144 -> 144

    Args:
        pokemon_id:

    Returns:
        A string with padded 0's in front.
    """
    return f"{pokemon_id:03}"


def download_image_from_url(url: str, filename: str, directory: str = "./"):
    """Downloads an image from a specific URL. Saves it to the filename parameter in the directory parameter.
    Directory defaults to ./

    Args:
        url: The url to download the image from
        filename: The name of the file to save as
        directory: The directory to save the file into. Defaults to ./
    """
    r = requests.get(url)

    with open(f"{directory}{filename}", 'wb') as f:
        f.write(r.content)
