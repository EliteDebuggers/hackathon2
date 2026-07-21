python script middelware in flask

# Express/Flask Middelware ( Javascript/Python )

### Theme : 
Even if the attacker sees all backend source code logic, they cannot exploit dyanamic endpoints without valid signed runtime signatures.

### Work : 
Plug n Play moddelware (100 line of code) for Express or Flask.

### How it works : 
Requires incomming client request to include a short lived HMAC signature computed using time + payload hash.
Even if attacker reads the sourcecode and discovers an unauthenticated API endpoints like /api/user/delete , they cannot send raw POST,curl requests without passing the runtime signature generation.

---

### Setup Guide:

`python3 -m venv .venv`

`source .venv/bin/activate`

`pip install -r requirements.txt`

`python3 server.py`

---

### Project structure

<pre>
.
├── attacher.py
├── client.py
├── favicon/
├── README.md
├── requirements.txt
├── server.py
└── templates
    └── index.html

3 directories, 14 files
</pre>
