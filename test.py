import Adafruit_GPIO
import Adafruit_SSD1306
text = "asdf"
import RPi.GPIO as GPIO
print(str(text)[2:(len(text)-1)])
break_script = False
#setup gpio
def power_button_pressed(channel):
	global break_script
	print("asdfasdf")
	break_script = True
	#GPIO.remove_event_detect(17)
GPIO.setmode(GPIO.BCM)
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#define mode number by push button gpio pins or flags or something
# when a falling edge is detected on port 17, regardless of whatever
# else is happening in the program, the function mode_button_pressed will be run
GPIO.add_event_detect(17, GPIO.FALLING, callback=power_button_pressed, bouncetime=300)
while True:
	if break_script:
		print("exiting motiondetect script")
		break

