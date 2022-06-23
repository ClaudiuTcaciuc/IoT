import paho.mqtt.client as mqtt
import json
import time
import cherrypy
from threading import Thread, Lock

LOGDEVICES = []
startTime = time.time()
runThread = True
lockLOG = Lock()

def on_message(client, userdata, message):
    topic = message.topic.split('/')
    msg = message.payload.decode('utf-8')
    registerorUpdateDevice(msg)
   
def registerorUpdateDevice(msg):
    global LOGDEVICES
    global startTime
    jsonDict = json.loads(msg)
    try:
        lockLOG.acquire()
        deviceDict = {
            "ID" : jsonDict["userID"],
            "endPoint" : [],
            "availableRes": jsonDict["name"],
            "insertTime": int(time.time()-startTime)
        }
        for device in LOGDEVICES:
            if device["ID"] == jsonDict["userID"]:
                device["insertTime"] = int(time.time()-startTime)
                return
        print(deviceDict)
        LOGDEVICES.append(deviceDict)
        lockLOG.release()
        return
    except Exception as e:
        raise cherrypy.HTTPError(404, "Bad Request 1 Devices"+str(e))

def deleteOldElements ():
    while runThread:
        time.sleep(30)
        global LOGDEVICES
        toDelete = []
        lockLOG.acquire()
        for userID in LOGDEVICES:
            if int(time.time())-userID["insertTime"] > 60:
                toDelete.append(userID)
        for o in toDelete:
            LOGDEVICES.remove(o)
        lockLOG.release()

if __name__ == 'main':
    thread = Thread(target = deleteOldElements)
    thread.start()
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('iot.eclipse.org',1883)
    client.subscribe('/tiot/group21/catalog/devices/subscription')
    client.loop_start()
    while(True):
        msg = input()
        client.publish('/tiot/group21/catalog/devices/subscription/', msg)