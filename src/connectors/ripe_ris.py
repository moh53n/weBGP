import json
import websockets

#TODO: Implement reconnection
class RIS:
    prefix = None
    ws_url = None
    dispatch = None
    def __init__(self, prefix, dispatch):
        self.prefix = prefix
        self.dispatch = dispatch
        self.ws_url = "wss://ris-live.ripe.net/v1/ws/?client=weBGP"

    async def subscribe(self):
        params = {
            "prefix": self.prefix,
            "moreSpecific": True,
            "type": "UPDATE",
            "socketOptions": {
                "acknowledge": False    #TODO: Make sure the channel is opened
            }
        }
        async with websockets.connect(self.ws_url) as ws:
            await ws.send(json.dumps({"type": "ris_subscribe", "data": params}))
            async for message in ws:
                self.handle(message)

    def handle(self, msg):
        msg = json.loads(msg)
        if msg['type'] == 'ris_message':
            final_msg = {
                "peer": None,
                "announcements": None,
                "withdrawals": None
            }
            final_msg['peer'] = msg['data']['peer']
            if 'announcements' in msg['data'].keys():
                for ann in msg['data']['announcements']:
                    final_msg['announcements'] = []
                    final_msg['announcements'].extend(ann['prefixes'])
            if 'withdrawals' in msg['data'].keys():
                final_msg['withdrawals'] = msg['data']['withdrawals'].copy()
            self.dispatch(final_msg)
