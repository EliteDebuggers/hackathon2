# PRAMAN: Zero-Trust Security Middleware

🛡️ PRAMAN
Trust No Request. Verify Every Request.
PRAMAN is a plug-and-play Zero Trust middleware for Express and Flask that secures APIs by verifying every incoming request. Instead of relying on hidden source code, PRAMAN assumes attackers may already know your backend implementation and focuses on runtime verification.

---

### Features
Plug-and-Play Integration

* Designed for an excellent developer experience (DX).
* Simply import the middleware and add a single line to your existing Express or Flask application.
- No complex routing changes or endpoint refactoring required.

---

### Zero-Trust API Protection
PRAMAN follows the Zero Trust security model.

- Even if attackers know your backend source code, API routes, and application logic, they cannot successfully access protected endpoints without generating a valid signed request.

---

### Cryptographic Request Verification
Every request is protected using HMAC-SHA256 signatures.

The signature includes:
- Request body
- API path
- HTTP method
- Timestamp

If any part of the request is modified, the signature immediately becomes invalid and the request is rejected.

---

### ⏱ Replay Attack Prevention
Each request contains a timestamp.

- Requests are accepted only within a configurable validity window (for example, 30 seconds).
- Even if an attacker captures a valid request, replaying it after the allowed time window will automatically fail.

---

### Lightweight & Developer Friendly

- Plug-and-play installation
- Minimal configuration
- Express support
- Flask support
- Easy integration into existing projects

---

### Problem Statement
CYBER-02: The Attacker Has the Source Code

Modern applications should remain secure even when attackers know the implementation details.

PRAMAN ensures security through request verification instead of code secrecy.

---

### 💡 Philosophy
Trust No Request. Verify Every Request.
Don't call it Authentication Middleware , ->  Zero Trust Middleware


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
