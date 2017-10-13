#!/bin/bash
 
echo "Starting Door Lock...."
python ~/sd/door-lock/doorlook.py &
echo "Done"

echo "Starting BLE Central..."
sudo node ~/sd/central-ble/central.js &
echo "Done"

echo "Starting Face Recognition..."
/home/pi/.virtualenvs/cv/bin/python ~/sd/face-recognition/recognition.py &
echo "Done"

sleep 6
echo "Starting Interface...."
python ~/sd/interface/interface.py 
