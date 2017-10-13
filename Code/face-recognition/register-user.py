import cv2
import sys
import numpy
import os

cascPath = '/home/pi/sd/face-recognition/haarcascade_frontalface_default.xml'
datasets = '/home/pi/sd/face-recognition/datasets'
sub_data = raw_input("Input Name: ")#str(sys.argv[1])
passcode = raw_input("Input Keycode: ")#str(sys.argv[2])

path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
    os.mkdir(path)
(width, height) = (130, 100)

faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(1)

file_target = open("/home/pi/sd/face-recognition/passcodes/"+ sub_data + ".code", 'w')
file_target.truncate()
file_target.write(passcode)
file_target.close()

count = 1
while count < 31:
    (_, frame)= video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        cv2.imwrite('%s/%s.png' % (path,count), face_resize)
    count += 1
    print('%s.png' % (count))
    cv2.imshow('OpenCV', frame)
    key = cv2.waitKey(10)
    if key == 27:
            break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
