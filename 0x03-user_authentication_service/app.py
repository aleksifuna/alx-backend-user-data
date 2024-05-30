#!/usr/bin/env python3
"""
Flask app configuration module
"""

from flask import Flask, jsonify
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def home():
    """Returns a json payload for home route
    """
    return jsonify({
        "message": "Bienvenue"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
