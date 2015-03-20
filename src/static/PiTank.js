//alert('loaded');
/*
var socket = new WebSocket("ws://127.0.0.1:9000/ws");


socket.onmessage = function(event)
{
	alert(event.data);
}

socket.onerror = function(event)
{
	alert(event.data);
}

socket.onopen = function(event)
{
	socket.send("test3");
}

socket.onclose = function(event)
{
	alert('Connection lost');
}

*/

  var nativeLogOutput = document.getElementById('native-hold');
  var kdLogOutput = document.getElementById('kd-hold');

  function log(outputEl, text) {
    outputEl.innerHTML += '<pre>' + text + '</pre>';
  }

  function clear (outputEl) {
    outputEl.innerHTML = '';
  }

var FORWARD = 'FORWARD';
var LEFT = 'LEFT';
var RIGHT = 'RIGHT';
var BACK = 'BACK';
var STOP = 'STOP';

var currentState = STOP;
function getState()
{
	var state = '';
	if (kd.UP.isDown())
	{
		state += FORWARD;
	}
	else if (kd.DOWN.isDown())
	{
		state += BACK;
	}

	if (kd.LEFT.isDown())
	{
		state += LEFT;
	}
	if (kd.RIGHT.isDown())
	{
		state += RIGHT;
	}
	if (state.length == 0)
	{
		state = STOP;
	}
	return state;
}

function handleState()
{
	var newState = getState();
	if (newState != currentState)
	{
		clear(kdLogOutput);
		log(kdLogOutput, newState);
		currentState = newState;
	}
}
  kd.UP.down(handleState);
  kd.DOWN.down(handleState);
  kd.LEFT.down(handleState);
  kd.RIGHT.down(handleState);
  
  kd.UP.up(handleState);
  kd.DOWN.up(handleState);
  kd.LEFT.up(handleState);
  kd.RIGHT.up(handleState);

  
  kd.run(function () {
    kd.tick();
  });
