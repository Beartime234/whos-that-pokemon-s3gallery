from src import dynamo_table

import json
import decimal
import boto3


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def put_pokemon_data(pokedex_id: int, pokemon_name: str, pokemon_orig_image_url: str, pokemon_bw_image_url: str):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(dynamo_table)
    table.put_item(
        Item={
            "PokedexID": pokedex_id,
            "PokemonName": pokemon_name,
            "PokemonOriginalImageUrl": pokemon_orig_image_url,
            "PokemonBWImageUrl": pokemon_bw_image_url
        }
    )
