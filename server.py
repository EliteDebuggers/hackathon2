import hashlib
import hmac
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

SHARED_SECRET = B"HackathonR2B2" #secret
VALIDITY_WINDOW = 30 #signature validity is 30s

# server setup hmac

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
    expected_sig = hmac.new(SHARED_SECRET, message, hasglib.sha256),hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
        return False, "Invalid Signature! Potential tampering or unauthorised source code exploit."

    return True, "OK"

    


