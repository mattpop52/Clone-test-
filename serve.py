#!/usr/bin/env python3
"""Serve the cloned site locally.

The clone uses root-relative URLs (/wp-content/..., /services/branding/), so it
must be served over HTTP rather than opened via file://.

    python3 serve.py [port]        # default 8000
"""
import functools
import http.server
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".webp": "image/webp",
        ".avif": "image/avif",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".svg": "image/svg+xml",
    }

    def log_message(self, fmt, *args):  # quieter output
        if not args or not str(args[1]).startswith("2"):
            super().log_message(fmt, *args)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(Handler, directory=ROOT)
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Serving {ROOT} at http://127.0.0.1:{port}/  (Ctrl-C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
