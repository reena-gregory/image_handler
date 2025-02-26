import json
import uuid
from app.s3_service import upload_image_to_s3, \
    get_presigned_url, delete_image_from_s3
from app.dynamodb_service import save_image_metadata, \
    list_images, get_image_metadata, delete_image_metadata


def upload_image(event, context):
    """Lambda function to upload an image"""
    body = json.loads(event["body"])
    image_id = str(uuid.uuid4())
    file_name = body["file_name"]
    file_content = body["file_content"].encode("utf-8")
    metadata = body["metadata"]

    s3_key = upload_image_to_s3(image_id, file_name, file_content)
    save_image_metadata(image_id, s3_key, metadata)

    return {
        "statusCode": 200,
        "body": json.dumps({"image_id": image_id})
    }


def list_images_handler(event, context):
    """Lambda function to list images"""
    query_params = event.get("queryStringParameters", {})
    filter_key = query_params.get("filter_key")
    filter_value = query_params.get("filter_value")

    images = list_images(filter_key, filter_value)
    return {
        "statusCode": 200,
        "body": json.dumps(images)
    }


def view_image(event, context):
    """Lambda function to generate a presigned URL for an image."""
    image_id = event["pathParameters"]["image_id"]
    metadata = get_image_metadata(image_id)

    if not metadata:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Image not found"})
        }

    image_url = get_presigned_url(metadata["s3_key"])
    return {
        "statusCode": 200,
        "body": json.dumps({"image_url": image_url})
    }


def delete_image(event, context):
    """Lambda function to delete an image."""
    image_id = event["pathParameters"]["image_id"]
    metadata = get_image_metadata(image_id)

    if not metadata:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Image not found"})
        }

    delete_image_from_s3(metadata["s3_key"])
    delete_image_metadata(image_id)
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Image deleted successfully"})
    }
