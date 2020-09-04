import os

from PIL import Image
import io
import base64


from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.enums import PNReconnectionPolicy
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

ENTRY = "Earth"
CHANNEL = "awesomeChannel"

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-10b9f92d-a0e2-4d07-bef2-8b84aee0c2a3"
pnconfig.subscribe_key = "sub-c-12ea3aa6-ed25-11ea-a728-4ec3aefbf636"
pnconfig.uuid = "serverUUID-SUB"
pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR

pubnub = PubNub(pnconfig)


class MySubscribeCallback(SubscribeCallback):
  def presence(self, pubnub, event):
    print("[PRESENCE: {}]".format(event.event))
    print("uuid: {}, channel: {}".format(event.uuid, event.channel))

  def status(self, pubnub, status):
          
      if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
        print("PN Unexpected Disconnect")
        pubnub.reconnect()

      if status.category == PNStatusCategory.PNConnectedCategory:
        print("PN Connected")

      if status.category == PNStatusCategory.PNReconnectedCategory:
        print("PN Re-Connected")
        pubnub.subscribe().channels('devChannel').execute()

      if status.category == PNStatusCategory.PNDecryptionErrorCategory:
        print("PN Decryption Error")
  
    
  def message(self, pubnub, event):
    print("[MESSAGE received]")

    print("message : {}".format(event.message["message"]))

class HandleDisconnectsCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
              print("Fuck you")
            # internet got lost, do some magic and call reconnect when ready
              pubnub.reconnect()
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            # do some magic and call reconnect when ready
              pubnub.reconnect()
              print("Fuck you")

        else:
            print("Bitch im working")
 
    def presence(self, pubnub, presence):
        pass
 
    def message(self, pubnub, event):
        print("[MESSAGE received]")
        print("{} : {}".format(event.message["name"], event.message["message"]))
        s = event.message["message"]
        s = s[2:-1]
        f = io.BytesIO(base64.b64decode(s))
        pilimage = Image.open(f)
        pilimage.save("recovered.jpg")

    def signal(self, pubnub, signal):
        pass

disconnect_listener = HandleDisconnectsCallback()
 
pubnub.add_listener(disconnect_listener)


pubnub.subscribe().channels(CHANNEL).with_presence().execute()

print("***************************************************")
print("* Waiting for updates to The Guide about {}... *".format(ENTRY))
print("***************************************************")
