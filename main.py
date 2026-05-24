import math
import os
import platform
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)


def build_health_payload() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Container is running",
        "hostname": socket.gethostname(),
        "python_version": os.sys.version.split(" ")[0],
        "time_utc": datetime.now(timezone.utc).isoformat(),
    }


def build_info_payload() -> dict[str, str]:
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "system": platform.system(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "time_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
@app.get("/health")
def health() -> tuple[dict[str, str], int]:
    return jsonify(build_health_payload()), 200


@app.get("/info")
def info() -> tuple[dict[str, str], int]:
    return jsonify(build_info_payload()), 200


@app.get("/percent/<a>/<b>")
def percent(a: str, b: str):
    try:
        a_value = float(a)
        b_value = float(b)
    except ValueError:
        return jsonify({"error": "a and b must be numeric values"}), 400

    result = (a_value / 100.0) * b_value
    if math.isfinite(result):
        return jsonify({"a": a_value, "b": b_value, "result": result}), 200
    return jsonify({"error": "result is not a finite number"}), 400


@app.get("/fact/<x>")
def factorial(x: str):
    try:
        x_value = int(x)
    except ValueError:
        return jsonify({"error": "x must be an integer"}), 400

    if x_value < 0:
        return jsonify({"error": "x must be greater than or equal to 0"}), 400

    return jsonify({"x": x_value, "result": math.factorial(x_value)}), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Not found"}), 404


def main() -> None:
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "5000"))
    print(f"Server started on http://{host}:{port}")
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
