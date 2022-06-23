import json
import cherrypy
import time
from threading import Thread, Lock

LOGDEVICES = []
LOGSERVICES = []
LOGUSERS = []

startTime = time.time()
runThread = True
lockLOG = Lock()

class timestamp(object):
    exposed = True
    def GET (self, *uri, **params):
        try:
            timeDict = {
                "insertTime": time.time()
            }
            return "<pre>"+json.dumps(timeDict, indent = 4)+"</pre>"
        except Exception as e:
            raise cherrypy.HTTPError(404, "Bad Request time"+ str(e))

class catalog (object):
    exposed = True
    def GET (self, *uri, **params):
        try:
            responseDict = {
                "subscription":{
                    "REST":{
                        "devices": "http://192.168.1.12/devices/subscrition",
                        "services": "http://192.168.1.12/services/subscrition",
                        "user": "http://192.168.1.12/users/subscrition"
                    },
                    "MQTT":{
                        "devices": {
                            "hostname": "iot.eclipse.org",
                            "port": "1883",
                            "topic": "tiot/group21/catalog/devices/subscription"
                        }
                    }
                }
            }
            return "<pre>"+json.dumps(responseDict,indent = 4)+"</pre>"
        except:
            raise cherrypy.HTTPError(404, "Bad Request")

class devices (object):
    exposed = True
    global LOGDEVICES
    global startTime
    def POST (self, *uri, **params):
        contentLength = cherrypy.request.headers['Content-Length']
        if contentLength:
            rawBody = cherrypy.request.body.read(int(contentLength))
            print(rawBody)
            jsonDict = json.loads(rawBody)
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
                LOGDEVICES.append(deviceDict)
                lockLOG.release()
                return json.dumps(deviceDict, indent = 4)
            except Exception as e:
                raise cherrypy.HTTPError(404, "Bad Request 1 Devices"+str(e))
        else:
            raise cherrypy.HTTPError(404, "Bad Request 2")
    
    def GET(self, *uri, **params):
        global LOGDEVICES
        if len(uri) == 0:
            logDevices = json.dumps(LOGDEVICES, indent = 4)
            print(logDevices)
            if len(params) == 0:
                return "<pre>"+logDevices+"</pre>"
            elif len(params) == 1:
                for deviceID in logDevices:
                    if deviceID["ID"] == params[0]:
                        return "<prev>"+deviceID+"</prev>"
        else:
            raise cherrypy.HTTPError(404, "Bad Request: Uri not corretly formatted")

class services (object):
    exposed = True
    global LOGSERVICES
    global startTime
    def POST (self, *uri, **params):
        contentLength = cherrypy.request.headers['Content-Length']
        if contentLength:
            rawBody = cherrypy.request.body.read(int(contentLength))
            jsonDict = json.loads(rawBody)
            try:
                servicesDict = {
                    "ID" : jsonDict["serviceID"],
                    "endPoint" : [],
                    "description": jsonDict["name"],
                    "insertTime": int(time.time()-startTime)
                }
                lockLOG.acquire()
                for service in LOGSERVICES:
                    if service["ID"] == jsonDict["serviceID"]:
                        service["insertTime"] = int(time.time()-startTime)
                        return
                LOGSERVICES.append(servicesDict)
                lockLOG.release()
                return json.dumps(servicesDict, indent = 4)
            except Exception as e:
                raise cherrypy.HTTPError(404, "Bad Request 1 Services"+str(e))
        else:
            raise cherrypy.HTTPError(404, "Bad Request 2")
    
    def GET(self, *uri, **params):
        global LOGSERVICES
        if len(uri) == 0:
            logServices = json.dumps(LOGSERVICES, indent = 4)
            print(logServices)
            if len(params) == 0:
                return "<pre>"+logServices+"</pre>"
            elif len(params) == 1:
                for ServiceID in logServices:
                    if ServiceID["ID"] == params[0]:
                        return "<prev>"+ServiceID+"</prev>"
        else:
            raise cherrypy.HTTPError(404, "Bad Request: Uri not corretly formatted")

class users(object):
    exposed = True
    def POST (self, *uri, **params):
        global LOGUSERS
        global startTime
        contentLength = cherrypy.request.headers['Content-Length']
        if contentLength:
            rawBody = cherrypy.request.body.read(int(contentLength))
            jsonDict = json.loads(rawBody)
            try:
                userDict = {
                    "ID": jsonDict["userID"],
                    #"ID": uuid.uuid4(),
                    "name": jsonDict["name"],
                    "surname": jsonDict["surname"],
                    "email": jsonDict["email"]
                }
                LOGUSERS.append(userDict)
                return "<pre>"+json.dumps(userDict, indent = 4)+"</pre>"
            except Exception as e:
                raise cherrypy.HTTPError(404, "Bad Request 1 User"+str(e))
        else:
            raise cherrypy.HTTPError(404, "Bad Request 2")
    def GET(self, *uri, **params):
        global LOGUSERS
        if len(uri) == 0:
            logUsers = json.dumps(LOGUSERS, indent = 4)
            print(logUsers)
            if len(params) == 0:
                return "<pre>"+logUsers+"</pre>"
            elif len(params) == 1:
                for UserID in logUsers:
                    if UserID["ID"] == params[0]:
                        return "<prev>"+UserID+"</prev>"
        else:
            raise cherrypy.HTTPError(404, "Bad Request: Uri not corretly formatted")

def deleteOldElements ():
    while runThread:
        time.sleep(30)
        global LOGSERVICES
        global LOGDEVICES
        toDelete = []
        lockLOG.acquire()
        for userID in LOGSERVICES:
            if int(time.time())-userID["insertTime"] > 60:
                toDelete.append(userID)
        for o in toDelete:
            LOGSERVICES.remove(o)
        toDelete.clear()
        for userID in LOGDEVICES:
            if int(time.time())-userID["insertTime"] > 60:
                toDelete.append(userID)
        for o in toDelete:
            LOGDEVICES.remove(o)
        lockLOG.release()


if __name__ == '__main__':
    thread = Thread(target = deleteOldElements)
    thread.start()
    conf = {
    	'/': { 
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
        }
    } 
    cherrypy.tree.mount(catalog(), '/catalog', conf)
    cherrypy.tree.mount(devices(), '/devices/subscription', conf)
    cherrypy.tree.mount(services(), '/services/subscription', conf)
    cherrypy.tree.mount(users(), '/users', conf)
    cherrypy.tree.mount(timestamp(), '/timestamp', conf)

    cherrypy.config.update({'server.socket_host': '192.168.1.12'})
    cherrypy.config.update({'server.socket_port': 8080})

    cherrypy.engine.start()
    cherrypy.engine.block()

    runThread = False
    thread.join()