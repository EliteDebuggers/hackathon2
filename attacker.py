import requests
import json

SERVER_URL = "http://127.0.0.1:5000/api/v1/delete-user"

def run_attacker_demos():
    print("Attack 1: Direct Endpoints Exploit (No headers)")
    payload = json.dumps({"username": "admin_user"})
    headers = {"Content-Type": "application/json"}

    res1 = requests.post(SERVER_URL, data=payload, headers=headers)
    print(f"Response Code: {res1.status_code}")
    print("Response Payload:", res1.json())
    print("-" * 50)

    print("\n Attack 2: Replay / Forged Signature Attack")
    fake_headers = {
        "Content-Type": "application/json",
        "X-Timestamp": "1600000000",
        "X-Signature": "invalid_forged_signature_hash"
    }
    res2 = requests.post(SERVER_URL, data=payload, headers=fake_headers)
    print(f"Response Code: {res2.status_code}")
    print("Response Payload:", res2.json())

if __name__ == "__main__":
    run_attacker_demos()