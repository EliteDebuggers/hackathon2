import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# import middleware
from praman import PramanMiddleware

load_dotenv()

# For CORS
app = Flask(__name__, template_folder='templates')
CORS(app, resources={
    r"/api/*": {
        "origins": "http://127.0.0.1:5500",
        "allow_headers": ["Content-Type", "X-Timestamp", "X-Signature"],
        "expose_headers": ["X-Timestamp", "X-Signature"]
    }
})

# Variables
SHARED_SECRET = os.getenv("SHARED_SECRET")
VALIDITY_WINDOW = int(os.getenv("VALIDITY_WINDOW", "30"))

# PRAMAN integration
PramanMiddleware(app, secret_key=SHARED_SECRET, validity_window=VALIDITY_WINDOW)

# Serve index.html in default port (5000)
@app.route('/')
def index():
    return render_template('index.html', 
env_secret=os.getenv('SHARED_SECRET'))

# Whitelist Endpoints
@app.before_request
def enforce_praman_security():
    if request.method == "OPTIONS" or request.path in ["/health", "/"]:
        return

    is_valid, reason = verify_request_integrity()
    if not is_valid:
        return jsonify({
            "status": "BLOCKED BY PRAMAN",
            "reason": reason,
            "threat_type": "UNAUTHORISED_SOURCE_CODE_EXPLOIT_ATTEMPT_DETECTED"
        }), 403

# Secured Endpoints (auto detected by PRAMAN)
@app.route("/api/v1/delete-user", methods=["POST"])
def delete_user():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "unknown")

    return jsonify({
        "status": "SUCCESS",
        "message": f"User '{username}' was permanently deleted."
    }), 200

# Server Running Status
if __name__ == "__main__":
    print("PRAMAN is running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
