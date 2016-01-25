import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

import picamera
from time import sleep
camera = picamera.PiCamera()

import global_rig_variables

#supply a pulse time between 0.0 and 100.0
#14.9 and 99.9 create the lowest possible speeds.
def rotate(pulseTime):
	pwm.ChangeDutyCycle(pulseTime)

rotate_count = 0.000

camera.start_recording('input/video/scan.h264')

while(rotate_count < global_rig_variables.full_rotation_time):
	rotate(99.9)
	sleep(global_rig_variables.seconds_per_degree)
	rotate_count += global_rig_variables.seconds_per_degree

camera.stop_recording()
