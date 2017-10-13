from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO   #import the GPIO library
import time               #import the time library

class Buzzer(object):
 def __init__(self):
  GPIO.setmode(GPIO.BCM)  
  self.buzzer_pin = 21 #set to GPIO pin 5
  GPIO.setup(self.buzzer_pin, GPIO.IN)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  #print("buzzer ready")

 def __del__(self):
  class_name = self.__class__.__name__
  #print (class_name, "finished")

 def buzz(self,pitch, duration):   #create the function "buzz" and feed it the pitch and duration)
 
  if(pitch==0):
   time.sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave  
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):    #start a loop from 0 to the variable "cycles" calculated above
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

 def play(self, tune):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0

  #print("Playing tune ",tune)
  if(tune==1):
    pitches=[262,294,330,349,392,440,494,523, 587, 659,698,784,880,988,1047]
    duration=0.1
    for p in pitches:
      self.buzz(p, duration)  #feed the pitch and duration to the function, "buzz"
      time.sleep(duration *0.5)
    for p in reversed(pitches):
      self.buzz(p, duration)
      time.sleep(duration *0.5)

  elif(tune==2):
    pitches=[262,330,392,523,1047]
    duration=[0.2,0.2,0.2,0.2,0.2,0,5]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the function, "buzz"
      time.sleep(duration[x] *0.5)
      x+=1
  elif(tune==3):
    pitches=[392,294,0,392,294,0,392,0,392,392,392,0,1047,262]
    duration=[0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==4):
    pitches=[1047, 988,659]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==5):
    pitches=[1047, 988,523]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  GPIO.setup(self.buzzer_pin, GPIO.IN)

sent = 0
myAlarm = ""
myDoor = ""
myDoorLock = ""
myDoorBell = ""
triggered = False
def customCallback(client, userdata, message):
	global myAlarm
	global myDoor
	global myDoorLock
	global myDoorBell
	global triggered
	global sent
	#print("Topic: " + message.topic)
	#print("Message: " + message.payload)
	if(message.topic == "/door"):
		if(message.payload == "Open"):
			myDoor = "opened"
		elif(message.payload == "Closed"):
			myDoor = "closed"
	if(message.topic == "/DoorLock"):
		if(message.payload == "0"):
			myDoorLock = "unlocked"
		elif(message.payload == "1"):
			myDoorLock = "locked"
	if(message.topic == "/doorbell"):
		if(message.payload == "knocked"):
			myDoorBell = "knocked"
	if(message.topic == "/alarm"):
		if(message.payload == "armed"):
			myAlarm = "armed"
		elif(message.payload == "disarmed"):
			myAlarm = "disarmed"
			triggered = False
			sent = 0
			
host = "agod1mle2ii87.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "DoorLock.cert.pem"
privateKeyPath = "DoorLock.private.key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("alarmPub")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("/DoorLock", 1, customCallback)
myAWSIoTMQTTClient.subscribe("/alarm", 1, customCallback)
myAWSIoTMQTTClient.subscribe("/door", 1, customCallback)
myAWSIoTMQTTClient.subscribe("/doorbell", 1, customCallback)
time.sleep(2)
		
while True:
	if myAlarm == "armed":
		if myDoor == "opened" or myDoorLock == "unlocked":
			triggered = True
			if sent == 0:
				myAWSIoTMQTTClient.publish("/alarm", "Triggered", 1)
				sent = 1
		if triggered == True:
			buzzer = Buzzer()
			buzzer.play(4)
	if myDoorBell == "knocked":
		#print "doorbell"
		buzzer = Buzzer()
		buzzer.play(2)
		myDoorBell = ""
	