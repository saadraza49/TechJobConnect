import urllib.request
import json
import traceback

def test():
    print("Testing /auth/login...")
    req = urllib.request.Request(
        'http://127.0.0.1:8000/auth/login',
        data=json.dumps({"email": "msaadraza49@gmail.com", "password": "password123"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            print("Login success:", data)
            token = data.get("access_token")
            
            print("\nTesting /profile...")
            req2 = urllib.request.Request(
                'http://127.0.0.1:8000/profile',
                headers={'Authorization': f'Bearer {token}'}
            )
            with urllib.request.urlopen(req2) as res2:
                print("Profile success:", res2.read().decode('utf-8'))
    except Exception as e:
        print("HTTP Error:", e)
        traceback.print_exc()

test()
