from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

ENTRY = "Earth"
CHANNEL = "awesomeChannel"
the_update = None

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-10b9f92d-a0e2-4d07-bef2-8b84aee0c2a3"
pnconfig.subscribe_key = "sub-c-12ea3aa6-ed25-11ea-a728-4ec3aefbf636"
pnconfig.uuid = "serverUUID-PUB"

pubnub = PubNub(pnconfig)

print("*****************************************")
print("* Submit updates to The Guide for Earth *")
print("*     Enter 42 to exit this process     *")
print("*****************************************")

while True:
    print
    the_update = input("Enter a Message: ")
    the_message = {"name": "Raven", "message": the_update}
    # the_message = {"message": [{"value" : the_update}]}
    envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()

    if envelope.status.is_error():
        print("[PUBLISH: fail]")
        print("error: %s" % status.error)
    else:
        print("[PUBLISH: sent]")
        print("timetoken: %s" % envelope.result.timetoken)