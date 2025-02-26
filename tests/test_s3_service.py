import boto3
import pytest
from moto import mock_s3
from app.s3_service import upload_image_to_s3, delete_image_from_s3


@pytest.fixture
def s3_mock():
    with mock_s3():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket="image-storage")
        yield client


def test_upload_image_to_s3(s3_mock):
    s3_key = upload_image_to_s3("1234", "test.jpg", b"dummy data")
    assert s3_key.startswith("images/1234/")


def test_delete_image_from_s3(s3_mock):
    s3_key = upload_image_to_s3("1234", "test.jpg", b"dummy data")
    delete_image_from_s3(s3_key)
