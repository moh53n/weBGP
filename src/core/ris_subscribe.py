from src.core.ris_connector import RIS
import asyncio

#TODO: Check if every prefix is valid
#TODO: Support multiple connectors and let user select one in the config
#TODO: Confirm and handle the subscriptions
class Subscribe:

    subscribed = None

    def __init__(self, prefixes, dispatch):
        self.subscribed = {}
        for prefix in prefixes:
            self.subscribed[prefix] = RIS(prefix, dispatch)
            print("Subscribed for", prefix)

    async def run(self):
        sub_job = []
        for prefix in self.subscribed.values():
            sub_job.append(prefix.subscribe())
        await asyncio.gather(*sub_job)
