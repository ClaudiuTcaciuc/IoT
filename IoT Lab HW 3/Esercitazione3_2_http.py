import cherrypy
import json
import time

LOG = []
startTime = time.time()

class ProducerWebService(object):
    exposed = True
    def POST(self, *uri, **params):
        global LOG
        global startTime
        contentLenght = cherrypy.request.headers['Content-Length']
        if contentLenght:
            rawBody = cherrypy.request.body.read(int(contentLenght))
            jsonDict = json.loads(rawBody)
            responseDict = {
                "bn": "Yun",
                "e": []
            }

            if 'temperature' in jsonDict.keys():
                try:
                    responseDict['e'].append(
                        {
                            'e':'temperature',
                            't':int(time.time()-startTime),
                            'v':jsonDict['temperature'],
                            'u':'Cel'
                        }
                    )
                    LOG.append(responseDict)
                    print(LOG)
                    return json.dumps(responseDict)
                except:
                    raise cherrypy.HTTPError(404, "Bad Request: value is not a number")
            else:
                raise cherrypy.HTTPError(404, "Bad Request: URI is not correctly formatted")
        else:
            raise cherrypy.HTTPError(404, "Bad Request: URI is not correctly formatted")
    def GET(self, *uri, **params):
        global LOG
        if len(uri) == 0:
            finalPrintJson = json.dumps(LOG, indent=4)
            print(finalPrintJson)
            return "<pre>"+finalPrintJson+"</pre>"
        else:
            raise cherrypy.HTTPError(404, "Bad Request: Uri not corretly formatted")


if __name__ == '__main__': 
    conf = { 
    	'/': { 
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 
        } 
    }
    cherrypy.tree.mount(ProducerWebService(), '/log', conf)
    cherrypy.config.update({'server.socket_host': '192.168.1.12'})
    cherrypy.config.update({'server.socket_port': 8080})

    cherrypy.engine.start()
    cherrypy.engine.block()