# pisecuritysystem
## overview
This is a raspberry pi based security camera that uses facial recognition and movement detection to find potential thiefs, and alerts the user when this occurs by sending images to a shared dropbox folder. This makes it easy to see who is in the protected space. The software uses opencv and its facial-recognition plugins, to flag people in an image as known or unknown. There are two modes - one that sends images to dropbox if unknown faces are found, and one that sends images if there is any movement in the image. The movement script also works using opencv. The modes are selected using physical buttons, attached to gpio pins on the pi, and information is displayed on an i2c oled display (see pictures below).

## installation
To install, either compile opencv (see notes), install all dependencies in the python scripts. Then add startup.sh to rc.local, and create a file permissions.json, with the dropbox token in json format. Then 'mkdir images' and include pictures of known faces in that folder. OR create the permissions.json and images folder, in the bootable iso included. This way you do not have to download all of teh dependencies, as it takes a very long time on a pi.

## hardware used
raspberry pi model 3B, [night-vision camera](https://www.aliexpress.com/item/Raspberry-Pi-Camera-RPI-Focal-Adjustable-Night-Version-Camera-Acrylic-Holder-IR-Light-FFC-Cable-for/32796213162.html), four push-buttons (off, back, mode, on), [oled screen](https://www.aliexpress.com/item/0-96-inch-IIC-Serial-Yellow-Blue-OLED-Display-Module-128X64-I2C-SSD1306-12864-LCD-Screen/32828449458.html), jumper wires

## pictures
![Alt text](assets/image_1.jpg?raw=true "Title")
![Alt text](assets/image_2.jpg?raw=true "Title")
![Alt text](assets/image_3.jpg?raw=true "Title")

## future upgrades
Add text-messageing if there is an intruder in the area, to alert the user. Make the software less prone to bugs.

## installation
'sudo apt-get install python3-opencv'
'pip3 install face_recognition'
'pip3 install picamera'
'pip3 install numpy'


## inspiration & notes
https://blog.alexellis.io/live-stream-with-docker/

https://www.hackster.io/brendan-lewis/detect-motion-with-opencv-no-pir-sensor-needed-bbeacf

https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/

http://life2coding.com/install-opencv-3-4-0-python-3-raspberry-pi-3

optional youtube live integration:
docker run --privileged --restart=always --name cam -ti alexellis2/streaming:07-05-2018 xxxx-xxxx-xxxx-xxxx
the x's are where your youtube api is inputted

## 2.0  
use https://www.raspberrypi-spy.co.uk/2017/04/raspberry-pi-zero-w-cctv-camera-with-motioneyeos/  
and https://www.youtube.com/watch?v=OAVvWFT1v5I  
and https://github.com/ccrisan/motioneyeos/issues/229  
