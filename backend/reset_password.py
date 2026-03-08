"""Quick password reset utility for local development"""

import json
import hashlib
from pathlib import Path

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def reset_password(email: str, new_password: str):
    """Reset password for a user"""
    users_file = Path(__file__).parent / "data" / "persistence" / "users.json"
    
    if not users_file.exists():
        print(f"❌ Users file not found: {users_file}")
        return
    
    # Load users
    with open(users_file, "r") as f:
        users = json.load(f)
    
    # Find user by email
    user_id = None
    for uid, user_data in users.items():
        if user_data.get("email") == email:
            user_id = uid
            break
    
    if not user_id:
        print(f"❌ User not found: {email}")
        return
    
    # Update password
    users[user_id]["password_hash"] = hash_password(new_password)
    
    # Save back
    with open(users_file, "w") as f:
        json.dump(users, f, indent=2)
    
    print(f"✅ Password reset successful for {email}")
    print(f"   New password: {new_password}")

if __name__ == "__main__":
    # Reset password for rudradewatwal@gmail.com
    email = "rudradewatwal@gmail.com"
    new_password = "Password@123"  # Valid: uppercase, lowercase, number, special char
    
    print(f"Resetting password for {email}...")
    reset_password(email, new_password)
