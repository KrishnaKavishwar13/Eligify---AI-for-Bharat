"""Utility functions"""

from src.utils.dynamodb import (
    get_item,
    put_item,
    update_item,
    delete_item,
    query_items,
    scan_items,
    batch_get_items,
    batch_write_items,
)
from src.utils.s3 import (
    upload_file,
    download_file,
    generate_presigned_url,
    delete_file,
    file_exists,
)
from src.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    generate_tokens,
    verify_token,
    extract_user_from_token,
)
from src.utils.validation import (
    validate_email,
    validate_password_strength,
    validate_github_url,
    normalize_skill_name,
)

__all__ = [
    # DynamoDB
    "get_item",
    "put_item",
    "update_item",
    "delete_item",
    "query_items",
    "scan_items",
    "batch_get_items",
    "batch_write_items",
    # S3
    "upload_file",
    "download_file",
    "generate_presigned_url",
    "delete_file",
    "file_exists",
    # Auth
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "generate_tokens",
    "verify_token",
    "extract_user_from_token",
    # Validation
    "validate_email",
    "validate_password_strength",
    "validate_github_url",
    "normalize_skill_name",
]
