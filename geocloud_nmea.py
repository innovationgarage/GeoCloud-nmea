import socketserver
import socket
import ais.stream
import ais.compatibility.gpsd
import sys
import threading
import json
import queue
import time
import datetime

senders = set()

class TCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        
class Server(threading.Thread):
    def run(self):
        print("Server: Started: %s" % self._kwargs)
        Handler = self._kwargs["handler"]
        class Server(socketserver.BaseRequestHandler):
            def handle(self):
                print("Server: Connection request received")
                Handler(self.request)
        self.server = TCPServer((self._kwargs["host"], self._kwargs["port"]), Server)
        self.server.serve_forever()

class Connector(threading.Thread):
    def run(self):
        print("Connector: Started: %s" % self._kwargs)
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self._kwargs["host"], self._kwargs["port"]))
                print("Connector: Connected")
                self._kwargs["handler"](sock)
            finally:
                sock.close()
            time.sleep(1)

class ReceiveHandler(object):
    def __init__(self, conn):
        self.conn = conn.makefile("r")
        for msg in ais.stream.decode(self.conn, keep_nmea=True):
            msg = ais.compatibility.gpsd.mangle(msg)
            if "tagblock_timestamp" not in msg:
                msg["tagblock_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            msg["timestamp"] = msg["tagblock_timestamp"]
            for sender in senders:
                try:
                    sender.put(msg)
                except Exception as e:
                    print(e)
    
class SendHandler(object):
    def __init__(self, conn):
        self.conn = conn.makefile("w")
        self.queue = queue.Queue()
        try:
            senders.add(self)
            
            while True:
                msg = self.queue.get()
                json.dump(msg, self.conn)
                self.conn.write("\n")
                self.conn.flush()
        finally:
            senders.remove(self)

    def put(self, msg):
        self.queue.put(msg)
            
    def __hash__(self):
        return id(self)
        
if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        config = json.load(f)

    for connection in config["connections"]:
        handler = {"source": ReceiveHandler, "destination": SendHandler}[connection["direction"]]
        addr = connection["address"].split(":")
        assert addr[0] == "tcp"
        host = "0.0.0.0"
        port = 1024
        if len(addr) == 2:
            port = addr[1]
        if len(addr) == 3:
            host, port = addr[1:]
        port = int(port)
        connhandler = {"listen": Server, "connect": Connector}[connection["type"]]
        connhandler(kwargs={"host": host, "port": port, "handler": handler}).start()
