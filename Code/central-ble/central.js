var noble = require('noble');
var awsIot = require('aws-iot-device-sdk');
var ServiceID = "13333333333333333333333333333337";
var CharacteristicID = "13333333333333333333333333330001";

var device = awsIot.device({
   host: 'agod1mle2ii87.iot.us-east-1.amazonaws.com',
   port: 8883,
   keyPath: 'cert/webapp.private.key',
  certPath: 'cert/webapp.cert.pem',
    caPath: 'cert/root-CA.crt',
  clientId: 'blemodule',
    region: 'iot.us-east-1' 
});

noble.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    noble.startScanning([ServiceID], false);
  }
  else {
    noble.stopScanning();
  }
})

device.on('connect', function(){
	device.subscribe('/moisture')
})

noble.on('disconnect', function(){
        process.exit(0);
})

noble.on('discover', function(peripheral) {
	noble.stopScanning();
	peripheral.connect(function(err) {
		peripheral.discoverServices([ServiceID], function(err, services) {
			var moistureService = services[0];
			moistureService.discoverCharacteristics([CharacteristicID], function(err, characteristics) {
				var dataCharacteristic = characteristics[0];
				dataCharacteristic.on('read', function(data, isNotification){
					var val = parseInt(data.toString('hex'), 16);
	//				console.log("This is val: " + val);
					device.publish("/moisture", val.toString());
				})
				dataCharacteristic.notify(true, function(error) {
	//				console.log('Moisture level notification on');
				});
			})
		})
	})
	peripheral.disconnect(function(error) {
	//	console.log('disconnected from peripheral: ' + peripheral.uuid);
		noble.startScanning([ServiceID], false);
	});
})
