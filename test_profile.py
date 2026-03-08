import requests
import json

# Sign in
signin_resp = requests.post('http://localhost:8000/auth/signin', json={
    'email': 'rudradewatwal@gmail.com',
    'password': 'Password@123'
})

print("Signin Response:")
print(json.dumps(signin_resp.json(), indent=2))

if signin_resp.status_code == 200:
    token = signin_resp.json()['accessToken']
    
    # Get profile
    profile_resp = requests.get('http://localhost:8000/profile', headers={
        'Authorization': f'Bearer {token}'
    })
    
    print("\nProfile Response:")
    print(f"Status Code: {profile_resp.status_code}")
    print(json.dumps(profile_resp.json(), indent=2))
else:
    print(f"Signin failed with status {signin_resp.status_code}")
