"""Test if projects are loaded correctly"""

from src.utils.enhanced_store import enhanced_store

# Check what's loaded
print("=" * 60)
print("PROJECTS LOAD TEST")
print("=" * 60)

# Get user projects
user_id = "9c27f1b2-8c3d-4df4-a0d0-e2252ee94861"
projects = enhanced_store.get_user_projects(user_id)

print(f"\nUser ID: {user_id}")
print(f"Projects found: {len(projects)}")

if projects:
    print("\nProject details:")
    for proj in projects:
        print(f"  - {proj.get('projectId')}: {proj.get('title')} ({proj.get('status')})")
else:
    print("\n⚠️  No projects found!")
    print("\nDebug info:")
    print(f"  Total projects in store: {len(enhanced_store._projects)}")
    print(f"  Project IDs: {list(enhanced_store._projects.keys())}")
    print(f"  User index: {dict(enhanced_store._project_user_index)}")

print("\n" + "=" * 60)
