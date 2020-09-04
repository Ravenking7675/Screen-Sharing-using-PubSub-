import asyncio
import aiohttp
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

ENTRY = "Earth"
CHANNEL = "avinash"

pnconfig.publish_key = "pub-c-10b9f92d-a0e2-4d07-bef2-8b84aee0c2a3"
pnconfig.subscribe_key = "sub-c-12ea3aa6-ed25-11ea-a728-4ec3aefbf636"
pnconfig.uuid = "serverUUID-PUB"
pubnub = PubNubAsyncio(pnconfig)


async def main():
    def my_publish_callback(task):
        # Check whether request successfully completed or not
        exception = task.exception()
        if exception is None:
            envelope = task.result()
            print("[PUBLISH: sent]")
        
        else:
            print("[PUBLISH: fail]")
            print("error: %s" % exception)
            
    await asyncio.sleep(1)

    asyncio.ensure_future(pubnub.publish().channel('such_channel').message(['hello', 'there']).future()) \
        .add_done_callback(my_publish_callback)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.stop()