'use strict';

/*
 * Constants defined here. Global variables are after functions & classes.
 */
var FORWARD = 'FORWARD';
var LEFT = 'LEFT';
var RIGHT = 'RIGHT';
var REVERSE = 'REVERSE';
var STOP = 'STOP';


function Device() 
{
	this.leftMotor = STOP;
	this.rightMotor = STOP;
	
	this.toString = function()
	{
		return 
			"leftMotor: " + this.leftMotor 
			+ "\nrightMotor: " + this.rightMotor;
	}
	
	this.equals = function(target)
	{
		return 
			this.leftMotor == target.leftMotor
			 && this.rightMotor == target.rightMotor;
	}
}

function ClientState()
{
	this.left = false;
	this.right = false;
	this.forward = false;
	this.reverse = false;
	this.shift = false;
	
	this.toString = function ()
	{
		return 
			"left: " + left + "\n" 
			+ "right: " + right + "\n" 
			+ "forward: " + forward + "\n" 
			+ "reverse: " + reverse + "\n" 
			+ "shift: " + shift + "\n";
	}
	
	this.equals = function(target)
	{
		return 
			this.left == target.left 
			&& this.right == target.right
			&& this.forward == target.forward  
			&& this.reverse == target.reverse
			&& this.shift == target.shift; 
	}
}

function getKeyState()
{
	var clientState = new ClientState();
	clientState.left = kd.LEFT.isDown();
	clientState.right = kd.RIGHT.isDown();
	clientState.forward = kd.UP.isDown();
	clientState.reverse = kd.DOWN.isDown();
	clientState.shift = kd.SHIFT.isDown();
	
	return clientState;
}


function createSocket()
{
	var host = window.location.host;
	var newSocket = new WebSocket("ws://" + host + "/ws");

	newSocket.onmessage = function(event)
	{
		eval(event.data);
	}

	newSocket.onerror = function(event)
	{
		alert("Error: " + event.data);
	}

	newSocket.onopen = function(event)
	{
		
	}

	newSocket.onclose = function(event)
	{
		alert('Connection lost. Refresh Page.');
	}
	
	return newSocket;
}


function log(outputEl, text) 
{
	outputEl.innerHTML += '<pre>' + text + '</pre>';
}

function clear (outputEl) 
{
	outputEl.innerHTML = '';
}


function generateCommand(clientState)
{
	var command = new Device();
	/*
	 * explicitly checking each state isn't the most efficient, but it's easier to read
	 * weird combinations like left and right both down will be caught by the first to match
	 * 
	 */
	if (clientState.left && ! clientState.shift)
	{
		command.rightMotor = FORWARD;
	}
	else if (clientState.left && clientState.shift)
	{
		command.leftMotor = REVERSE;
		command.rightMotor = FORWARD;
	}
	else if (clientState.right && !clientState.shift)
	{
		command.leftMotor = FORWARD;
	}
	else if (clientState.right && clientState.shift)
	{
		command.leftMotor = FORWARD;
		command.rightMotor = REVERSE;
	}
	else if (clientState.forward)
	{
		command.leftMotor = FORWARD;
		command.rightMotor = FORWARD;
	}
	else if (clientState.reverse)
	{
		command.leftMotor = REVERSE;
		command.rightMotor = REVERSE;
	}

	return state;
}

function sendCommand()
{
	
}

function handleKeyChange()
{
	if (socket.readyState == WebSocket.OPEN)
	{
		log (DEBUG, "Web socket open");
		var newClientState = getKeyState();
		// In future, get state from other sources?
		
		if (! newClientState.equals(currentClientState))
		{
			var command = generateCommand(newState);
			clear(KEY_STATUS);
			log(KEY_STATUS, newClientState.toString + "\n\n" + command.toString);
			socket.send(JSON.stringify(command));
			currentClientState = newClientState;
		}
	}
	else
	{
		log(DEBUG, "Web socket not open");
		clear(KEY_STATUS);
	}
}

function initializeKD()
{
	kd.UP.down(handleKeyChange);
	kd.DOWN.down(handleKeyChange);
	kd.LEFT.down(handleKeyChange);
	kd.RIGHT.down(handleKeyChange);
	kd.SHIFT.down(handleKeyChange);
	  
	kd.UP.up(handleKeyChange);
	kd.DOWN.up(handleKeyChange);
	kd.LEFT.up(handleKeyChange);
	kd.RIGHT.up(handleKeyChange);
	kd.SHIFT.up(handleKeyChange);
}

var DEBUG = document.getElementById('logDebug');
var KEY_STATUS = document.getElementById('logStatus');
var socket = createSocket();
var currentClientState = new State();

initializeKD();

  
kd.run(function () {
    kd.tick();
});
