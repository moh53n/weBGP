from src.core.ris_handler import Handler
from src.core.ris_subscribe import Subscribe
import asyncio
import threading

class Core:
    def __init__(self, prefixes, ws_server):
        handler = Handler()
        sub = Subscribe(prefixes, handler, ws_server)
        thread = threading.Thread(target=asyncio.run, args=(sub.run(),))
        thread.start()
