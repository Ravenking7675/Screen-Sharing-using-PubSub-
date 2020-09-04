import asyncio
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub_asyncio import PubNubAsyncio

pnconfig = PNConfiguration()

ENTRY = "Earth"
CHANNEL = "avinash"

pnconfig.publish_key = "pub-c-10b9f92d-a0e2-4d07-bef2-8b84aee0c2a3"
pnconfig.subscribe_key = "sub-c-12ea3aa6-ed25-11ea-a728-4ec3aefbf636"
pnconfig.uuid = "serverUUID-SUB"
pubnub = PubNubAsyncio(pnconfig)


async def main():
    # def my_publish_callback(task):
    #     # Check whether request successfully completed or not
    #     exception = task.exception()
    #     if exception is None:
    #         envelope = task.result()
    #         pass  # Message successfully published to specified channel.
    #     else:
    #         pass  # Handle message publish error. Check 'category' property to find out possible issue
    #         # because of which request did fail.
    #         # Request can be resent using: [status retry];

    class MySubscribeCallback(SubscribeCallback):
        def presence(self, pubnub, presence):
            print("[PRESENCE: {}]".format(presence.event))
            print("uuid: {}, channel: {}".format(presence.uuid, presence.channel))

        def status(self, pubnub, status):
            if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                print("[STATUS: Unstable disconnection")

            elif status.category == PNStatusCategory.PNConnectedCategory:
                # Connect event. You can do stuff like publish, and know you'll get it.
                # Or just use the connected event to confirm you are subscribed for
                # UI / internal notifications, etc
                # asyncio.ensure_future(pubnub.publish()
                #                       .channel("awesomeChannel")
                #                       .message("hello!!").future())\
                #     .add_done_callback(my_publish_callback)
                print("[STATUS: PNConnectedCategory]")
                print("connected to channels: {}".format(event.affected_channels))
                
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # Happens as part of our regular operation. This event happens when
                # radio / connectivity is lost, then regained.
            elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
                pass
                # Handle message decryption error. Probably client configured to
                # encrypt messages and on live data feed it received plain text.

        def message(self, pubnub, message):
            # Handle new message stored in message.message
            print("[MESSAGE received]")

            # print(event.message['message'])
            if event.message["update"] == "42":
                print("The publisher has ended the session.")
                os._exit(0)
            else:
                print("{}: {}".format(event.message["entry"], event.message["update"]))
                print("Got message from {}".format(event.message["sender"]))

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(CHANNEL).execute()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.stop()