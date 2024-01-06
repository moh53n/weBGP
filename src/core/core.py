from src.core.ris_handler import Handler
from src.core.ris_subscribe import Subscribe
import asyncio
import threading

class Core:
    def __init__(self, prefixes, fifo):
        handler = Handler()
        fifo_thread = threading.Thread(target=fifo.runner, args=())
        fifo_thread.start()
        sub = Subscribe(prefixes, handler, fifo)
        sub_thread = threading.Thread(target=asyncio.run, args=(sub.run(),))
        sub_thread.start()
