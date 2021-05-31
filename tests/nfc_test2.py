import nfc
from nfc.clf import RemoteTarget

clf = nfc.ContactlessFrontend('usb:001:008')

clf.connect(rdwr={'on-connect': lambda tag: False}):
