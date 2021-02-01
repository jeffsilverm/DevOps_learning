#! /usr/bin/env python3
#
# This is from https://pythonspot.com/flask-hello-world/
from flask import Flask
import socket


# getaddrinfo retrurns a list with 3 elements: one for stream, which is what we
# want, one for datagrams (UDP), and one for raw sockets.
af, socktype, proto, canonname, sa = \
        socket.getaddrinfo(socket.gethostname(), port=80)[0]  # stream = TCP
assert socktype == socket.SocketKind.SOCK_STREAM, \
    f"socktype should be socket.SocketKind.SOCK_STREAM but is actually " \
    f"{str(socktype)}."
my_address = sa[0]


app = Flask(__name__)


@app.route("/")
def hello():
    global my_address
    return "Hello World! My address is " + my_address


if __name__ == "__main__":
    app.run()
