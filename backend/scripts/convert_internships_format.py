"""Convert internships.json from snake_case to camelCase format"""

import json
from pathlib import Path

def convert_internship(old_format):
    """Convert single internship from old format to new format"""
    
    # Convert required_skills
    required_skills = []
    for skill in old_format.get("required_skills", []):
        required_skills.append({
            "name": skill["skill_name"],
            "proficiencyLevel": skill["proficiency_required"],
            "mandatory": skill["is_mandatory"],
            "weight": skill.get("weight", 1.0)
        })
    
    # Convert main internship object
    new_format = {
        "internshipId": old_format["internship_id"],
        "title": old_format["title"],
        "company": old_format["company"],
        "description": old_format["description"],
        "requiredSkills": required_skills,
        "preferredSkills": old_format.get("preferred_skills", []),
        "duration": old_format["duration"],
        "stipend": {
            "amount": old_format["stipend"],
            "currency": "INR",
            "period": "monthly"
        } if old_format.get("stipend") else None,
        "location": old_format["location"],
        "type": old_format["type"],
        "applicationDeadline": old_format["deadline"],
        "startDate": old_format.get("start_date", "2026-06-01"),
        "endDate": old_format.get("end_date"),
        "eligibilityCriteria": old_format.get("eligibility_criteria"),
        "applicationUrl": old_format.get("application_url"),
        "applicationProcess": old_format.get("application_process"),
        "status": "active" if old_format.get("is_active", True) else "closed",
        "postedBy": old_format.get("posted_by", "admin"),
        "createdAt": old_format.get("created_at", "2026-03-01T00:00:00Z"),
        "updatedAt": old_format.get("updated_at", "2026-03-01T00:00:00Z"),
        "viewCount": old_format.get("view_count", 0),
        "applicationCount": old_format.get("application_count", 0)
    }
    
    return new_format

def main():
    # Read old format
    data_file = Path(__file__).parent.parent / "data" / "internships.json"
    
    with open(data_file, "r") as f:
        old_internships = json.load(f)
    
    # Convert all internships
    new_internships = [convert_internship(i) for i in old_internships]
    
    # Write new format
    with open(data_file, "w") as f:
        json.dump(new_internships, f, indent=2)
    
    print(f"✅ Converted {len(new_internships)} internships to new format")
    print(f"📁 Updated: {data_file}")

if __name__ == "__main__":
    main()
