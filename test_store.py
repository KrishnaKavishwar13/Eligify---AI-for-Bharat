from backend.src.utils.mock_store import mock_store

internships = mock_store.get_all_internships()
print(f"Total internships: {len(internships)}")

if internships:
    print("\nFirst internship:")
    print(internships[0])
else:
    print("\nNo internships found!")
