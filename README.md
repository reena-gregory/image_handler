# Image Upload Service (LocalStack)
The service allows the users to upload images, store metadata, list images, and delete them using AWS services through LocalStack.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start LocalStack: `docker-compose up`
3. Deploy Lambda functions
4. Run tests: `pytest tests/`

## API Endpoints
1. **Upload Image:** `POST /upload`
2. **List Images:** `GET /images?filter_key=type&filter_value=png`
3. **View Image:** `GET /image/{image_id}`
4. **Delete Image:** `DELETE /image/{image_id}`
