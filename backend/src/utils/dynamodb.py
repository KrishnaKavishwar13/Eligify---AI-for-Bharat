"""DynamoDB utility functions with error handling and retry logic"""

import time
from typing import Any, Optional
from decimal import Decimal
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

from src.config.settings import settings


# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)


def python_to_dynamodb(obj: Any) -> Any:
    """Convert Python types to DynamoDB compatible types"""
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: python_to_dynamodb(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [python_to_dynamodb(item) for item in obj]
    return obj


def dynamodb_to_python(obj: Any) -> Any:
    """Convert DynamoDB types to Python types"""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    elif isinstance(obj, dict):
        return {k: dynamodb_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [dynamodb_to_python(item) for item in obj]
    return obj


def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 0.1):
    """
    Retry function with exponential backoff
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        
    Returns:
        Function result
        
    Raises:
        Last exception if all retries fail
    """
    for attempt in range(max_retries):
        try:
            return func()
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            
            # Don't retry on certain errors
            if error_code in ["ResourceNotFoundException", "ValidationException"]:
                raise
            
            # Retry on throttling and other transient errors
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                raise


async def get_item(
    table_name: str,
    key: dict[str, Any],
    consistent_read: bool = False
) -> Optional[dict[str, Any]]:
    """
    Get item from DynamoDB table
    
    Args:
        table_name: Name of the table
        key: Primary key of the item
        consistent_read: Whether to use consistent read
        
    Returns:
        Item dict or None if not found
    """
    def _get():
        table = dynamodb.Table(table_name)
        response = table.get_item(
            Key=python_to_dynamodb(key),
            ConsistentRead=consistent_read
        )
        return response.get("Item")
    
    try:
        item = retry_with_backoff(_get)
        return dynamodb_to_python(item) if item else None
    except ClientError as e:
        print(f"Error getting item from {table_name}: {e}")
        raise


async def put_item(
    table_name: str,
    item: dict[str, Any],
    condition_expression: Optional[str] = None
) -> dict[str, Any]:
    """
    Put item into DynamoDB table
    
    Args:
        table_name: Name of the table
        item: Item to put
        condition_expression: Optional condition expression
        
    Returns:
        The item that was put
    """
    def _put():
        table = dynamodb.Table(table_name)
        kwargs = {"Item": python_to_dynamodb(item)}
        if condition_expression:
            kwargs["ConditionExpression"] = condition_expression
        table.put_item(**kwargs)
        return item
    
    try:
        return retry_with_backoff(_put)
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            raise ValueError("Condition check failed - item may already exist or version mismatch")
        print(f"Error putting item into {table_name}: {e}")
        raise


async def update_item(
    table_name: str,
    key: dict[str, Any],
    update_expression: str,
    expression_attribute_values: dict[str, Any],
    expression_attribute_names: Optional[dict[str, str]] = None,
    condition_expression: Optional[str] = None,
    return_values: str = "ALL_NEW"
) -> dict[str, Any]:
    """
    Update item in DynamoDB table
    
    Args:
        table_name: Name of the table
        key: Primary key of the item
        update_expression: Update expression
        expression_attribute_values: Attribute values for expression
        expression_attribute_names: Attribute names for expression
        condition_expression: Optional condition expression
        return_values: What to return (ALL_NEW, ALL_OLD, etc.)
        
    Returns:
        Updated item
    """
    def _update():
        table = dynamodb.Table(table_name)
        kwargs = {
            "Key": python_to_dynamodb(key),
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": python_to_dynamodb(expression_attribute_values),
            "ReturnValues": return_values
        }
        if expression_attribute_names:
            kwargs["ExpressionAttributeNames"] = expression_attribute_names
        if condition_expression:
            kwargs["ConditionExpression"] = condition_expression
        
        response = table.update_item(**kwargs)
        return response.get("Attributes", {})
    
    try:
        result = retry_with_backoff(_update)
        return dynamodb_to_python(result)
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            raise ValueError("Condition check failed - concurrent update detected")
        print(f"Error updating item in {table_name}: {e}")
        raise


async def delete_item(
    table_name: str,
    key: dict[str, Any],
    condition_expression: Optional[str] = None
) -> bool:
    """
    Delete item from DynamoDB table
    
    Args:
        table_name: Name of the table
        key: Primary key of the item
        condition_expression: Optional condition expression
        
    Returns:
        True if deleted successfully
    """
    def _delete():
        table = dynamodb.Table(table_name)
        kwargs = {"Key": python_to_dynamodb(key)}
        if condition_expression:
            kwargs["ConditionExpression"] = condition_expression
        table.delete_item(**kwargs)
        return True
    
    try:
        return retry_with_backoff(_delete)
    except ClientError as e:
        print(f"Error deleting item from {table_name}: {e}")
        raise


async def query_items(
    table_name: str,
    key_condition_expression: Any,
    filter_expression: Optional[Any] = None,
    index_name: Optional[str] = None,
    limit: Optional[int] = None,
    scan_index_forward: bool = True
) -> list[dict[str, Any]]:
    """
    Query items from DynamoDB table
    
    Args:
        table_name: Name of the table
        key_condition_expression: Key condition expression
        filter_expression: Optional filter expression
        index_name: Optional index name for GSI
        limit: Maximum number of items to return
        scan_index_forward: Sort order (True = ascending, False = descending)
        
    Returns:
        List of items
    """
    def _query():
        table = dynamodb.Table(table_name)
        kwargs = {
            "KeyConditionExpression": key_condition_expression,
            "ScanIndexForward": scan_index_forward
        }
        if filter_expression:
            kwargs["FilterExpression"] = filter_expression
        if index_name:
            kwargs["IndexName"] = index_name
        if limit:
            kwargs["Limit"] = limit
        
        response = table.query(**kwargs)
        return response.get("Items", [])
    
    try:
        items = retry_with_backoff(_query)
        return [dynamodb_to_python(item) for item in items]
    except ClientError as e:
        print(f"Error querying items from {table_name}: {e}")
        raise


async def scan_items(
    table_name: str,
    filter_expression: Optional[Any] = None,
    limit: Optional[int] = None
) -> list[dict[str, Any]]:
    """
    Scan items from DynamoDB table
    
    Args:
        table_name: Name of the table
        filter_expression: Optional filter expression
        limit: Maximum number of items to return
        
    Returns:
        List of items
    """
    def _scan():
        table = dynamodb.Table(table_name)
        kwargs = {}
        if filter_expression:
            kwargs["FilterExpression"] = filter_expression
        if limit:
            kwargs["Limit"] = limit
        
        response = table.scan(**kwargs)
        return response.get("Items", [])
    
    try:
        items = retry_with_backoff(_scan)
        return [dynamodb_to_python(item) for item in items]
    except ClientError as e:
        print(f"Error scanning items from {table_name}: {e}")
        raise


async def batch_get_items(
    table_name: str,
    keys: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Batch get items from DynamoDB table
    
    Args:
        table_name: Name of the table
        keys: List of primary keys
        
    Returns:
        List of items
    """
    def _batch_get():
        response = dynamodb.batch_get_item(
            RequestItems={
                table_name: {
                    "Keys": [python_to_dynamodb(key) for key in keys]
                }
            }
        )
        return response.get("Responses", {}).get(table_name, [])
    
    try:
        items = retry_with_backoff(_batch_get)
        return [dynamodb_to_python(item) for item in items]
    except ClientError as e:
        print(f"Error batch getting items from {table_name}: {e}")
        raise


async def batch_write_items(
    table_name: str,
    items: list[dict[str, Any]]
) -> bool:
    """
    Batch write items to DynamoDB table
    
    Args:
        table_name: Name of the table
        items: List of items to write
        
    Returns:
        True if all items written successfully
    """
    def _batch_write():
        table = dynamodb.Table(table_name)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=python_to_dynamodb(item))
        return True
    
    try:
        return retry_with_backoff(_batch_write)
    except ClientError as e:
        print(f"Error batch writing items to {table_name}: {e}")
        raise
