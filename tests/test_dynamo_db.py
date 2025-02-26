import pytest
import boto3
from moto import mock_dynamodb2
from app.dynamo_db import (
    save_image_metadata,
    list_images,
    get_image_metadata,
    delete_image_metadata
)
from app.config import DYNAMODB_TABLE_NAME


@pytest.fixture
def setup_dynamodb():
    """Setup mock DynamoDB table"""
    with mock_dynamodb2():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            KeySchema=[
                {"AttributeName": "image_id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "image_id", "AttributeType": "S"}
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            },
        )
        table.wait_until_exists()
        yield dynamodb


def test_save_image_metadata(setup_dynamodb):
    """Test saving image metadata"""
    save_image_metadata(
        "img-123",
        "images/img-123.jpg",
        {"user_id": "user-1", "tags": ["nature", "sunset"]}
    )
    table = setup_dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.get_item(Key={"image_id": "img-123"})
    item = response.get("Item")

    assert item is not None
    assert item["image_id"] == "img-123"
    assert item["s3_key"] == "images/img-123.jpg"
    assert item["user_id"] == "user-1"
    assert "nature" in item["tags"]


def test_list_images_without_filter(setup_dynamodb):
    """Test listing images without filters"""
    save_image_metadata(
        "img-1", "images/img-1.jpg", {"user_id": "user-A"}
    )
    save_image_metadata(
        "img-2", "images/img-2.jpg", {"user_id": "user-B"}
    )

    result = list_images()
    assert len(result) == 2


def test_list_images_with_filter(setup_dynamodb):
    """Test listing images with a filter"""
    save_image_metadata(
        "img-1", "images/img-1.jpg",
        {"user_id": "user-A", "tags": ["cat"]}
    )
    save_image_metadata(
        "img-2", "images/img-2.jpg",
        {"user_id": "user-B", "tags": ["dog"]}
    )

    filtered_result = list_images("user_id", "user-A")
    assert len(filtered_result) == 1
    assert filtered_result[0]["image_id"] == "img-1"


def test_get_image_metadata(setup_dynamodb):
    """Test fetching a single image metadata"""
    save_image_metadata(
        "img-100", "images/img-100.jpg",
        {"user_id": "user-X", "tags": ["art"]}
    )

    result = get_image_metadata("img-100")
    assert result is not None
    assert result["image_id"] == "img-100"
    assert result["s3_key"] == "images/img-100.jpg"
    assert result["user_id"] == "user-X"


def test_get_image_metadata_not_found(setup_dynamodb):
    """Test fetching metadata of a non-existent image"""
    result = get_image_metadata("non-existent-id")
    assert result is None


def test_delete_image_metadata(setup_dynamodb):
    """Test deleting an image metadata"""
    save_image_metadata(
        "img-500", "images/img-500.jpg",
        {"user_id": "user-Z"}
    )
    delete_image_metadata("img-500")

    result = get_image_metadata("img-500")
    assert result is None


def test_delete_image_metadata_not_existing(setup_dynamodb):
    """Test deleting a non-existing image should not raise error"""
    delete_image_metadata("non-existing-id")  # Should not throw an error
