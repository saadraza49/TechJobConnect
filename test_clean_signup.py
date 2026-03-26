import urllib.request
import json

def test():
    print("Testing clean signup...")
    req = urllib.request.Request(
        'http://127.0.0.1:8000/signup',
        data=json.dumps({"first_name": "New", "last_name": "User", "email": "brandnew@gmail.com", "password": "password123", "role": "job_seeker"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode('utf-8'))
            print("Signup success:", data)
    except Exception as e:
        print("HTTP Error:", e)

test()
