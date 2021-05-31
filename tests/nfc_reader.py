import nfc
from nfc.clf import RemoteTarget
import time, threading

class Nfc:
    def __init__(self, port):
        self.port = port
        self.is_listening = False
        
        self.clf = nfc.ContactlessFrontend(self.port)

    def _nfcReadThread(self):
        while self.is_listening:
            time.sleep(3)
            tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
            print(tag.ndef.records)

    def startListen(self):
        self.is_listening = True
        listenThread = threading.Thread(target=self._nfcReadThread, args=())
        listenThread.start()

    def stopListen(self):
        if(self.is_listening):
            self.is_listening = False
