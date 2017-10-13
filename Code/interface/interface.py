from Tkinter import *
import tkFont
import os
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "agod1mle2ii87.iot.us-east-1.amazonaws.com"
rootCAPath = "cert/root-CA.crt"
certificatePath = "cert/interface.cert.pem"
privateKeyPath = "cert/interface.private.key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("basicInterface")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

#Variables
code = ""
code_display = ""
recieved_code = ""
last_messege = ""

win = Tk()
win.configure(background = "#123456")

#Full Screen
win.overrideredirect(True)
win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))
win.focus_set()
win.bind("<Escape>", lambda e: win.quit())
#End of full screen

myFont = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')
myFont2 = tkFont.Font(family = 'Helvetica', size = 16, weight = 'bold')
myFont3 = tkFont.Font(family = 'Helvetica', size = 20, weight = 'bold')

homeStatus = Label(win, font = myFont2, fg="#FFF", bg="#123456", text="Door Status:")
textCode = Label(win, font = myFont2, fg="#FFF", bg="#123456", text="Code: ")
textStatus = Label(win, font = myFont3, fg="#FFF", bg="#123456", text="Locked")
textUser = Label(win, font = myFont, fg="#FFF", bg="#123456", text="")
last_textstatus = "Locked"

def customCallback(client, userdata, msg):
    global recieved_code
    global last_messege
    global last_textstatus

    #print(msg.topic + " " + str(msg.payload))
    if(msg.topic == "/interface"):
		textUser = Label(win, font = myFont, fg="#123456", bg="#123456", text = last_messege)
		textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)
		if(str(msg.payload) == "unknown"):
			messege = "User not recognized!"
			last_messege = messege
			textUser = Label(win, font = myFont, fg="#FFF", bg="#123456", text = messege)
			textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)
		else:
			messege = "Hello " + str(msg.payload) + ", enter your code!"
			last_messege = messege
			textUser = Label(win, font = myFont, fg="#FFF", bg="#123456", text = messege)
			textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)
		
    if(msg.topic == "/passcode"):
		recieved_code = str(msg.payload)

    if(msg.topic == "/DoorLock"):
		if str(msg.payload) == "1":
			msg.payload = "Locked"
		elif str(msg.payload) == "0":
			msg.payload = "Unlocked"
			
		textStatus = Label(win, font = myFont3, fg="#123456", bg="#123456", text=last_textstatus)
		textStatus.grid(row = 4, column = 8)
		textStatus = Label(win, font = myFont3, fg="#FFF", bg="#123456", text=str(msg.payload))
		textStatus.grid(row = 4, column = 8)
		last_textstatus = str(msg.payload)

myAWSIoTMQTTClient.connect()
#print("connected")
myAWSIoTMQTTClient.subscribe("/DoorLock", 1, customCallback)
myAWSIoTMQTTClient.subscribe("/interface", 1, customCallback)
myAWSIoTMQTTClient.subscribe("/passcode", 1, customCallback)
myAWSIoTMQTTClient.subscribe("/doorbell", 1, customCallback)

def scanFace():
    global last_messege
    #print("Scan face button pressed")
    #os.system("/home/pi/.virtualenvs/cv/bin/python ~/senior-design/face-recognition/recognition.py")
    myAWSIoTMQTTClient.publish("/recognition", "recognize", 1)
    textUser = Label(win, font = myFont, fg="#123456", bg="#123456", text = last_messege)
    textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)
    messege = "Starting Face Recognition..."
    last_messege = messege
    textUser = Label(win, font = myFont, fg="#FFF", bg="#123456", text = messege)
    textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)

def doorBell():
	global last_textStatus
	#print("Door bell button pressed")
	myAWSIoTMQTTClient.publish("/doorbell", "knocked", 1)
	textStatus = Label(win, font = myFont3, fg="#123456", bg="#123456", text=last_textStatus)
	textStatus.grid(row = 4, column = 8)
	textStatus = Label(win, font = myFont3, fg="#FFF", bg="#123456", text="Knocked!")
	textStatus.grid(row = 4, column = 8)

