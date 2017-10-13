from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import RPi.GPIO as GPIO

oldstatus = ""
def moveDoorLock(status):
    global oldstatus
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(18, 100)
    pwm.start(5)
    count = 0
    newstatus = status
    if newstatus == oldstatus:
	return
    while count < 1: 
	if status == "Lock":
		pwm.ChangeDutyCycle(2.5)
	elif status == "Unlock":
		pwm.ChangeDutyCycle(20.5)
	else:
		return
	time.sleep(0.45)
	count += 1
    oldstatus = status
    GPIO.cleanup() 
	
def customCallback(client, userdata, message):
	print("Topic: " + message.topic)
	print("Message: " + message.payload)
	if(message.topic == "/DoorLock"):
		if(message.payload == "1"):
			moveDoorLock("Lock")
		elif(message.payload == "0"):
			moveDoorLock("Unlock")

host = "agod1mle2ii87.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "DoorLock.cert.pem"
privateKeyPath = "DoorLock.private.key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("/DoorLock", 1, customCallback)
time.sleep(2)

while True:
	pass
