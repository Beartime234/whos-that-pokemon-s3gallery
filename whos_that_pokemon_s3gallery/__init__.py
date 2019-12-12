import os

import yaml

module_dir = os.path.dirname(__file__)

s3_bucket = os.getenv("S3_BUCKET")
config = {}

with open(f"{module_dir}/config.yml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        raise SystemExit
