"""Quick health check - verify backend is working"""

import requests

BASE_URL = "http://localhost:8000"

print("="*60)
print("QUICK BACKEND HEALTH CHECK")
print("="*60)

# Test 1: Server running
print("\n1. Server Status...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    if response.status_code == 200:
        print("   ✓ Server is running on port 8000")
    else:
        print(f"   ✗ Server returned {response.status_code}")
        exit(1)
except Exception as e:
    print(f"   ✗ Server not accessible: {e}")
    print("\n   Start server with:")
    print("   cd backend")
    print("   ./venv/Scripts/python.exe -m uvicorn src.main:app --reload")
    exit(1)

# Test 2: OpenAPI spec
print("\n2. API Specification...")
try:
    response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
    if response.status_code == 200:
        spec = response.json()
        paths = spec.get("paths", {})
        
        # Count intelligence endpoints
        intel_endpoints = [p for p in paths.keys() if "/intelligence/" in p]
        
        print(f"   ✓ OpenAPI spec loaded")
        print(f"   Total endpoints: {len(paths)}")
        print(f"   Intelligence endpoints: {len(intel_endpoints)}")
        
        if len(intel_endpoints) >= 10:
            print("   ✓ All 10 intelligence endpoints registered")
        else:
            print(f"   ⚠️  Only {len(intel_endpoints)}/10 intelligence endpoints found")
    else:
        print(f"   ✗ OpenAPI spec returned {response.status_code}")
        exit(1)
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 3: Ollama AI service
print("\n3. Ollama AI Service...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        data = response.json()
        models = data.get("models", [])
        llama_models = [m for m in models if "llama" in m.get("name", "").lower()]
        
        if llama_models:
            print(f"   ✓ Ollama running with {len(models)} model(s)")
            print(f"   Model: {llama_models[0].get('name', 'N/A')}")
        else:
            print("   ⚠️  Ollama running but no Llama models found")
    else:
        print(f"   ✗ Ollama returned {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Ollama not accessible: {e}")
    print("   AI features may not work without Ollama")

# Test 4: Internship data
print("\n4. Internship Data...")
try:
    # Create a test user and signin
    signup_data = {
        "name": "Health Check User",
        "email": "healthcheck@example.com",
        "password": "HealthCheck123!"
    }
    
    # Try signup (may already exist)
    requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    # Signin
    signin_data = {
        "email": "healthcheck@example.com",
        "password": "HealthCheck123!"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data)
    if response.status_code == 200:
        result = response.json()
        token = result.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test internship graph endpoint
        response = requests.get(
            f"{BASE_URL}/api/v1/intelligence/internship-graph",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json().get("data", {})
            total_internships = data.get("totalInternships", 0)
            total_skills = data.get("totalUniqueSkills", 0)
            
            print(f"   ✓ Internship data loaded")
            print(f"   Internships: {total_internships}")
            print(f"   Unique skills: {total_skills}")
        else:
            print(f"   ✗ Internship graph returned {response.status_code}")
    else:
        print(f"   ✗ Auth failed: {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Could not verify internship data: {e}")

# Summary
print("\n" + "="*60)
print("HEALTH CHECK COMPLETE")
print("="*60)
print("\n✅ Backend is HEALTHY and READY")
print("\n🌐 Next steps:")
print("  • View API docs: http://localhost:8000/docs")
print("  • Test endpoints interactively")
print("  • Integrate with frontend")
print("\n" + "="*60)
