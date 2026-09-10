#!/usr/bin/env python3
"""Minimal loopback Echo API used only by the transport PoC."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


MAX_BODY = 4096


class EchoHandler(BaseHTTPRequestHandler):
    allowed_origin = ""

    def log_message(self, format_string, *args):
        print(
            f"{self.command} path={self.path} "
            f"origin={self.headers.get('Origin', '-')} status={args[1]}",
            flush=True,
        )

    def _cors_headers(self):
        origin = self.headers.get("Origin")
        if origin and origin == self.allowed_origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        if self.path != "/echo":
            self._json(404, {"error": "not_found"})
            return
        self.send_response(204)
        self._cors_headers()
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Max-Age", "60")
        self.end_headers()

    def do_POST(self):
        if self.path != "/echo":
            self._json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._json(400, {"error": "invalid_length"})
            return
        if length < 0 or length > MAX_BODY:
            self._json(413, {"error": "body_too_large"})
            return
        try:
            request = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json(400, {"error": "invalid_json"})
            return
        text = request.get("text") if isinstance(request, dict) else None
        if not isinstance(text, str):
            self._json(400, {"error": "text_required"})
            return
        self._json(200, {"text": text})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", required=True)
    args = parser.parse_args()
    EchoHandler.allowed_origin = args.origin
    server = ThreadingHTTPServer(("127.0.0.1", 8765), EchoHandler)
    print(f"LISTEN 127.0.0.1:8765 origin={args.origin}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
