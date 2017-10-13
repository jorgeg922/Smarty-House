import time
import wiringpi
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "agod1mle2ii87.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "DoorLock.cert.pem"
privateKeyPath = "DoorLock.private.key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("cameraControl")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

pinx = 18
piny = 12

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(pinx, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(piny, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

positionx = 150 #centered
positiony = 150 #centered
wiringpi.pwmWrite(pinx, positionx)
#wiringpi.pwmWrite(piny, positiony)

def customCallback(client, userdata, message):
	global positionx
	global positiony
	#print("Topic: " + message.topic)
	#print("Message: " + message.payload)
	if(message.topic == "/camera"):
		if(message.payload == "left"):
			if positionx >= 250:
				print("limit")
			else:
				positionx = positionx + 20
				wiringpi.pwmWrite(pinx, positionx)
		elif(message.payload == "right"):
			if positionx <= 50:
				print("limit")
			else:
				positionx = positionx - 20
				wiringpi.pwmWrite(pinx, positionx)
		elif(message.payload == "up"):
			if positiony >= 250:
				print("limit")
			else:
				positiony = positiony + 20
				wiringpi.pwmWrite(piny, positiony)
		elif(message.payload == "down"):
			if positiony <= 50:
				print("limit")
			else:
				positiony = positiony - 20
				wiringpi.pwmWrite(piny, positiony)	
		elif(message.payload == "center"):
			positionx = 150
			positiony = 150
			wiringpi.pwmWrite(pinx, positionx)
			wiringpi.pwmWrite(piny, positionx)

			
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("/camera", 1, customCallback)

while True:
	pass
			
