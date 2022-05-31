
import paho.mqtt.client as mqtt
import json
import time

MESSAGE = {
    "bn":"YunGroup21",
    "e":[]
}
MEASURE = {
    "n":"temperature",
    "u":"Cel",
    "t":0,
    "v":0.0
}

def on_message(client, userdata, message):
    topic = message.topic.split('/')
    msg = message.payload.decode('utf-8')
    if topic[-1] == 'command':
        try:
            msg = json.loads(msg)
            if "e" not in msg:
                return
            peripheral = msg["e"][0]["n"]
            value = msg["e"][0]["v"]
            if peripheral != 'led':
                return
            print("L:"+str(value))
        except Exception:
            print("E:3")

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('test.mosquitto.org', 1883)
    client.subscribe('/tiot/group21/command')
    client.loop_start()
    while(True):
        msg = input()
        msg = msg.split(':')
        if msg[0] == 'T':
            try:
                val = float(msg[1].strip())
            except:
                print("E:1")
                continue
            MEASURE["t"] = time.time()
            MEASURE["v"] = val
            MESSAGE["e"] = [MEASURE]
            json_data = json.dumps(MESSAGE).encode('utf-8')
            client.publish('/tiot/group21', json_data)
        else:
            print("E:2")