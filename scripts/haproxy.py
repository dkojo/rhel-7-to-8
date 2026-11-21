"""Send one command to HAProxy's runtime API and print the answer.

  python3 scripts/haproxy.py "set server web/web1 state maint"
  python3 scripts/haproxy.py status web1        (prints UP, DOWN, MAINT ...)
"""
import socket
import sys


def send(command):
    with socket.create_connection(("127.0.0.1", 9999), timeout=5) as s:
        s.sendall(command.encode() + b"\n")
        chunks = []
        while data := s.recv(65536):
            chunks.append(data)
    return b"".join(chunks).decode()


if sys.argv[1] == "status":
    for line in send("show stat").splitlines():
        cols = line.split(",")
        if len(cols) > 17 and cols[0] == "web" and cols[1] == sys.argv[2]:
            print(cols[17])
else:
    print(send(sys.argv[1]).strip())
