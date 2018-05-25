import facerecognition
import motiondetect
import RPi.GPIO as GPIO
import os
import sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import time

#setup display
RST = 24 # on the PiOLED this pin isnt used
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
space = 8

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

mode_text = "Press Mode to Start"
back_text = "Press PWR to shutdown"
mode = True
start = True

def main():
  global start
  global mode
  global mode_text
  global back_text
  #get display
  global disp
  # Draw a black filled box to clear the image.
  draw.rectangle((0,0,width,height), outline=0, fill=0)

  # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
  cmd = "hostname -I | cut -d\' \' -f1"
  IP = subprocess.check_output(cmd, shell = True )
  cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
  CPU = subprocess.check_output(cmd, shell = True )
  cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
  MemUsage = subprocess.check_output(cmd, shell = True )
  cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
  Disk = subprocess.check_output(cmd, shell = True )

  # Write two lines of text.
  draw.text((x, top),       mode_text, font=font, fill=255)
  draw.text((x, top + space * 1),       back_text, font=font, fill=255)
  new_text = str(IP)[2:(len(str(IP))-3)]
  draw.text((x, top + space * 3),       "IP: " + new_text,  font=font, fill=255)
  new_text = str(CPU)[2:(len(str(CPU))-1)]
  draw.text((x, top + space * 4),     new_text, font=font, fill=255)
  new_text = str(MemUsage)[2:(len(str(MemUsage))-1)]
  draw.text((x, top + space * 5),    new_text,  font=font, fill=255)
  new_text = str(Disk)[2:(len(str(Disk))-1)]
  draw.text((x, top + space * 6),    new_text,  font=font, fill=255)

  # Display image.
  disp.image(image)
  disp.display()

  def mode_button_pressed(channel):
    global mode
    global mode_text
    global back_text

    print("mode button pressed")
    mode = not mode
    if mode:
      mode_text = "face recognition"
      back_text = "press mode to quit"
      #mode 1
      facerecognition.main()
      start=True
    else:
      mode_text = "motion detect"
      back_text = "press mode to quit"
      #mode 2
      motiondetect.main()
      start=True
  def power_button_pressed(channel):
    print("power button pressed")
    os.system("shutdown now -h")

  def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
    # Both ports are wired to connect to GND on button press.
    # So we'll be setting up falling edge detection for both
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #define mode number by push button gpio pins or flags or something
    # when a falling edge is detected on port 17, regardless of whatever
    # else is happening in the program, the function mode_button_pressed will be run
    GPIO.add_event_detect(17, GPIO.FALLING, callback=main.mode_button_pressed, bouncetime=300)

    # when a falling edge is detected on port 23, regardless of whatever
    # else is happening in the program, the function power_button_pressed will be run
    # 'bouncetime=300' includes the bounce control written into interrupts2a.py
    GPIO.add_event_detect(23, GPIO.FALLING, callback=main.power_button_pressed, bouncetime=300)
  if start:
    setup_gpio()
    start=False
  GPIO.cleanup()           # clean up GPIO on normal exit

if __name__ == '__main__':
  #facerecognition.main() #runs mode 1 when first used
  while True:
    main()
