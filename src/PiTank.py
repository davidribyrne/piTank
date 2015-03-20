import cherrypy
import os, os.path
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

cherrypy.config.update({'server.socket_port': 9000})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class PiTank(object):
    @cherrypy.expose
    def index(self):
        return """
        <html><title>PiTank</title>
        <body>
            <b>PiTank</b><br/>
            <div id="kd-hold" class="log-output"></div>

            <script src="/static/keydrown.js"></script>
            <script src="/static/PiTank.js"></script>
        </body></html>
        """

    @cherrypy.expose
    def ws(self):
        # you can access the class instance through
        handler = cherrypy.request.ws_handler
        
class CommandSocket(WebSocket):
    def received_message(self, message):
        
        self.send(message.data, message.is_binary)

if __name__ == '__main__':
    conf = {
         '/ws': {
             'tools.websocket.on': True,
             'tools.websocket.handler_cls': CommandSocket
         },
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './static'
         }
     }
    cherrypy.quickstart(PiTank(), '/', conf)
