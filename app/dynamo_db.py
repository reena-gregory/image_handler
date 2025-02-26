import boto3
from app.config import AWS_ENDPOINT_URL, AWS_REGION, \
    DYNAMODB_DB_NAME, DYNAMODB_TABLE_NAME


dynamodb = boto3.resource(
    DYNAMODB_DB_NAME, endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def save_image_metadata(image_id, s3_key, metadata):
    """
    Saves image metadata in DynamoDB.

    Params:
        image_id (str): Image id of the image uploaded image
        s3_key (str): S3 key of the uploaded file
        metadata (dict): The metadata information of the uploaded image
    Returns:
        None
    """
    metadata["image_id"] = image_id
    metadata["s3_key"] = s3_key
    table.put_item(Item=metadata)


def list_images(filter_key=None, filter_value=None):
    """
    Lists all images with optional filtering

    Params:
        filter_key (str): Key on which the filter has to be applied
        filter_value (str): Value of the key on which the filter has to be applied
    Returns:
        Image list from the db, type: list
    """
    filter_kwargs = {}
    if filter_key and filter_value:
        filter_kwargs["FilterExpression"] = f"{filter_key} = :val"
        filter_kwargs["ExpressionAttributeValues"] = {":val": filter_value}
    response = table.scan(**filter_kwargs)
    return response.get("Items", [])


def get_image_metadata(image_id):
    """
    Fetches image metadata from DynamoDB.

    Params:
        image_id (str): Image id of the image uploaded image
    Returns:
        Image metadata response of one image, type: dict
    """
    response = table.get_item(Key={"image_id": image_id})
    return response.get("Item")


def delete_image_metadata(image_id):
    """
    Deletes image metadata from DynamoDB

    Params:
        image_id (str): Image id of the image uploaded image
    Returns:
        None
    """
    table.delete_item(Key={"image_id": image_id})
