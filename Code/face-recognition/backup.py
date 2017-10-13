import cv2
import sys
import numpy
import os

cascPath = '/home/pi//senior-design/face-recognition/haarcascade_frontalface_default.xml'
datasets = '/home/pi//senior-design/face-recognition/datasets'
detected = 0
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
video_capture = cv2.VideoCapture(0)
while True:
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
            detected+=1
            
        else:
            cv2.putText(frame, 'Not Recognized', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,2,(0, 255, 255))
    cv2.imshow('OpenCV', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #if detected==3:
     #   break

video_capture.release()
cv2.destroyAllWindows()
