import requests, json
import hashlib

import nfc
from nfc.clf import RemoteTarget

import time, threading


class Device:
    def __init__(self, username, password, host, nfc_port):
        self.username = username
        self.md5password = hashlib.md5(str(password).encode('utf-8')).hexdigest()
        self.host = host
        self.protocol = "http"
        self.idroom = None              # Authenticate first to get it
        
        self.nfc_port = nfc_port
        self.nfc_clf = nfc.ContactlessFrontend(self.nfc_port)
        self.nfc_thread_running = False


    # --- NFC READER ---

    def _nfcListenThread(self):
        while self.nfc_thread_running:
            time.sleep(3)
            tag = self.nfc_clf.connect(rdwr={'on-connect': lambda tag: False})
            try:
                idnfc = int(tag.ndef.records.pop().text)
                self.movement(idnfc)
            except Exception as e:
                print(e)

        self.nfc_clf.close()

    def startListen(self):
        self.nfc_thread_running = True
        listenThread = threading.Thread(target=self._nfcListenThread, args=())
        listenThread.start()

    def stopListen(self):
        self.nfc_thread_running = False


    # --- REQUESTS ---

    def _endpointBuilder(self, path):
        return "{protocol}://{host}{path}".format(
            protocol = self.protocol,
            host = self.host,
            path = path
        )


    def _responseHandler(self, response):
        code = response.status_code
        path = response.url
    
        if(code == 200):
            print("{path} - {code} - Success".format(path=path, code=code))
            return response.json()

        elif(code == 401):
            print("{path} - {code} - Authentication error".format(path=path, code=code))
            return False

        elif(code == 500):
            err_message = json.loads(response.text)["message"]
            print("{path} - {code} - {err_message}".format(path=path, code=code, err_message=err_message))
            return False


    def _request(self, method, path, data):
        method = method.lower()
        if(method == "post"):
            response = requests.post(self._endpointBuilder(path), data = data)
        
        return self._responseHandler(response)
        # elif(method == "get"):
        #     requests.get(self._endpointBuilder(path))


    def auth(self):
        method = "post"
        path = "/device/auth"
        data = {
            'username' : self.username,
            'password' : self.md5password
        }
        
        response = self._request(method, path, data)
        if(response != False):
            self.idroom = response['codroom']
        return response

    def movement(self, idnfc):
        method = "post"
        path = "/device/movement"
        data = {
            'idroom' : self.idroom,
            'idnfc' : idnfc
        }
        
        response = self._request(method, path, data)