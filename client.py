import hashlib
import hmac
import time
import request
import json

SERVER_URL = "http://127.0.0.1:5000/api/v1/delete-user"
SHARED_SECRET = b"NTrustHackathonR2B2"

def send_authenticated_request(username):
    timestamp = str9int(time.time())
    payload = json.dumps({"username": username})

    #signature payload: timestamp "http_method:path:body"
    message = f"{timestamp}:POST:/api/v1/delete-user:{payload}".encode("utf-8")

    # hmac-sha256 signature
    signature = hmac.new(SHARED_SECRET, message, hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": timestamp,
        "X-Signature": signature
    }

    print("Sending request via NTrust Client...")
    response = request.post(SERVER_URL, data=payload, headers=headers)

    print(f"Status Code: {response.status_code}")
    print("Response Body:", response.json())

if __name__ == "__main__":
    send_authenticated_request("user")