import os

import boto3

s3_client = boto3.client("s3")


def upload_folder_to_s3(path: str, bucket_name: str) -> None:
    """This uploads a folder to S3

    Args:
        path: The file_path that you are uploading from
        bucket_name: The bucket you are uploading too

    Returns:
        None
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            s3_client.upload_file(os.path.join(root, file), bucket_name, file)


def upload_image_to_s3(file_path, bucket_name: str) -> None:
    """

    Args:
        file_path:
        bucket_name:

    Returns:

    """
    s3_client.upload_file(file_path, bucket_name, file_path.split("/")[-1], ExtraArgs={"ContentType": "image/png"})
