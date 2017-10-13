var port = 3000
var express = require('express');
var path = require('path');
var mqtt = require('mqtt');

var io = require('socket.io').listen('1991');
var router = express.Router();
var app = express();
var awsIot = require('aws-iot-device-sdk');

var device = awsIot.device({
   host: 'url to host',
   port: 8883,
   keyPath: 'your cert key',
  certPath: 'your cert pem',
    caPath: 'cert/root-CA.crt',
  clientId: 'webapp',
    region: 'iot.us-east-1' 
});

app.use(express.static(path.join(__dirname + '')));

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, '/index.html'));
});

app.listen(port);

console.log("Now listening on port " + port);

io.sockets.on('connection', function (socket) {
    socket.on('subscribe', function (data) {
        console.log('Subscribing to '+data.topic);
        socket.join(data.topic);
        device.subscribe(data.topic);
    });
    socket.on('publish', function (data) {
        console.log('Publishing to '+data.topic);
        device.publish(data.topic,data.payload);
    });

	socket.on('/dimmer', function (val){
		device.publish("/dimmer",val);
	});
	socket.on('/tvremote', function (command){
		device.publish("/tvremote", command);
	});
	socket.on('/camera', function (command){
		device.publish("/camera", command);
	});
	socket.on('/alarm', function (command){
		device.publish("/alarm", command);
	});
	socket.on('/DoorLock', function (command){
		device.publish("/DoorLock", command);
	});
});
 
device.on('message', function (topic, payload, packet) {
    //console.log(topic+'='+payload);
    io.sockets.emit('mqtt',{'topic':String(topic),
                            'payload':String(payload)});
});

device.on('connect', () => {  
  console.log('client connected');
  device.subscribe('/moisture')
  device.subscribe('/temperature')
  device.subscribe('/humidity')
  device.subscribe('/dimmer')
  device.subscribe('/door')
  device.subscribe('/face')
  device.subscribe('/security')
  device.subscribe('/DoorLock')
  device.subscribe('/tvremote')
  device.subscribe('/camera')
  device.subscribe('/alarm')
  device.subscribe('/doorbell')
})
