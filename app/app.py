from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import socket
import datetime

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return jsonify({
        "message": "CloudOps AI Monitor is running",
        "status": "success",
        "host": socket.gethostname()
    })

@app.route("/health")
def health():
    REQUEST_COUNT.inc()
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
