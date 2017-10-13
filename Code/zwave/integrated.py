#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import time
import libopenzwave
from libopenzwave import PyManager
from openzwave.node import ZWaveNode
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "url to host"
rootCAPath = "your root path"
certificatePath = "certificate path"
privateKeyPath = "certificate key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("zwaveInterface")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

device="/dev/ttyACM0"
doorSensor="72057594093240320"
dimmer1 =  72057594076299265

options = ZWaveOption(device, \
  config_path="config", \
  user_path=".", cmd_line="")

options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level("None")
options.set_logging(False)
options.lock()

network = ZWaveNetwork(options, autostart=False)
network.start()

manager = libopenzwave.PyManager()
manager.create()

for i in range(0,2):
    if network.state>=network.STATE_READY:
        print("Network is ready")
        break
    else:
        time.sleep(1.0)

def sendDimmer(value):
	network.nodes[2].set_dimmer(dimmer1, value)
	
	
def customCallback(client, userdata, msg):
	if msg.topic == "/dimmer":
		value = int(str(msg.payload))
		sendDimmer(value)
	
def callback(args):
    if args:
        if 'valueId' in args:
            v = args['valueId']

            if str(v['id']) == doorSensor:
				if str(v['value']) == "True":
					myAWSIoTMQTTClient.publish("/door", "Open", 1)
				elif str(v['value']) == "False":
					myAWSIoTMQTTClient.publish("/door", "Closed", 1)

manager.addWatcher(callback)
manager.addDriver(device)

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("/door", 1, customCallback)
myAWSIoTMQTTClient.subscribe("/dimmer", 1, customCallback)
while True:
	pass
	
manager.removeWatcher(callback)
manager.removeDriver(device)
