//var mqtt = require('mqtt')
//var client = mqtt.connect({host:'10.113.46.250',port:1883});
var sensorLib = require('node-dht-sensor');
var awsIot = require('aws-iot-device-sdk');

var device = awsIot.device({
   host: 'url to host',
   port: 8883,
   keyPath: 'cert/tvpi.private.key',
  certPath: 'cert/tvpi.cert.pem',
    caPath: 'cert/root-CA.crt',
  clientId: 'tmp-hum',
    region: 'iot.us-east-1' 
});

function read_tmp(){
	var readout = sensorLib.read();
	var celc = readout.temperature;
	//should be +32 but due to low resistor,throws the valye 10 deg higher
	var faren = Math.round((celc* 1.8)+22)
	var tmp = faren.toString(); 
	return tmp;
}
function read_hum(){
	var readout = sensorLib.read();
	var hum = readout.humidity.toString();
	return hum;
}
function doSetInterval(){
	var x = 1
	setInterval(function(){
	device.publish('/temperature', read_tmp())
	//console.log('temp sent')
	device.publish('/humidity', read_hum())
	//console.log('hum sent')
	console.log('Data Sent! Iteration: '+ x);
	x++
	},30000);
}
if(sensorLib.initialize(11,4)){
	device.on('connect', function myFunction(){
		device.subscribe('/temperature')
		device.subscribe('/humidity')
		for(var i = 1;i<=1; ++i){
		doSetInterval();
		}			
	})
}
else{
	console.warn('Failed to intialize sensor');
}
