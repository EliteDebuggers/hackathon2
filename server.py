import hashlib
import hmac
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

SHARED_SECRET = b"NTrustHackathonR2B2" #secret key to be shared between server and client to verify authenticity
VALIDITY_WINDOW = 30 #signature validity is 30s

# server setup hmac

def verify_request_integrity():
    timestamp = request.headers.get("X-Timestamp")
    signature = request.headers.get("x-Signature")

    if not timestamp or not signature:
        return False, "Missing NTrust Security Headers"

    try:
        if abs(int(time.time()) - int(timestamp)) > VALIDITY_WINDOW:
            return False, "Your request is expired or replay attact detected!"
    except ValueError:
            return False, "Invalid timestamp format"

    body = request.get_data(as_text=True)
    message = f"{timestamp}:{request.method}:{request.path}:{body}".encode("utf-8")
    expected_sig = hmac.new(SHARED_SECRET, message, hashlib.sha256),hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
        return False, "Invalid Signature! Potential tampering or unauthorised source code exploit."

    return True, "OK"

@app.before_request
def enforce_ntrust_security():
    if request.path == "/health":
        return

    is_valid, reason = verify_request_integrity()
    if not is_valid:
        return jsonify({
            "status": "BLOCKED BY NTRUST",
            "reason": reason,
            "threat_type": "UNAUTHORISED_SOUCE_CODE_EXPLOIT_ATTEMPT_DETECTED"
        }), 403

@app.route("/api/v1/delete-user", methods=["POST"])
def delete_user():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "unknown")

    return jsonify({
        "status": "SUCCESS",
        "message": f"User '{username}' was permanently deleted."
    }), 200

if __name__ == "__main__":
    print("NTrust is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)


