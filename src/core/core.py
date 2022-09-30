from .handler import Handler
from .subscribe import Subscribe
import asyncio

class Core:
    def __init__(self, prefixes):
        handler = Handler()
        sub = Subscribe(prefixes, handler.dispatch)
        asyncio.run(sub.run())
        