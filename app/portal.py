"""The orders portal: a small legacy web service.

On RHEL 7 it runs on Python 2.7 (/usr/bin/python2). RHEL 8 has no Python 2 by default, so this file
was ported to run on both, and the RHEL 8 hosts run it on Python 3. That's one of the real changes
an upgrade from 7 to 8 forces.
  GET /        a page saying which RHEL release served it
  GET /health  "ok", for the load balancer
"""
import sys

try:  # Python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:  # Python 2
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


def release():
    with open("/etc/redhat-release") as f:
        return f.read().split(" release ")[1].split(" ")[0]


class Portal(BaseHTTPRequestHandler):
    server_version = "portal"   # no software versions in the Server header
    sys_version = ""

    def do_GET(self):
        if self.path == "/health":
            body = "ok\n"
        else:
            body = "<h1>Orders portal</h1>\n<p>Served from RHEL %s on Python %d</p>\n" % (release(), sys.version_info[0])
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 80), Portal).serve_forever()
