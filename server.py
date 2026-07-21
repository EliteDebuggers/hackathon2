import hashlib
import hmac
import time
from flask import Flask, request, jsonify

app = Flask(__name__)