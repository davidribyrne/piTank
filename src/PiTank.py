import cherrypy
import RPi.GPIO as gpio
import os, os.path
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

FORWARD = 'FORWARD'
REVERSE = 'REVERSE'
STOP = 'STOP'

LEFT_MOTOR_PIN_A = 15
LEFT_MOTOR_PIN_B = 13
RIGHT_MOTOR_PIN_A = 16
RIGHT_MOTOR_PIN_B = 18

gpio.setmode(gpio.BOARD)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT)


cherrypy.config.update({'server.socket_port': 9000})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()



def leftMotor(direction):
    PIN_A = False
    PIN_B = False

    if direction == FORWARD:
        PIN_B = True
    elif direction == REVERSE:
        PIN_B = True

    gpio.output(LEFT_MOTOR_PIN_A, PIN_A)
    gpio.output(LEFT_MOTOR_PIN_B, PIN_B)

    
def rightMotor(direction):
    PIN_A = False
    PIN_B = False

    if direction == FORWARD:
        PIN_B = True
    elif direction == REVERSE:
        PIN_B = True

    gpio.output(RIGHT_MOTOR_PIN_A, PIN_A)
    gpio.output(RIGHT_MOTOR_PIN_B, PIN_B)
    


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
