from flask import Flask, jsonify
#!/usr/bin/env python3
"""
Flask app
"""

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello() -> str:
    """ Return json respomse"""
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
