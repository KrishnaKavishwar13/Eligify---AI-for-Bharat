import requests
import json

# Create a simple test resume file
resume_content = """
RUDRA DEWATWAL
Software Engineer
Email: rudra@example.com

SKILLS
- Python, JavaScript, TypeScript, React, Node.js
- MongoDB, PostgreSQL, Git, Docker
- Communication, Problem Solving

EXPERIENCE
Frontend Developer Intern at TechStart (2025)
"""

# Save to file
with open('test_resume.txt', 'w') as f:
    f.write(resume_content)

# Sign in
signin_resp = requests.post('http://localhost:8000/auth/signin', json={
    'email': 'rudradewatwal@gmail.com',
    'password': 'Password@123'
})

if signin_resp.status_code == 200:
    token = signin_resp.json()['accessToken']
    
    # Upload resume
    with open('test_resume.txt', 'rb') as f:
        files = {'file': ('test_resume.txt', f, 'text/plain')}
        headers = {'Authorization': f'Bearer {token}'}
        
        upload_resp = requests.post(
            'http://localhost:8000/profile/upload-resume',
            files=files,
            headers=headers
        )
        
        print("Upload Response:")
        print(f"Status Code: {upload_resp.status_code}")
        print(json.dumps(upload_resp.json(), indent=2))
else:
    print(f"Signin failed: {signin_resp.status_code}")
