import requests
import json

# Sign in
signin_resp = requests.post('http://localhost:8000/auth/signin', json={
    'email': 'rudradewatwal@gmail.com',
    'password': 'Password@123'
})

if signin_resp.status_code == 200:
    token = signin_resp.json()['accessToken']
    
    # Get classified internships
    internships_resp = requests.get('http://localhost:8000/internships/classify', headers={
        'Authorization': f'Bearer {token}'
    })
    
    print("Internships Classification Response:")
    print(f"Status Code: {internships_resp.status_code}")
    print(f"\nFull Response:")
    print(json.dumps(internships_resp.json(), indent=2))
else:
    print(f"Signin failed with status {signin_resp.status_code}")
