import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)


def build_payload() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Container is running",
        "hostname": socket.gethostname(),
        "python_version": os.sys.version.split(" ")[0],
        "time_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
@app.get("/health")
def health() -> tuple[dict[str, str], int]:
    return jsonify(build_payload()), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Not found"}), 404


def main() -> None:
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8000"))
    print(f"Server started on http://{host}:{port}")
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
import json
import os
import socket
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


class ContainerTestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path not in ("/", "/health"):
            self.send_response(404)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode("utf-8"))
            return

        payload = {
            "status": "ok",
            "message": "Container is running",
            "hostname": socket.gethostname(),
            "python_version": os.sys.version.split(" ")[0],
            "time_utc": datetime.now(timezone.utc).isoformat(),
        }

        response = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer((host, port), ContainerTestHandler)
    print(f"Server started on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
