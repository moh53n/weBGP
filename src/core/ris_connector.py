import json
import websockets

class RIS:
    prefix = None
    ws_url = None
    handler = None
    def __init__(self, prefix, handler):
        self.prefix = prefix
        self.handler = handler
        self.ws_url = "wss://ris-live.ripe.net/v1/ws/?client=weBGP"

    async def subscribe(self, ws_server):
        params = {
            "prefix": self.prefix,
            "moreSpecific": True,
            "type": "UPDATE",
            "socketOptions": {
                "acknowledge": False    #TODO: Make sure the channel is opened
            }
        }
        async for ws in websockets.connect(self.ws_url):
            try:
                await ws.send(json.dumps({"type": "ris_subscribe", "data": params}))
                async for message in ws:
                    self.handle(message, ws_server)
            except Exception as e:
                print(f"Socket disconnected ({e}), reconnecting...")
                continue

    def handle(self, msg, ws_server):
        msg = json.loads(msg)
        if msg['type'] == 'ris_message':
            final_msg = {
                "peer": None,
                "announcements": None,
                "withdrawals": None,
                "timestamp": None
            }
            final_msg['peer'] = msg['data']['peer']
            if 'announcements' in msg['data'].keys():
                final_msg['announcements'] = []
                for ann in msg['data']['announcements']:
                    final_msg['announcements'].extend(ann['prefixes'])
            if 'withdrawals' in msg['data'].keys():
                final_msg['withdrawals'] = msg['data']['withdrawals'].copy()
            if 'timestamp' in msg['data'].keys():
                final_msg['timestamp'] = msg['data']["timestamp"]
            self.handler.dispatch(final_msg, ws_server)
