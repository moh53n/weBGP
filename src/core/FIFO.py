import queue

class FIFO:
    def __init__(self, ws):
        self.ws = ws
        self.live_queue = queue.Queue()

    def live_runner(self):
        while True:
            event = self.live_queue.get()
            self.ws.dispatch_submit_live_update(event)
    
    def add_live_offline(self, prefix):
        self.live_queue.put({
            "prefix": prefix,
            "update": "offline"
        })

    def add_live_online(self, prefix, offline_for):
        self.live_queue.put({
            "prefix": prefix,
            "update": "online",
            "offline_for" : int(offline_for)
        })
