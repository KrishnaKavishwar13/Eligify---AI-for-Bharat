"""Setup demo data for video recording"""

import json
from pathlib import Path

def setup_demo_data():
    """Prepare clean demo environment"""
    print("🎬 Setting up demo environment...")
    print("=" * 50)
    
    # Verify existing user (Rudra) has full profile
    users_file = Path("backend/data/persistence/users.json")
    profiles_file = Path("backend/data/persistence/profiles.json")
    skills_file = Path("backend/data/persistence/skills.json")
    
    # Check Rudra's data
    with open(users_file) as f:
        users = json.load(f)
    
    with open(profiles_file) as f:
        profiles = json.load(f)
    
    with open(skills_file) as f:
        skills = json.load(f)
    
    rudra_id = None
    for uid, user in users.items():
        if user['email'] == 'rudradewatwal@gmail.com':
            rudra_id = uid
            break
    
    if rudra_id:
        print(f"✅ Existing user found: {users[rudra_id]['name']}")
        print(f"   Email: {users[rudra_id]['email']}")
        
        profile = profiles.get(rudra_id, {})
        print(f"   Profile complete: {profile.get('onboardingComplete', False)}")
        print(f"   Education entries: {len(profile.get('education', []))}")
        print(f"   Experience entries: {len(profile.get('experience', []))}")
        print(f"   Projects: {len(profile.get('projects', []))}")
        print(f"   Certifications: {len(profile.get('certifications', []))}")
        
        skill_data = skills.get(rudra_id, {})
        print(f"   Total skills: {skill_data.get('totalSkills', 0)}")
        print(f"   Verified skills: {skill_data.get('verifiedSkills', 0)}")
    
    # Check internships
    internships_file = Path("backend/data/internships.json")
    with open(internships_file) as f:
        internships = json.load(f)
    
    print(f"\n✅ Internships loaded: {len(internships)}")
    
    # List some eligible ones
    print("\n📋 Sample internships that should be eligible:")
    eligible_samples = [
        "Web Developer Intern (Infosys)",
        "React Developer Intern (Wipro)",
        "Python Backend Intern (Zomato)",
        "Full Stack JavaScript Intern (Razorpay)",
        "TypeScript Developer Intern (Atlassian)",
        "Junior Web Developer (TCS)"
    ]
    for sample in eligible_samples:
        print(f"   • {sample}")
    
    print("\n" + "=" * 50)
    print("✅ Demo environment ready!")
    print("\n🎬 Demo Flow 1: New User Signup")
    print("   Name: Priya Sharma")
    print("   Email: priya.sharma@example.com")
    print("   Password: Priya@2026")
    print("\n🎬 Demo Flow 2: Existing User with Full Profile")
    print("   Email: rudradewatwal@gmail.com")
    print("   Password: Password@123")
    print("\n📍 Start here: http://localhost:3000/landing")
    print("\n💡 Tip: Test Flow 1 first to verify signup works!")

if __name__ == "__main__":
    setup_demo_data()
