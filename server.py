import hashlib
import hmac
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

SHARED_SECRET = B"my_private_signing_key_2026"
REQUEST_VALIDITY_WINDOW = 30 #signature validity is 30s

def verify_request_intergity():
    timestamp = request.headers.get("X-Timestamp")
    signature = request.headers.get("x-Signature")

    if not timestamp or not signature:
        return Flase, "Missing NTrust Headers (X-Timestamp / X-Signature)"