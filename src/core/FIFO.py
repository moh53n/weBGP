import queue

class FIFO:
    def __init__(self, ws):
        self.ws = ws
        self.queue = queue.Queue()

    def runner(self):
        while True:
            event = self.queue.get()
            self.ws.dispatch_submit_update(event)
    
    def add(self, msg): #TODO: We must get the raw data and process them here instead of msg
        self.queue.put(msg)
