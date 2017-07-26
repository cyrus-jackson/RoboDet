import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import os,sys
import sys
import termios
import time

#Camera Servos
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
upDownServo = GPIO.PWM(13,50)
baseServo = GPIO.PWM(19,50)
i = 7
baseServo.start(7)
upDownServo.start(4)
time.sleep(1)
def getchar():

	fd = sys.stdin.fileno()

	if os.isatty(fd):

		old = termios.tcgetattr(fd)
		new = termios.tcgetattr(fd)
		new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
		new[6] [termios.VMIN] = 1
		new[6] [termios.VTIME] = 0

		try:
			termios.tcsetattr(fd, termios.TCSANOW, new)
			termios.tcsendbreak(fd,0)
			ch = os.read(fd,7)
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, old)
	else:
		ch = os.read(fd,7)

	return(ch)
def forward():
	GPIO.setup(7,GPIO.LOW)
	GPIO.setup(11,GPIO.LOW)
def stop():
	GPIO.setup(7,GPIO.HIGH)
	GPIO.setup(11,GPIO.HIGH)
def left():
	GPIO.setup(7,GPIO.LOW)
	GPIO.setup(11,GPIO.HIGH)
def right():
	GPIO.setup(7,GPIO.HIGH)
	GPIO.setup(11,GPIO.LOW)


try:
	while True:
		key = str(getchar())
		print(key)
		if key == "s":
			stop()
			time.sleep(0.06)
			print("stop")
		if key == "w":
			forward()
			time.sleep(0.3)
			stop()
		if key == 'a':
			left()
			time.sleep(0.15)
			stop()
		if key == 'd':
			right()
			time.sleep(0.15)
			stop()
		if key == 'e':
			if i > 12:
				i = 3
			i = i + 1
			baseServo.ChangeDutyCycle(i)
			time.sleep(0.2)
		if key == 'r':
			if i < 4:
				i = 14
			i = i - 1
			baseServo.ChangeDutyCycle(i)
			time.sleep(0.2)
		if key == 'v':
			if i < 8:
				i = i + 1
				upDownServo.ChangeDutyCycle(i)
				time.sleep(0.2)
		if key == 'f':
			if i > 1:
				i = i - 1
				upDownServo.ChangeDutyCycle(i)
				time.sleep(0.2)
		print(i)
except:
# this catches ALL other exceptions including errors.
# You won't get any error messages for debugging
# so only use it once your code is working
	print "Other error or exception occurred!"

finally:
	upDownServo.stop()
	baseServo.stop()
	GPIO.cleanup() # this ensures a clean exit
