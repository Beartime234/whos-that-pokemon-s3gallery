from src import dynamo_table

import json
import decimal
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(dynamo_table)

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
    table.put_item(
        Item={
            "PokedexID": pokedex_id,
            "Name": pokemon_name,
            "OriginalImageUrl": pokemon_orig_image_url,
            "BWImageUrl": pokemon_bw_image_url
        }
    )
