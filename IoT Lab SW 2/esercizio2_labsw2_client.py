import json
import requests

class Client(object):
    def handler(self, command):
        if command == "MQTTInfo":
            self.getMQTTInfo()
        if command == "Devices":
            self.getDevices()
        if command == "DeviceID":
            self.getDeviceID()
        if command == "Users":
            self.getUsers()
        if command == "UserID":
            self.getUserID()
    def getMQTTInfo():
        request = requests.get("http://192.168.1.12/catalog")
        print (json.dumps(request.json(), indent = 4))
    def getDevices():
        request = requests.get("http://192.168.1.12/devices/subscrition")
        print (json.dumps(request.json(), indent = 4))
    def getDeviceID():
        ID = input("Insert device ID:\n")
        request = requests.get("http://192.168.1.12/devices/subscription/{}".format(ID))
        print (json.dumps(request.json(), indent = 4))
    def getUsers():
        request = requests.get("http://192.168.1.12/users")
        print (json.dumps(request.json(), indent = 4))
    def getUserID():
        ID = input("Insert users ID:\n")
        request = requests.get("http://192.168.1.12/users/{}".format(ID))
        print (json.dumps(request.json(), indent = 4))

if __name__ == '__main__':
    client = Client()
    commandList = ['MQTTInfo', 'Devices', 'DeviceID', 'Users', 'UserID']
    while(True):
        command = ("Available command:\nMQTTInfo\nDevices\nDeviceID\nUsers\nUserID\nquit")
        if command == 'quit':
            break
        elif command in commandList:
            client.handler(command)
        else:
            print("Wrong command")
