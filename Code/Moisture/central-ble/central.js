var noble = require('noble');
var mqtt = require('mqtt');

var client = mqtt.connect({host: '10.113.59.43', port: 1883});

var ServiceID = "13333333333333333333333333333337";
var CharacteristicID = "13333333333333333333333333330001";

noble.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    noble.startScanning([ServiceID], false);
  }
  else {
    noble.stopScanning();
  }
})

client.on('connect', function(){
	client.subscribe('sensor/moisture')
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
					client.publish("/sensor/moisture", val.toString());
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
