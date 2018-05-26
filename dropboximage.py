import picamera
import json
import time
import glob
import os
import dropbox as dbx
from picamera.array import PiRGBArray
import datetime
import warnings
import imutils
import cv2
from pyimagesearch.tempimage import TempImage

def main():
  # Put your token here:
  with open("/home/pi/Desktop/pisecuritysystem/permissions.json") as f:
    data = json.load(f)
  client = dbx.Dropbox(data['db-token'])

  # initialize the camera and grab a reference to the raw camera capture
  camera = picamera.PiCamera()
  #default 640x480 - decrease to go faster
  #motion-detect camera resolution
  camera.resolution = (1808,1008)
  rawCapture = PiRGBArray(camera, size=(1808,1008))

  for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = f.array
    timestamp = datetime.datetime.now()
    frame = imutils.resize(frame, width=1808)

    # draw the text and timestamp on the frame
    ts = timestamp.strftime("%A_%d_%m_%Y_%I:%M:%S%p")
    cv2.putText(frame, "{}".format(ts), (10, 20),
      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    t = TempImage()
    cv2.imwrite(t.path, frame)
    print("[UPLOAD] {}".format(ts))
    name = "{base}{timestamp}".format(base="", timestamp=ts)
    os.rename(t.path[3:], "{new}.jpg".format(new=name))
    with open("/home/pi/Desktop/pisecuritysystem/{name}.jpg".format(name=name), "rb") as f:
      client.files_upload(f.read(), "/{name}.jpg".format(name=name), mute = True)
    os.remove("{name}.jpg".format(name=name))

    rawCapture.truncate(0)
    camera.close()
    break
if __name__ == '__main__':
  main()
