import os
import hashlib
import hmac
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = "http://127.0.0.1:5000/api/v1/delete-user"
SHARED_SECRET = os.getenv("SHARED_SECRET").encode("utf-8") #secret key

def send_authenticated_requests(username):
    timestamp = str(int(time.time()))
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

    print("Sending requests via NTrust Client...")
    response = requests.post(SERVER_URL, data=payload, headers=headers)

    print(f"Status Code: {response.status_code}")
    print("Response Body:", response.json())

if __name__ == "__main__":
    send_authenticated_requests("stark")