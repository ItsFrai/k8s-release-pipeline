import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "service": "release-pipeline-demo",
        "version": os.getenv("APP_VERSION", "v1.0.0"),
        "environment": os.getenv("APP_ENV", "local")
    })

@app.route("/healthz")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)