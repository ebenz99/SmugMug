# Hayden Riewe
# github.com/hriewe
# hrcyber.tech

import numpy as np
import cv2
import subprocess
import sys
import time
import os

# Set up variables
cap = cv2.VideoCapture(0)
lockCounter = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(os.getcwd()+"/recognizers/face-trainner.yml")

lockCounterv=0

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()
	
	# Convert frames to black and white image
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.imshow('frame',gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	# Draw rectangle on face, not necessary
	for (x,y,w,h) in faces:   
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)  
		roi_gray = gray[y:y+h, x:x+w]
		id_, conf = recognizer.predict(roi_gray)
		if conf>=45 and conf<=85:
			lockCounter=0
			break
		else:
			lockCounter+=1



	# Determine if face in in view, if not lock Mac
	#if len(faces) > 0:
	#	lockCounter = 0
	#else:
	#	lockCounter = lockCounter + 1

	# This value determines how many frames pass without a face before Mac locks
	print(lockCounter)
	if lockCounter >= 10:
		subprocess.call('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend',shell=True)
		sys.exit()
	
	# Display the resulting frame, used for testing
	cv2.imshow('LockAway', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break



# Clean up
cap.release()
cv2.destroyAllWindows()