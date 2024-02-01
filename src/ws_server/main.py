import websockets
import asyncio
import json

#TODO: Maybe use a more standard structure, make param a dict (params), etc?
#TODO: Fix param texts, even I can't understand them
#TODO: Maybe use a subscribe command, in case of we need other commands too?
class WS_Main:
    def __init__(self):
        self.live_dispatch_sub_list = set()
        self.offs_dispatch_sub_lists = {
            1: set(),
            5: set(),
            15: set(),
            60: set(),
            180: set(),
            360: set(),
            1440: set()
        }

    async def parse_sub_type(self, msg, websocket):
        msg = json.loads(msg)
        try:
            if msg["channel"] == "live":
                self.live_dispatch_sub_list.add(websocket)
                await websocket.send(json.dumps({
                    "type": "internal",
                    "status": "ok",
                    "param": "subscribed to channel live"
                }))
                return self.live_dispatch_sub_list
            elif msg["channel"] == "offlines":
                if "param" not in msg.keys():
                    await websocket.send(json.dumps({
                        "type": "internal",
                        "status": "error",
                        "param": "No param: No time selected, supported times are 1, 5, 15, 60, 180, 360, 1440"
                    }))
                    await websocket.close(4000)
                    return False
                if not int(msg["param"]) in [1, 5, 15, 60, 180, 360, 1440]:
                    await websocket.send(json.dumps({
                        "type": "internal",
                        "status": "error",
                        "param": "Bad param: Wrong time channel selected, supported times are 1, 5, 15, 60, 180, 360, 1440"
                    }))
                    await websocket.close(4000)
                    return False
                self.offs_dispatch_sub_lists[int(msg["param"])].add(websocket)
                await websocket.send(json.dumps({
                    "type": "internal",
                    "status": "ok",
                    "param": f"subscribed to channel offlines-{msg['param']}"
                }))
                return self.offs_dispatch_sub_lists[int(msg["param"])]
            else:
                await websocket.send(json.dumps({
                    "type": "internal",
                    "status": "error",
                    "param": "Wrong channel selected, available channels are \"live\" and \"offlines\""
                }))
                await websocket.close(4000)
                return False
        except Exception as e:
            print(e) #TODO
            return False

    async def _register(self, websocket):
        sub_type = await websocket.recv()
        sub_list = await self.parse_sub_type(sub_type, websocket)
        if sub_list:
            try:
                await websocket.wait_closed()
            finally:
                sub_list.remove(websocket)

    async def main(self):
        async with websockets.serve(self._register, "127.0.0.1", 8000):
            await asyncio.Future()

    def run_server(self):
        asyncio.run(self.main())

    def dispatch_submit_update(self, update):
        websockets.broadcast(self.live_dispatch_sub_list, update)
