import uuid
import json
import requests
import time

DEVICEID = str (uuid.uuid1())

class Client(object):
    def updateDevice(self):
        Device  = {
            "userID": DEVICEID,
            "name": "Temperature Sensor"
        }
        requests.post("http://192.168.1.12:8080/devices/subscription",data = json.dumps(Device))

if __name__ == '__main__':
    client = Client()
    while(True):
        client.updateDevice()
        time.sleep(15)