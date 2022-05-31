import json
import cherrypy
import time

CONVERSIONS = []

def TempConverter(value, originalUnit, targetUnit):
    if originalUnit == targetUnit:
        return value
    if originalUnit == 'C':
        if targetUnit == 'K':
            return value + 273.15
        if targetUnit == 'F':
            return (value*1.8)+32
    elif originalUnit == 'K':
        if targetUnit == 'C':
            return value - 273.15
        if targetUnit == 'F':
            return ((value-273.15)*1.8)+32
    elif originalUnit == 'F':
        if targetUnit == 'K':
            return ((value-32)/1.8)+273.15
        if targetUnit == 'C':
            return (value-32)/1.8

class ProducerWebService(object):
    exposed = True

    def POST(self, *uri, **params):
        variousUnit = ['C', 'K', 'F']
        global CONVERSIONS
        contentLength = cherrypy.request.headers['Content-Length']
        if contentLength:
            rawBody = cherrypy.request.body.read(int(contentLength))
            jsonDict = json.loads(rawBody)
            if 'targetUnit' in jsonDict.keys() and 'originalUnit' in jsonDict.keys() and 'values' in jsonDict.keys():
                if jsonDict['targetUnit'] in variousUnit and jsonDict['originalUnit'] in variousUnit:
                    try:
                        jsonDict['timestamp'] = time.time()
                        jsonDict['convertedValue'] = []
                        for i in jsonDict['values']:
                            val = float(i)
                            jsonDict['convertedValue'].append(TempConverter(val, jsonDict['originalUnit'], jsonDict['targetUnit']))                    
                        CONVERSIONS.append(jsonDict)
                        print(CONVERSIONS)
                        return json.dumps(jsonDict)
                    except:
                        raise cherrypy.HTTPError(404, "Bad Request: value is not a number")
                else:
                    raise cherrypy.HTTPError(404, "Bad Request: URI is not correctly formatted")
            else:
                raise cherrypy.HTTPError(404, "Bad Request: URI is not correctly formatted")
        else:
            raise cherrypy.HTTPError(404, "Bad Request: URI is not correctly formatted")
if __name__ == '__main__': 
    conf = { 
    	'/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
        } 
    } 
    cherrypy.tree.mount(ProducerWebService(), '/converter', conf)

    cherrypy.config.update({'server.socket_host': '127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 8080})

    cherrypy.engine.start()
    cherrypy.engine.block()