import hashlib
import hmac
import time
from flask import request, jsonify

class PramanMiddleware:
    def __init__(self, app, secret_key: str, validity_window: int = 30, excluded_paths: list = None):
        """
        Initializes the Praman Security Middleware.
        """
        self.app = app
        self.secret_key = secret_key.encode("utf-8")
        self.validity_window = validity_window
        self.excluded_paths = excluded_paths or ["/health", "/"]

        self.app.before_request(self.enforce_security)

    def verify_request_integrity(self):
        timestamp = request.headers.get("X-Timestamp")
        signature = request.headers.get("X-Signature")

        if not timestamp or not signature:
            return False, "Missing PRAMAN Security Headers"

        try:
            if abs(int(time.time()) - int(timestamp)) > self.validity_window:
                return False, "Your request is expired or replay attack detected!"
        except ValueError:
            return False, "Invalid timestamp format"

        body_bytes = request.get_data() 
        message = f"{timestamp}:{request.method}:{request.path}:".encode("utf-8") + body_bytes
        
        expected_sig = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        
        signature_to_check = request.headers.get("X-Signature") or request.headers.get("x-Signature")

        if not hmac.compare_digest(expected_sig, signature_to_check):
            return False, "Invalid Signature! Potential tampering or unauthorised source code exploit."

        return True, "OK"

    def enforce_security(self):
        if request.method == "OPTIONS" or request.path in self.excluded_paths:
            return

        is_valid, reason = self.verify_request_integrity()
        if not is_valid:
            return jsonify({
                "status": "BLOCKED BY PRAMAN",
                "reason": reason,
                "threat_type": "UNAUTHORISED_SOURCE_CODE_EXPLOIT_ATTEMPT_DETECTED"
            }), 403
