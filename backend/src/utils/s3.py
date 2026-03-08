"""S3 utility functions for file upload and management"""

import os
from datetime import datetime, timedelta
from typing import Optional, BinaryIO
import boto3
from botocore.exceptions import ClientError

from src.config.settings import settings
from src.utils.retry import retry_s3


# Initialize S3 client
s3_client = boto3.client("s3", region_name=settings.AWS_REGION)


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def is_allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file
        
    Returns:
        True if extension is allowed
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def generate_s3_key(user_id: str, filename: str) -> str:
    """
    Generate unique S3 key for file
    
    Args:
        user_id: User ID
        filename: Original filename
        
    Returns:
        S3 key in format: resumes/{user_id}/{timestamp}-{filename}
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_filename = filename.replace(" ", "_")
    return f"resumes/{user_id}/{timestamp}-{safe_filename}"


@retry_s3(max_attempts=3)
async def upload_file(
    file_obj: BinaryIO,
    filename: str,
    user_id: str,
    content_type: Optional[str] = None
) -> str:
    """
    Upload file to S3 with automatic retry
    
    Args:
        file_obj: File object to upload
        filename: Original filename
        user_id: User ID
        content_type: MIME type of the file
        
    Returns:
        S3 URI of uploaded file
        
    Raises:
        ValueError: If file type not allowed or size exceeds limit
        Exception: If upload fails after retries
    """
    # Validate file extension
    if not is_allowed_file(filename):
        raise ValueError(
            f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    file_obj.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File size ({file_size / 1024 / 1024:.2f}MB) exceeds maximum allowed size (10MB)"
        )
    
    # Generate S3 key
    s3_key = generate_s3_key(user_id, filename)
    
    # Prepare upload parameters
    extra_args = {
        "ServerSideEncryption": "AES256",
        "Metadata": {
            "user_id": user_id,
            "original_filename": filename,
            "uploaded_at": datetime.utcnow().isoformat()
        }
    }
    
    if content_type:
        extra_args["ContentType"] = content_type
    
    try:
        # Upload file
        s3_client.upload_fileobj(
            file_obj,
            settings.S3_RESUME_BUCKET,
            s3_key,
            ExtraArgs=extra_args
        )
        
        # Return S3 URI
        s3_uri = f"s3://{settings.S3_RESUME_BUCKET}/{s3_key}"
        return s3_uri
        
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        raise Exception(f"Failed to upload file: {str(e)}")


@retry_s3(max_attempts=3)
async def download_file(s3_uri: str) -> bytes:
    """
    Download file from S3 with automatic retry
    
    Args:
        s3_uri: S3 URI of the file
        
    Returns:
        File content as bytes
        
    Raises:
        ValueError: If S3 URI is invalid
        Exception: If download fails after retries
    """
    # Parse S3 URI
    if not s3_uri.startswith("s3://"):
        raise ValueError("Invalid S3 URI format")
    
    parts = s3_uri.replace("s3://", "").split("/", 1)
    if len(parts) != 2:
        raise ValueError("Invalid S3 URI format")
    
    bucket, key = parts
    
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()
    except ClientError as e:
        print(f"Error downloading file from S3: {e}")
        raise Exception(f"Failed to download file: {str(e)}")


@retry_s3(max_attempts=3)
async def generate_presigned_url(
    s3_uri: str,
    expiration: int = 3600
) -> str:
    """
    Generate presigned URL for file access with automatic retry
    
    Args:
        s3_uri: S3 URI of the file
        expiration: URL expiration time in seconds (default: 1 hour)
        
    Returns:
        Presigned URL
        
    Raises:
        ValueError: If S3 URI is invalid
        Exception: If URL generation fails after retries
    """
    # Parse S3 URI
    if not s3_uri.startswith("s3://"):
        raise ValueError("Invalid S3 URI format")
    
    parts = s3_uri.replace("s3://", "").split("/", 1)
    if len(parts) != 2:
        raise ValueError("Invalid S3 URI format")
    
    bucket, key = parts
    
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration
        )
        return url
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        raise Exception(f"Failed to generate presigned URL: {str(e)}")


@retry_s3(max_attempts=3)
async def delete_file(s3_uri: str) -> bool:
    """
    Delete file from S3 with automatic retry
    
    Args:
        s3_uri: S3 URI of the file
        
    Returns:
        True if deleted successfully
        
    Raises:
        ValueError: If S3 URI is invalid
        Exception: If deletion fails after retries
    """
    # Parse S3 URI
    if not s3_uri.startswith("s3://"):
        raise ValueError("Invalid S3 URI format")
    
    parts = s3_uri.replace("s3://", "").split("/", 1)
    if len(parts) != 2:
        raise ValueError("Invalid S3 URI format")
    
    bucket, key = parts
    
    try:
        s3_client.delete_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        print(f"Error deleting file from S3: {e}")
        raise Exception(f"Failed to delete file: {str(e)}")


async def file_exists(s3_uri: str) -> bool:
    """
    Check if file exists in S3
    
    Args:
        s3_uri: S3 URI of the file
        
    Returns:
        True if file exists
    """
    # Parse S3 URI
    if not s3_uri.startswith("s3://"):
        return False
    
    parts = s3_uri.replace("s3://", "").split("/", 1)
    if len(parts) != 2:
        return False
    
    bucket, key = parts
    
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False
