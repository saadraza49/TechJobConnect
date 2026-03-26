import requests

print("Testing /auth/login...")
res = requests.post('http://127.0.0.1:8000/auth/login', json={
    'email': 'msaadraza49@gmail.com', 'password': 'password123'
})
print(res.status_code)
print(res.text)

if res.ok:
    token = res.json()['access_token']
    print("\nTesting /profile...")
    res2 = requests.get('http://127.0.0.1:8000/profile', headers={'Authorization': f'Bearer {token}'})
    print(res2.status_code)
    print(res2.text)
