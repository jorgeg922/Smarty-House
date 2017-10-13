#!/usr/bin/python
import sys
import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "your host url"
rootCAPath = "path to cert root"
certificatePath = "path to cert pem"
privateKeyPath = "path to cert key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("tvInterface")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

def tv_remote_cmd(command_in):
        #command_in= raw_input("What command would you like to send?")
        if(command_in == "power"):
                print "powering on/off command sent"
                os.system("irsend SEND_ONCE SONY_TV KEY_POWER")
        elif(command_in == "volume up"):
                print "volume up command sent"
                os.system("irsend SEND_ONCE SONY_TV KEY_VOLUMEUP")
        elif(command_in == "volume down"):
                print "volume down command sent"
                os.system("irsend SEND_ONCE SONY_TV KEY_VOLUMEDOWN")
        elif(command_in == "channel down"):
                print "channel down command sent"
                os.system("irsend SEND_ONCE SONY_TV KEY_CHANNELDOWN")
        elif(command_in == "channel up"):
                print "channel up command sent"
                os.system("irsend SEND_ONCE SONY_TV KEY_CHANNELUP")
        else:
                print"wrong command, please try again"

def myMessage(client, userdate, msg): #defining method on_message
	if msg.topic == "/tvremote": 
		val = str(msg.payload)
		print "Received message " +val
		tv_remote_cmd(val)

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("/tvremote", 1, myMessage)

while True:
	pass