def keypad(value):
    #print("keypad button: " + str(value))
    global code
    global code_display
    
    if value == 10:
		code = ""
		code_display = ""
		hidden_code = Label(win, font = myFont3, fg="#FFF", bg="#123456", text="          ")
		hidden_code.grid(padx = 5, pady = 11, row = 8, column = 8)

    elif value == 11:
		#print("Code: " + str(code))
		if str(code) == "":
			validatecode("*")
		else:	
			validatecode(str(code))
		code = ""
		code_display = ""
		hidden_code = Label(win, font = myFont3, fg="#FFF", bg="#123456", text="          ")
		hidden_code.grid(padx = 5, pady = 11, row = 8, column = 8)
    else:
    	code = code + str(value)
	code_display = code_display + ""
	hidden_code = Label(win, font = myFont3, fg="#FFF", bg="#123456", text=code_display)
	hidden_code.grid(padx = 5, pady = 11, row = 8, column = 8)
	
def validatecode(enteredcode):
	global recieved_code
	global last_messege
	textUser = Label(win, font = myFont, fg="#123456", bg="#123456", text = last_messege)
	textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)
	if(enteredcode == recieved_code):
		#print("Code matches!")
		messege = "Access Granted!"
		myAWSIoTMQTTClient.publish("/DoorLock", "0", 0)
		myAWSIoTMQTTClient.publish("/alarm", "disarmed", 1)
		last_messege = messege
		textUser = Label(win, font = myFont, fg="#FFF", bg="#123456", text = messege)
		textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)
	else:
		#print("code does not match")
		messege = "Access Denied!"
		last_messege = messege
		textUser = Label(win, font = myFont, fg="#FFF", bg="#123456", text = messege)
		textUser.grid(padx = 10, pady = 10, row = 6, column = 7, columnspan = 2)
        

win.title("Smarty House Security Authenitication")
win.geometry("800x480")


exitButton = Button(win, text = "Door Bell", font = myFont, command = doorBell, height = 3, width = 30)
#exitButton.pack(side = BOTTOM)
exitButton.grid(columnspan = 4, row = 1, column = 7)
scanFaceButton = Button(win, text = "Face Recognition", font = myFont, command = scanFace, height = 3, width = 30)
#scanFaceButton.pack()
scanFaceButton.grid(padx = 30, pady = 30, columnspan = 6, row = 1, column = 1)


number1 = Button(win, comman=lambda: keypad(1), text = "1", font = myFont, width = 6, height = 2)
number2 = Button(win, comman=lambda: keypad(2), text = "2", font = myFont, width = 6, height = 2)
number3 = Button(win, comman=lambda: keypad(3), text = "3", font = myFont, width = 6, height = 2)
number4 = Button(win, comman=lambda: keypad(4), text = "4", font = myFont, width = 6, height = 2)
number5 = Button(win, comman=lambda: keypad(5), text = "5", font = myFont, width = 6, height = 2)
number6 = Button(win, comman=lambda: keypad(6), text = "6", font = myFont, width = 6, height = 2)
number7 = Button(win, comman=lambda: keypad(7), text = "7", font = myFont, width = 6, height = 2)
number8 = Button(win, comman=lambda: keypad(8), text = "8", font = myFont, width = 6, height = 2)
number9 = Button(win, comman=lambda: keypad(9), text = "9", font = myFont, width = 6, height = 2)
clr = Button(win, comman=lambda: keypad(10),text = "CLR", font = myFont, width = 6, height = 2)
ent = Button(win, comman=lambda: keypad(11), text = "ENT", font = myFont, width = 6, height = 2)
number0 = Button(win, comman=lambda: keypad(0), text = "0", font = myFont, width = 6, height = 2)

number7.grid(padx = 10, pady = 10, row = 4, column = 3)
number8.grid(padx = 10, pady = 10, row = 4, column = 4)
number9.grid(padx = 10, pady = 10, row = 4, column = 5)
number4.grid(padx = 10, pady = 10, row = 6, column = 3)
number5.grid(padx = 10, pady = 10, row = 6, column = 4)
number6.grid(padx = 10, pady = 10, row = 6, column = 5)
number1.grid(padx = 10, pady = 10, row = 8, column = 3)
number2.grid(padx = 10, pady = 10, row = 8, column = 4)
number3.grid(padx = 10, pady = 10, row = 8, column = 5)
clr.grid(padx = 10, pady = 10, row = 10, column = 3)
number0.grid(padx = 10, pady = 10, row = 10, column = 4)
ent.grid(padx = 10, pady = 10, row = 10, column = 5)

homeStatus.grid(padx = 10, pady = 10, row = 4, column = 7)
textStatus.grid(padx = 10, pady = 10, row = 4, column = 8)
textCode.grid(padx = 10, pady = 10, row = 8, column = 7)
#textUnlock.grid(padx = 10, pady = 10, row = 4, column = 8)

mainloop()
