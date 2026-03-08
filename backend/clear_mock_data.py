"""Clear all mock data - run this to reset the in-memory database"""

import sys
sys.path.insert(0, 'src')

from src.utils.mock_store import mock_store

# Clear all data
mock_store.clear_all()

print("✓ All mock data cleared!")
print("\nYou can now test with fresh user accounts.")
print("Run: python test_complete_flow.py")
