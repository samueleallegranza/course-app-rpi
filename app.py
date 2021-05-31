# import requests, json
# import hashlib

# def endpoint(path):
#     global apiHost
#     return "{protocol}://{host}{path}".format(
#         protocol = "http",
#         host = apiHost,
#         path = path
#     )


# # Collect informations about API and client
# with open('./config.json') as f:
#     config = json.load(f)
#     apiHost = "{ip}:{port}".format(ip=config["api_ip"], port=config["api_port"])
#     username = config["username"]
#     password = config["password"]
#     password_MD5 = hashlib.md5(str(password).encode('utf-8')).hexdigest()



# try:
    
#     # Authenticate with API
#     requests.post(endpoint("/device/auth"), data={
#         'username' : username,
#         'password' : password_MD5
#     });

#     #

# except Exception as e:
#     print(e)

import json
from device import Device
from sys import exit
import time

# Collect informations about API and client
with open('./config.json') as f:
    config = json.load(f)
    apiHost = "{ip}:{port}".format(ip=config["api_ip"], port=config["api_port"])
    username = config["username"]
    password = config["password"]
    nfcPort = config["nfc_port"]

dev = Device(username, password, apiHost, nfcPort)

# Authentication
response = dev.auth()
if(response == False):
    exit() # Wrong credentials

print("Authenticated! Room ID associated: {}".format(response["codroom"]))

dev.startListen()

print("waiting")
