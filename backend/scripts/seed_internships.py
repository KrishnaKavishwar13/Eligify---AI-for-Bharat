"""Script to seed internship data into DynamoDB"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from src.utils.dynamodb import DynamoDBClient
from src.config.settings import settings


async def seed_internships():
    """Load internship data from JSON and insert into DynamoDB"""
    
    # Initialize DynamoDB client
    db_client = DynamoDBClient()
    
    # Load internships data
    data_file = Path(__file__).parent.parent / "data" / "internships.json"
    
    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        return
    
    with open(data_file, "r") as f:
        internships = json.load(f)
    
    print(f"Loading {len(internships)} internships into DynamoDB...")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for internship in internships:
        try:
            internship_id = internship["internship_id"]
            
            # Check if internship already exists
            existing = await db_client.get_item(
                table_name=settings.INTERNSHIPS_TABLE,
                key={"internship_id": internship_id}
            )
            
            if existing:
                print(f"⏭️  Skipping {internship_id} - already exists")
                skip_count += 1
                continue
            
            # Insert internship
            await db_client.put_item(
                table_name=settings.INTERNSHIPS_TABLE,
                item=internship
            )
            
            print(f"✅ Inserted {internship_id} - {internship['title']} at {internship['company']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error inserting {internship.get('internship_id', 'unknown')}: {str(e)}")
            error_count += 1
    
    print("\n" + "="*60)
    print(f"Seeding complete!")
    print(f"✅ Successfully inserted: {success_count}")
    print(f"⏭️  Skipped (already exist): {skip_count}")
    print(f"❌ Errors: {error_count}")
    print("="*60)


if __name__ == "__main__":
    # Check if AWS credentials are configured
    if not os.getenv("AWS_ACCESS_KEY_ID") and not os.getenv("AWS_PROFILE"):
        print("Warning: AWS credentials not found in environment")
        print("Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or configure AWS_PROFILE")
    
    # Run seeding
    asyncio.run(seed_internships())
