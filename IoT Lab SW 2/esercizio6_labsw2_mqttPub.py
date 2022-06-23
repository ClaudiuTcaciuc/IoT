import uuid
import json
import time
import paho.mqtt.client as mqtt

DEVICEID = str(uuid.uuid1())


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect('iot.eclipse.org',1883)
    client.subscribe('/tiot/group21/catalog/devices/subscription')
    client.loop_start()
    while(True):
        Device = {
            "userID":DEVICEID,
            "name":"Temperature Sensor"
        }
        client.publish('/tiot/group21/catalog/devices/subscription', json.dumps(Device).encode('utf-8'))
        time.sleep(15)