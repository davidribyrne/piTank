#!/usr/bin/python
import json
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


class DeviceState:
    def __init__(self):
        self.leftMotor = STOP
        self.rightMotor = STOP
        


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
    
def processCommand(command):
    if command.leftMotor != state.leftMotor:
        leftMotor(command.leftMotor)
    if command.rightMotor != state.rightMotor:
        rightMotor(command.leftMotor)
        

class WebServer(object):
    @cherrypy.expose
    def index(self):
        return """
        <html><title>PiTank Main Menu</title>
        <body>
            <a href="keyboard">Keyboard interface</a><br/>
        </body></html>
        """

    @cherrypy.expose
    def keyboard(self):
        return """
        <html><title>PiTank Keyboard Interface</title>
        <body>
            <b>PiTank</b><br/>
            <div id="logStatus"></div><br/>
            <div id="logDebug"></div><br/>

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
        processCommand(json.load(message.data))
        #self.send(message.data, message.is_binary)

if __name__ == '__main__':
    gpio.setmode(gpio.BOARD)

    gpio.setup(LEFT_MOTOR_PIN_A, gpio.OUT)
    gpio.setup(LEFT_MOTOR_PIN_B, gpio.OUT)
    gpio.setup(RIGHT_MOTOR_PIN_A, gpio.OUT)
    gpio.setup(RIGHT_MOTOR_PIN_B, gpio.OUT)
    
    state = DeviceState()
    
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 80,
                            'log.access_file': './log/access',
                            'log.error_file': './log/error'
                            })
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    
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
    cherrypy.quickstart(WebServer(), '/', conf)
