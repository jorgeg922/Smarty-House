import cv2
import sys
import numpy
import os
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "agod1mle2ii87.iot.us-east-1.amazonaws.com"
rootCAPath = "cert/root-CA.crt"
certificatePath = "cert/recognition.cert.pem"
privateKeyPath = "cert/recognition.private.key"

myAWSIoTMQTTClient = AWSIoTMQTTClient("basicRecognition")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)

cascPath = '/home/pi/sd/face-recognition/haarcascade_frontalface_default.xml'
datasets = '/home/pi/sd/face-recognition/datasets'
detected = 0
unknown = 0
print('Training...')

(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)
(images, labels) = [numpy.array(lis) for lis in [images, labels]]
model = cv2.createFisherFaceRecognizer()
model.train(images, labels)
print("Training Complete!")
faceCascade = cv2.CascadeClassifier(cascPath)

print("Waiting for signal")
def recognition():
    global detected
    global unknown
    global result
    detected = 0
    unknown = 0
    video_capture = cv2.VideoCapture(1)
    while (True):
        (_, frame)= video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 4)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 4)

            if prediction[1]<500:
                cv2.putText(frame,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,2,(0, 255, 255))
                print("Recognized: " + (names[prediction[0]]))
                result = str(names[prediction[0]])
                detected+=1
                
            else:
                cv2.putText(frame, 'Not Recognized', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,2,(0, 255, 255))
                print("unknown")
                unknown+=1
                
                
        #cv2.imshow('OpenCV', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("pressed q")
            return
        
        if detected == 3:
            myAWSIoTMQTTClient.publish("/interface", result, 1)
	    send_passcode(result)
            return
        
        if unknown == 15:
            myAWSIoTMQTTClient.publish("/interface", "unknown", 1)
            return

    video_capture.release()
    cv2.destroyAllWindows()
def send_passcode(user):
	file_target = open("/home/pi/sd/face-recognition/passcodes/"+ user + ".code", 'r')
	code = file_target.read()
	file_target.close()
	myAWSIoTMQTTClient.publish("/passcode", code, 1)

def customCallback(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    if( str(msg.payload) == "recognize" ):
        recognition()
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("/recognition", 1, customCallback)
time.sleep(2)

while True:
	pass
