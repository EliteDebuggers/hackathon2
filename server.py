import os
import hashlib
import hmac
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from flask import render_template_string

load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app, resources={
    r"/api/*": {
        "origins": "http://127.0.0.1:5500",
        "allow_headers": ["Content-Type", "X-Timestamp", "X-Signature"],
        "expose_headers": ["X-Timestamp", "X-Signature"]
    }
})

SHARED_SECRET = os.getenv("SHARED_SECRET", "NTrustHackathonR2B2").encode("utf-8") #secret key to be shared between server and client to verify authenticity
VALIDITY_WINDOW = os.getenv("VALIDITY_WINDOW", "30").encode("utf-8") #signature validity is 30s

# server setup hmac

def verify_request_integrity():
    timestamp = request.headers.get("X-Timestamp")
    signature = request.headers.get("x-Signature")

    if not timestamp or not signature:
        return False, "Missing NTrust Security Headers"

    try:
        if abs(int(time.time()) - int(timestamp)) > int(VALIDITY_WINDOW):
            return False, "Your request is expired or replay attact detected!"
    except ValueError:
            return False, "Invalid timestamp format"

    body = request.get_data(as_text=True)
    message = f"{timestamp}:{request.method}:{request.path}:{body}".encode("utf-8")
    expected_sig = hmac.new(SHARED_SECRET, message, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
        return False, "Invalid Signature! Potential tampering or unauthorised source code exploit."

    return True, "OK"

@app.route('/')
def index():
    return render_template('index.html', 
env_secret=os.getenv('SHARED_SECRET', 'NTrustHackathonR2B2'))

@app.before_request
def enforce_ntrust_security():
    if request.method == "OPTIONS" or request.path in ["/health", "/", "/favicon.ico"] or request.path.startswith("/static/"):
        return

    is_valid, reason = verify_request_integrity()
    if not is_valid:
        return jsonify({
            "status": "BLOCKED BY NTRUST",
            "reason": reason,
            "threat_type": "UNAUTHORISED_SOURCE_CODE_EXPLOIT_ATTEMPT_DETECTED"
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


