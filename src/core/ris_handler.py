import time

#TODO: Maybe use FIFO and a thread here? Or use set for offlines and let the FIFO/classifier handler offline_for, etc
#TODO: Probably we're going to have race conditions, fix the async thing by making sure where to wait
#TODO: Yes we're having race condition and delays, must work with the timestamp of the RIS message
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
        self.large_prefixes = None

    def set_large_prefixes(self, prefixes):
        self.large_prefixes = set(prefixes)

    def dispatch(self, msg, fifo):    #TODO: Shitty code and flow, needs refactor and optimization
        if msg['withdrawals']:
            for off in msg['withdrawals']:
                if self.large_prefixes is not None and off not in self.large_prefixes:
                    continue
                if off not in self.offlines.keys():
                    if off in self.offline_queue.keys():
                        self.offline_queue[off]['peers'] += 1
                        if self.offline_queue[off]['peers'] >= 40:    #TODO: Let the user set this
                            self.offlines[off] = self.offline_queue[off]['time']
                            del(self.offline_queue[off])    #TODO: Possible race condition?
                            fifo.add(f'{{"prefix": {off}, "update": "offline"}}')
                    else:
                        self.offline_queue[off] = {
                            "time": int(msg['timestamp']),
                            "peers": 1
                        }
        if msg['announcements']:
            for on in msg['announcements']:
                if self.large_prefixes is not None and on not in self.large_prefixes:
                    continue
                if on in self.offlines.keys():
                    if on in self.online_queue.keys():
                        self.online_queue[on]['peers'] += 1
                        if self.online_queue[on]['peers'] >= 40:    #TODO: Let the user set this
                            offline_for = self.online_queue[on]["time"] - self.offlines[on]
                            del(self.online_queue[on])    #TODO: Possible race condition?
                            del(self.offlines[on])
                            fifo.add(f'{{"prefix": {on}, "update": "online", "offline_for": {offline_for}}}')
                    else:
                        self.online_queue[on] = {
                            "time": int(msg['timestamp']),
                            "peers": 1
                        }
                elif on in self.offline_queue.keys() and int(msg['timestamp']) > self.offline_queue[on]['time']:
                    if self.offline_queue[on]['peers'] <= 1:
                        del(self.offline_queue[on])
                    else:
                        self.offline_queue[on]['peers'] -= 1