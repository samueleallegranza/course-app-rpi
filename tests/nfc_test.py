import nfc
from nfc.clf import RemoteTarget

import threading, time


# target = clf.sense(RemoteTarget('106A'))
# print(target)
# tag = nfc.tag.activate(clf, target)
# print(tag)
# print(tag.ndef)

clf = nfc.ContactlessFrontend('usb')

def thread_function(name):
    print("thread - started")
    
    while stop!='exit':
        time.sleep(5)
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print(tag)
        print(tag.ndef.records)
    
    clf.close()


nfc_search = threading.Thread(target=thread_function, args=(1,))
nfc_search.start()

stop=""
while stop!='exit':
    stop = input()
