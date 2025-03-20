import boto3

from app.config import AWS_ENDPOINT_URL, AWS_REGION, S3_BUCKET_NAME, \
    AWS_ACCESS_KEY, AWS_SECRET_KEY
from app.constants import IMAGE_FOLDER

s3_client = boto3.client(
    "s3", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,)

def upload_image_to_s3(image_id, image_file_name, image_file_content):
    """
    Uploads an image to S3

    Params:
        image_id (str): Image id of the image to be uploaded
        image_file_name (str): File name of the image to be uploaded
        image_file_content (str): base64 file content of the image to be uploaded.
    Returns:
        s3_key: S3 key of the uploaded file
    """
    s3_key = f"{IMAGE_FOLDER}/{image_id}/{image_file_name}"
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME, Key=s3_key, Body=image_file_content
    )
    return s3_key

def get_presigned_url(s3_key):
    """
    Generates a pre-signed URL to view/download the image

    Params:
        s3_key (str): S3 key of the uploaded file
    Returns:
        url: The presigned url of the uploaded image with a validity of 3600 seconds
    """
    return s3_client.generate_presigned_url(
        "get_object", Params={"Bucket": S3_BUCKET_NAME, "Key": s3_key}, ExpiresIn=3600
    )

def delete_image_from_s3(s3_key):
    """
    Deletes an image from S3

    Params:
        s3_key (str): S3 key of the uploaded file
    Returns:
        None
    """
    s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
