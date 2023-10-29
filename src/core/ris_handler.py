import time

#TODO: Probably we're going to have race conditions, fix the async thing by making sure where to wait
#TODO: Implement the queue time limit
#TODO: Store peer list in the queue
class Handler:

    offlines = None
    offline_queue = None
    online_queue = None
    num = 0
    def __init__(self):
        self.offlines = {}
        self.offline_queue = {}
        self.online_queue = {}

    def dispatch(self, msg):
        if msg['withdrawals']:
            for off in msg['withdrawals']:
                if off not in self.offlines.keys():
                    if off in self.offline_queue.keys():
                        self.offline_queue[off]['peers'] += 1
                        if self.offline_queue[off]['peers'] >= 40:    #TODO: Let the user set this
                            del(self.offline_queue[off])    #TODO: Possible race condition?
                            self.offlines[off] = int(time.time())
                            print(off, "OFFLINE")    #TODO: Report
                    else:
                        self.offline_queue[off] = {
                            "time": int(time.time()),
                            "peers": 1
                        }
        if msg['announcements']:
            for on in msg['announcements']:
                if on in self.offlines.keys():
                    if on in self.online_queue.keys():
                        self.online_queue[on]['peers'] += 1
                        if self.online_queue[on]['peers'] >= 40:    #TODO: Let the user set this
                            del(self.online_queue[on])    #TODO: Possible race condition?
                            del(self.offlines[on])
                            print(on, "ONLINE on", msg['peer'])    #TODO: Report
                    else:
                        self.online_queue[on] = {
                            "time": int(time.time()),
                            "peers": 1
                        }