# PRAMAN: Zero-Trust Security Middleware

# Express/Flask Middelware ( Javascript/Python )

### Theme : 
Even if the attacker sees all backend source code logic, they cannot exploit dyanamic endpoints without valid signed runtime signatures.

### Features : 
* **True Plug n Play**: Secure your entire app with just 1 line of code.
* **Zero-Trust**: Endpoints are locked down cryptographically.
* **Tamper-Proof**: Uses HMAC-SHA256 based on time, method, path, and payload.
* **Replay Attack Defense**: 30-second strict signature validity window.

### How it works : 
Requires incoming client requests to include a short-lived HMAC signature computed using the timestamp and the payload hash.
Even if an attacker reads the source code and discovers unauthenticated API endpoints like `/api/v1/delete-user`, they cannot send raw POST/cURL requests without dynamically generating the correct runtime signature.

### How to Integrate (Plug & Play)
It automatically intercepts **all** incoming requests to your Flask app. You can easily whitelist specific public endpoints (like your landing page or health checks) that shouldn't require signatures.

```python
from flask import Flask
from praman import PramanMiddleware

app = Flask(__name__)

# That's it! Your entire app is now secured.
# By default, "/" and "/health" are whitelisted.
PramanMiddleware(app, secret_key="YOUR_SHARED_SECRET")
```

---

### Setup Guide:

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python3 server.py`

running `python3 client.py` (will succeed) and `python3 attacker.py` (will fail).

---

### Project structure
```text
.
├── praman.py
├── server.py
├── client.py
├── attacker.py
├── favicon/
├── README.md
├── requirements.txt
└── templates
    └── index.html
```
