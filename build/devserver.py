"""Local dev server that mirrors this site's Vercel routing.

vercel.json sets cleanUrls + trailingSlash:false, so production serves
/home-cleaning from home-cleaning.html. Plain http.server would 404 on every
extensionless internal link, which would make local link-testing meaningless.
This also applies the redirects declared in vercel.json so they can be tested.

Usage: ./.venv/Scripts/python.exe build/devserver.py [port]
"""

import http.server
import json
import pathlib
import socketserver
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4599

config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
REDIRECTS = {r["source"]: (r["destination"], r.get("statusCode", 308))
             for r in config.get("redirects", [])}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def do_GET(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]

        if path in REDIRECTS:
            dest, code = REDIRECTS[path]
            self.send_response(code)
            self.send_header("Location", dest)
            self.end_headers()
            return

        # cleanUrls: /home-cleaning -> home-cleaning.html
        if path != "/" and not pathlib.Path(path).suffix:
            candidate = ROOT / (path.lstrip("/") + ".html")
            if candidate.is_file():
                self.path = path + ".html"

        return super().do_GET()

    def log_message(self, fmt, *args):
        status = args[1] if len(args) > 1 else ""
        if status not in ("200", "304"):
            sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Nacravo dev server (Vercel-style routing) on http://127.0.0.1:{PORT}")
        httpd.serve_forever()
