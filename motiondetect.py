from pyimagesearch import *
from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import warnings
import datetime
import imutils
import json
import time
import cv2
import os
import numpy as np
import glob
import dropbox as dbx
import RPi.GPIO as GPIO
import sys

def main():
	break_script = False
	# filter warnings, load the configuration and initialize the Dropbox
	warnings.filterwarnings("ignore")

	#setup gpio
	def power_button_pressed(channel):
		break_script = True
		GPIO.remove_event_detect(17)
	GPIO.setmode(GPIO.BCM)
	# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
	# Both ports are wired to connect to GND on button press.
	# So we'll be setting up falling edge detection for both
	GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	#define mode number by push button gpio pins or flags or something
	# when a falling edge is detected on port 17, regardless of whatever
	# else is happening in the program, the function mode_button_pressed will be run
	GPIO.add_event_detect(17, GPIO.FALLING, callback=power_button_pressed, bouncetime=300)
	#dropbox:
	with open("permissions.json") as f:
		data = json.load(f)
	client = dbx.Dropbox(data['db-token'])

	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	#default 640x480 - decrease to go faster
	#motion-detect camera resolution
	camera.resolution = (640,480)
	rawCapture = PiRGBArray(camera, size=(640,480))

	# allow the camera to warmup, then initialize the average frame, last
	# uploaded timestamp, and frame motion counter
	print("[INFO] warming up...")
	time.sleep(2.5)
	avg = None
	lastUploaded = datetime.datetime.now()
	motionCounter = 0
	text = ""
	name = ""

	# capture frames from the camera
	for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	    # grab the raw NumPy array representing the image and initialize
		# the timestamp and occupied/unoccupied text
		frame = f.array
		timestamp = datetime.datetime.now()

		# resize the frame, convert it to grayscale, and blur it
		#frame=500 default, decrease it to go faster
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		# if the average frame is None, initialize it
		if avg is None:
			print("[INFO] starting background model...")
			avg = gray.copy().astype("float")
			rawCapture.truncate(0)
			continue

		# accumulate the weighted average between the current frame and
		# previous frames, then compute the difference between the current
		# frame and running average
		cv2.accumulateWeighted(gray, avg, 0.5)
		frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

		# threshold the delta image, dilate the thresholded image to fill
		# in holes, then find contours on thresholded image
		thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < 5000:
				continue

			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			text = "!"

		# draw the text and timestamp on the frame
		ts = timestamp.strftime("%A_%d_m_%Y_%I:%M:%S%p")
		cv2.putText(frame, "{}".format(ts), (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

		# check to see if the room is occupied
		if text == "!":
			# check to see if enough time has passed between uploads
			if (timestamp - lastUploaded).seconds >= 3.0:
				# increment the motion counter
				motionCounter += 1

				# check to see if the number of frames with consistent motion is
				# high enough
				if motionCounter >= 8: #originally 8
					print("Capturing image.")
					t = TempImage()
					cv2.imwrite(t.path, frame)
					name = "{base}{timestamp}".format(base="", timestamp=ts)
					os.rename(t.path[3:], "{new}.jpg".format(new=name))
					print("[UPLOAD] {}".format(ts))
					with open("/home/pi/Desktop/pisecuritysystem/{name}.jpg".format(name=name), "rb") as f:
						client.files_upload(f.read(), "/{name}.jpg".format(name=name), mute = True)
					os.remove("{name}.jpg".format(name=name))
					# update the last uploaded timestamp and reset the motion
					# counter
					lastUploaded = timestamp
					motionCounter = 0
					text=""

		# otherwise, the room is not occupied
		else:
			motionCounter = 0
			text=""

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
		if break_script:
			print("exiting motiondetect script")
			break

if __name__ == '__main__':
	main()
