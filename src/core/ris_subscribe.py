from src.core.ris_connector import RIS
import asyncio

#TODO: Check if every prefix is valid
#TODO: Support multiple connectors and let user select one in the config
#TODO: Confirm and handle the subscriptions
class Subscribe:

    subscribed = None

    def __init__(self, prefixes, handler):
        self.subscribed = {}
        if len(prefixes) > 8:
            print("Too many prefixes to subscribe, subscribing to 0.0.0.0/0 and filtering locally...")
            handler.set_large_prefixes(prefixes)
            prefix = "0.0.0.0/0"
            self.subscribed[prefix] = RIS(prefix, handler)
            print("Subscribed for", prefix)
        else:
            for prefix in prefixes:
                self.subscribed[prefix] = RIS(prefix, handler)
                print("Subscribed for", prefix)

    async def run(self):
        sub_job = []
        for prefix in self.subscribed.values():
            sub_job.append(prefix.subscribe())
        await asyncio.gather(*sub_job)
