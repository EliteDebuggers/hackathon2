import hashlib
import hmac
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

SHARED_SECRET = B"my_private_signing_key_2026"
VALIDITY_WINDOW = 30 #signature validity is 30s

def verify_request_intergity():
    timestamp = request.headers.get("X-Timestamp")
    signature = request.headers.get("x-Signature")

    if not timestamp or not signature:
        return Flase, "Missing NTrust Security Headers (X-Timestamp / X-Signature)"

    try:
        if abs(int(time.time()) - int(timestamp)) > VALIDITY_WINDOW:
            return Flase, "Your request is expired or replay attact detected."
        except ValueError:
            return False, "Invalid timestamp formate"

    body = request.get_data(as_text=True)
    message = f"{timestamp}:{request.method}:{request.path}:{body}".encode("utf-8")
    expected_sig = hmac.new)SHARED_SECRET

    


    