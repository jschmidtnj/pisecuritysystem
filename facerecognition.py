# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import cv2
import face_recognition
import picamera
import numpy as np
import json
import time
import datetime
import glob
import os
import dropboximage
import RPi.GPIO as GPIO2
break_script = False

def facemain():
	pin_num = 22
	#setup gpio
	GPIO2.setmode(GPIO2.BCM)
	# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
	# Both ports are wired to connect to GND on button press.
	# So we'll be setting up falling edge detection for both
	GPIO2.setup(pin_num, GPIO2.IN, pull_up_down=GPIO2.PUD_UP)


	# Get a reference to the Raspberry Pi camera.
	# If this fails, make sure you have a camera connected to the RPi and that you
	# enabled your camera in raspi-config and rebooted first.
	camera = picamera.PiCamera()
	camera.resolution = (320, 240)
	output = np.empty((240, 320, 3), dtype=np.uint8)

	# Load a sample picture and learn how to recognize it.
	print("Loading known face image(s)")
	encodings = []
	os.chdir("images")
	for file in glob.glob("*.jpg"):
		image = face_recognition.load_image_file(file)
		encodings.append(face_recognition.face_encodings(image)[0])

	# Initialize some variables
	face_locations = []
	face_encodings = []

	while True:
		print("Getting image.")
		# Grab a single frame of video from the RPi camera as a numpy array
		camera.capture(output, format="rgb")

		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(output)
		print("Found {} faces in image.".format(len(face_locations)))
		face_encodings = face_recognition.face_encodings(output, face_locations)

		intruder = False
		# Loop over each face found in the frame to see if it's someone we know.
		for face_encoding in face_encodings:
			# See if the face is a match for the known face(s)
			match = face_recognition.compare_faces(encodings, face_encoding)

			if match[0] == False:
				intruder = True

			if intruder:
				print("I see an Intruder!")
				camera.close()
				time.sleep(.5)
				#run the send to dropbox script
				dropboximage.dbxmain()
				camera = picamera.PiCamera()
				camera.resolution = (320, 240)

			else:
				print("Everyone is friendly!")
		if GPIO2.input(pin_num) == False:
			print("ending script")
			break
	GPIO2.cleanup()
	camera.close()
	print("camera closed")

if __name__ == '__main__':
	facemain()
