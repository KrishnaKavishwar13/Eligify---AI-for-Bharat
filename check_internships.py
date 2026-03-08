import json

with open('backend/data/internships.json', 'r') as f:
    internships = json.load(f)
    print(f"Total internships in file: {len(internships)}")
    
    if internships:
        print(f"\nFirst internship ID: {internships[0]['internshipId']}")
        print(f"First internship title: {internships[0]['title']}")
