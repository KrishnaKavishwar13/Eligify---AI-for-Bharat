import requests
import json

# Sign in
signin_resp = requests.post('http://localhost:8000/auth/signin', json={
    'email': 'rudradewatwal@gmail.com',
    'password': 'Password@123'
})

if signin_resp.status_code == 200:
    token = signin_resp.json()['accessToken']
    
    # Upload the actual DOCX resume
    docx_path = r'C:\Users\ASUS\Downloads\Resume.docx'
    
    with open(docx_path, 'rb') as f:
        files = {'file': ('Resume.docx', f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
        headers = {'Authorization': f'Bearer {token}'}
        
        print("Uploading Resume.docx...")
        upload_resp = requests.post(
            'http://localhost:8000/profile/upload-resume',
            files=files,
            headers=headers
        )
        
        print(f"\nStatus Code: {upload_resp.status_code}")
        print("\nResponse:")
        print(json.dumps(upload_resp.json(), indent=2))
else:
    print(f"Signin failed: {signin_resp.status_code}")
