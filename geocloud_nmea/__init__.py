import socket_tentacles
import ais.stream
import ais.compatibility.gpsd
import sys
import threading
import json
import queue
import time
import datetime

senders = set()

class ReceiveHandler(socket_tentacles.ReceiveHandler):
    def handle(self):
        for msg in ais.stream.decode(self.file, keep_nmea=True):
            msg = ais.compatibility.gpsd.mangle(msg)
            if "tagblock_timestamp" not in msg:
                msg["tagblock_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            msg["timestamp"] = msg["tagblock_timestamp"]
            for sender in senders:
                try:
                    sender.put(msg)
                except Exception as e:
                    print(e)
    
class SendHandler(socket_tentacles.SendHandler):
    def handle(self):
        self.queue = queue.Queue()
        try:
            senders.add(self)
            
            while True:
                msg = self.queue.get()
                json.dump(msg, self.file)
                self.file.write("\n")
                self.file.flush()
        finally:
            senders.remove(self)

    def put(self, msg):
        self.queue.put(msg)
            
    def __hash__(self):
        return id(self)
        
def main(*arg, **kw):
    with open(sys.argv[1]) as f:
        config = json.load(f)

    socket_tentacles.run(config, {"source": ReceiveHandler, "destination": SendHandler})

if __name__ == "__main__":
    main()
