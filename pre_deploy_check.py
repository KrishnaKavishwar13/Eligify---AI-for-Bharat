"""Pre-deployment health check script"""

import sys
import subprocess
import json
from pathlib import Path

def check_mark(passed):
    return "✅" if passed else "❌"

def run_checks():
    """Run all pre-deployment checks"""
    print("\n🔍 Eligify Pre-Deployment Health Check")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Backend files exist
    total_checks += 1
    backend_main = Path("backend/src/main.py").exists()
    print(f"\n{check_mark(backend_main)} Backend main.py exists")
    if backend_main:
        checks_passed += 1
    
    # Check 2: Frontend files exist
    total_checks += 1
    frontend_package = Path("frontend/package.json").exists()
    print(f"{check_mark(frontend_package)} Frontend package.json exists")
    if frontend_package:
        checks_passed += 1
    
    # Check 3: Database files exist
    total_checks += 1
    users_db = Path("backend/data/persistence/users.json").exists()
    print(f"{check_mark(users_db)} Users database exists")
    if users_db:
        checks_passed += 1
        # Check if users exist
        with open("backend/data/persistence/users.json") as f:
            users = json.load(f)
            print(f"   📊 {len(users)} user(s) in database")
    
    # Check 4: Internships data exists
    total_checks += 1
    internships_file = Path("backend/data/internships.json").exists()
    print(f"{check_mark(internships_file)} Internships data exists")
    if internships_file:
        checks_passed += 1
        with open("backend/data/internships.json") as f:
            internships = json.load(f)
            print(f"   📊 {len(internships)} internship(s) loaded")
    
    # Check 5: Environment files
    total_checks += 1
    backend_env = Path("backend/.env").exists()
    print(f"{check_mark(backend_env)} Backend .env exists")
    if backend_env:
        checks_passed += 1
    
    total_checks += 1
    frontend_env = Path("frontend/.env.local").exists()
    print(f"{check_mark(frontend_env)} Frontend .env.local exists")
    if frontend_env:
        checks_passed += 1
    
    # Check 6: Docker files
    total_checks += 1
    docker_compose = Path("docker-compose.yml").exists()
    print(f"{check_mark(docker_compose)} docker-compose.yml exists")
    if docker_compose:
        checks_passed += 1
    
    # Check 7: Deployment configs
    total_checks += 1
    backend_dockerfile = Path("backend/Dockerfile").exists()
    print(f"{check_mark(backend_dockerfile)} Backend Dockerfile exists")
    if backend_dockerfile:
        checks_passed += 1
    
    total_checks += 1
    frontend_dockerfile = Path("frontend/Dockerfile").exists()
    print(f"{check_mark(frontend_dockerfile)} Frontend Dockerfile exists")
    if frontend_dockerfile:
        checks_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Results: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("\n✅ All checks passed! Ready to deploy!")
        print("\n🚀 Next steps:")
        print("   1. Run: docker-compose up --build")
        print("   2. Or deploy to Vercel + Railway")
        print("   3. See DEPLOY.md for detailed instructions")
        return 0
    else:
        print(f"\n⚠️  {total_checks - checks_passed} check(s) failed")
        print("   Fix the issues above before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(run_checks())
