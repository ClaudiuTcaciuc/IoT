import json
import urllib3

if __name__ == '__main__':
    http = urllib3.PoolManager()
    while(True):
        msg = input()
        msg = msg.split(':')
        if msg[0] == 'T':
            try:
                val = float(msg[1].strip())
            except:
                print("Cannot convert to float")
                continue
            data = {'temperature':val}
            json_data = json.dumps(data).encode('utf-8')
            r = http.request('POST', 'http://192.168.1.12:8080/log',
                body = json_data, headers = {'Content-Type':'application/json'})
            print(str(r.status))
        else:
            print("Unrecognized message:", msg)