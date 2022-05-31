import cherrypy
import json

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
    def GET (self, *uri, **params):
        variousUnit = ['C', 'K', 'F']
        if len(uri) == 0:
            if 'value' in params and 'originalUnit' in params and 'targetUnit' in params:
                if params['originalUnit'] in variousUnit and params['targetUnit'] in variousUnit:
                    try:
                        val = float(params['value'])
                        targetUnit = params['targetUnit']
                        originalUnit = params['originalUnit']
                        response = {
                            'targetUnit': targetUnit,
                            'originalUnit': originalUnit,
                            'value': val,
                            'convertedValue': TempConverter(val,originalUnit,targetUnit )
                        }
                        return json.dumps(response)
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