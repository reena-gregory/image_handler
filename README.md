# Image Upload Service (LocalStack)
The service allows the users to upload images, store metadata, list images, and delete them using AWS services through LocalStack.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start LocalStack: `docker-compose up`
3. Deploy Lambda functions
4. Run tests: `pytest tests/`
5. Configure AWS CLI for LocalStack
6. `aws configure set aws_access_key_id test`
7. `aws configure set aws_secret_access_key test`
8. `aws configure set region us-east-1`
9. Verify localstack is running: `aws --endpoint-url=http://localhost:4566 s3 ls`
10. Create S3 bucket in local: `aws --endpoint-url=http://localhost:4566 s3 mb s3://image-storage`
11. Create DynamoDB in local: `aws --endpoint-url=http://localhost:4566 dynamodb create-table \
    --table-name image-metadata \
    --attribute-definitions AttributeName=image_id,AttributeType=S \
    --key-schema AttributeName=image_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1`

## API Endpoints
1. **Upload Image:** `POST /upload`
2. **List Images:** `GET /images?filter_key=type&filter_value=png`
3. **View Image:** `GET /image/{image_id}`
4. **Delete Image:** `DELETE /image/{image_id}`
