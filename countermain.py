# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 18:10:27 2017

@author: KARAN KHANNA
"""

import cv2
import numpy as np
import argparse
import serial
import time
from collections import deque
global tmt
PTS_LENGTH = int(input('Enter The number of Points='))
arduino = serial.Serial('COM7', 9600, timeout=.1)
i=0

while True:
	n=input()
	def nothing():
		pass

	ap = argparse.ArgumentParser()
	ap.add_argument("-v","--video",help = "path to the (optional) Video File")
	ap.add_argument("-b","--buffer",type = int ,default = 64,help = "max buffer size")
	args = vars(ap.parse_args())
	pts1= deque(maxlen = PTS_LENGTH)
	pts2 = deque(maxlen = PTS_LENGTH)
	pts3 = deque(maxlen = PTS_LENGTH)
	time.sleep(2)
	if not args.get("video",False):

		VidIn = cv2.VideoCapture(0)
	else:
		VidIn = cv2.VideoCapture(args["video"])


	while True:

		grabbed, frame = VidIn.read()
		if args.get("video") and not grabbed:
			break
			frame = cv2.resize(frame,(600,600),interpolation = cv2.INTER_CUBIC)



		Lower_Value_Red = np.array([131,75,104])
		Upper_Value_Red = np.array([255,255,255])
		Lower_Value_Green = np.array([9,139,227])
		Upper_Value_Green = np.array([255,255,255])
		Lower_Value_Blue = np.array([95,110,142])
		Upper_Value_Blue = np.array([146,255,255])
		tmt = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask1 = cv2.inRange(tmt, Lower_Value_Red,Upper_Value_Red)
		mask2 = cv2.inRange(tmt, Lower_Value_Green,Upper_Value_Green)
		mask3 = cv2.inRange(tmt, Lower_Value_Blue,Upper_Value_Blue)

		kernel = np.ones((8,8),np.uint8)

		mask1 = cv2.erode(mask1,kernel,iterations=2)
		mask1 = cv2.dilate(mask1,kernel,iterations = 2)
		mask1 = cv2.morphologyEx(mask1,cv2.MORPH_CLOSE,kernel)
		mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,kernel)

		mask2 = cv2.erode(mask2,kernel,iterations=2)
		mask2 = cv2.dilate(mask2,kernel,iterations = 2)
		mask2 = cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernel)
		mask2 = cv2.morphologyEx(mask2,cv2.MORPH_OPEN,kernel)

		mask3 = cv2.erode(mask3,kernel,iterations=2)
		mask3 = cv2.dilate(mask3,kernel,iterations = 2)
		mask3 = cv2.morphologyEx(mask3,cv2.MORPH_CLOSE,kernel)
		mask3 = cv2.morphologyEx(mask3,cv2.MORPH_OPEN,kernel)

		#result = cv2.bitwise_and(frame,frame,mask=mask)



		_,cnts1,_ = cv2.findContours(mask1.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		_,cnts2,_ = cv2.findContours(mask2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		_,cnts3,_ = cv2.findContours(mask3.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


		center1 = None
		center2 = None
		center3 = None

		if len(cnts1) > 0:
			c1 = max(cnts1,key=cv2.contourArea)
			x1,y1,w1,h1 = cv2.boundingRect(c1)
			M1 = cv2.moments(c1)
			center1 = (int(M1["m10"]/M1["m00"]),int(M1["m01"]/M1["m00"]))
			cv2.rectangle(frame,(int(x1),int(y1)),(int(x1+w1),int(y1+h1)),(255,0,0),2)
			temp = "red"
			arduino.write(temp.encode("utf-8"));
			#time.sleep(2)
			#t = arduino.readline().strip().decode("utf-8")
			#print(t)
			print("RED")
			break;
		if len(cnts2) > 0:
			c2 = max(cnts2,key=cv2.contourArea)
			x2,y2,w2,h2 = cv2.boundingRect(c2)
			M2 = cv2.moments(c2)
			center2 = (int(M2["m10"]/M2["m00"]),int(M2["m01"]/M2["m00"]))
			cv2.rectangle(frame,(int(x2),int(y2)),(int(x2+w2),int(y2+h2)),(0,255,0),2)
			temp = "green"
			arduino.write(temp.encode("utf-8"));
			#time.sleep(2)
			#t = arduino.readline().strip().decode("utf-8")
			print("GREEN")
			break;
		if len(cnts3) > 0:
			c3 = max(cnts3,key=cv2.contourArea)
			x3,y3,w3,h3 = cv2.boundingRect(c3)
			M3 = cv2.moments(c3)
			center3 = (int(M3["m10"]/M3["m00"]),int(M3["m01"]/M3["m00"]))
			temp = "blue"
			arduino.write(temp.encode("utf-8"));
			#time.sleep(1)
			#t = arduino.readline().strip().decode("utf-8")
			#print(t)
			print ("BLUE")
			break;

	# to check the centroid moment is used
			cv2.rectangle(frame,(int(x3),int(y3)),(int(x3+w3),int(y3+h3)),(0,0,255),2)

		print ("The Current center of the Object is =",center1,center2,center3)

		pts1.appendleft(center1)
		pts2.appendleft(center2)
		pts3.appendleft(center3)

		for i in range(1,len(pts1)):
			if pts1[i-2] is None or pts1[i] is None:
				continue

			thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
			cv2.line(frame,pts1[i-1],pts1[i],(0,255,0),thickness)

		for i in range(1,len(pts2)):
			if pts2[i-2] is None or pts2[i] is None:
				continue

			thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
			cv2.line(frame,pts2[i-1],pts2[i],(0,255,0),thickness)

		for i in range(1,len(pts3)):
			if pts3[i-2] is None or pts3[i] is None:
					  thickness = int(np.sqrt(args["buffer"]/float(i+1))* 2.5)
					  cv2.line(frame,pts3[i-1],pts3[i],(0,255,0),thickness)

		cv2.imshow('frame',frame)
		cv2.imshow('tmt',tmt)
		cv2.imshow('mask1',mask1)

		cv2.imshow('mask2',mask2)
		cv2.imshow('mask3',mask3)
		if cv2.waitKey(1) & 0xFF == ord('p'):
			break

	cv2.destroyAllWindows()
	VidIn.release()