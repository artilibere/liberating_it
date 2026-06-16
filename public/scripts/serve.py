#!/usr/bin/env python3
"""Local dev server: trailing-slash URLs and 301 away from index.html."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


class CleanURLHandler(SimpleHTTPRequestHandler):
    def _clean_path(self) -> str | None:
        path = urlsplit(self.path).path
        if path.endswith("/index.html"):
            return path[: -len("index.html")]
        if path.endswith("/index.htm"):
            return path[: -len("index.htm")] or "/"
        return None

    def do_GET(self) -> None:
        location = self._clean_path()
        if location is not None:
            self._redirect(location)
            return
        super().do_GET()

    def do_HEAD(self) -> None:
        location = self._clean_path()
        if location is not None:
            self._redirect(location)
            return
        super().do_HEAD()

    def _redirect(self, location: str) -> None:
        if not location.endswith("/"):
            location += "/"
        query = urlsplit(self.path).query
        if query:
            location = f"{location}?{query}"
        self.send_response(301)
        self.send_header("Location", location)
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        super().log_message(format, *args)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve liberating.it with clean URLs")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Site root (default: public/)",
    )
    args = parser.parse_args()
    root = args.directory.resolve()

    handler = partial(CleanURLHandler, directory=str(root))
    server = ThreadingHTTPServer(("", args.port), handler)
    print(f"Serving {root} at http://localhost:{args.port}/")
    print("Clean URLs: /structures/foo/ (redirects from .../index.html)")
    server.serve_forever()


if __name__ == "__main__":
    main()
