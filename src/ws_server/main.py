import websockets
import asyncio

class WS_Main:
    def __init__(self):
        self.dispatch_sub_list = set()

    async def _register(self, websocket):
        self.dispatch_sub_list.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.dispatch_sub_list.remove(websocket)

    async def main(self):
        async with websockets.serve(self._register, "127.0.0.1", 8000):
            await asyncio.Future()

    def run_server(self):
        asyncio.run(self.main())

    def dispatch_submit_update(self, update):
        websockets.broadcast(self.dispatch_sub_list, update)
