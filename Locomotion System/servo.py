#This code is to test one servo
import time

import pigpio
pi= pigpio.pi()
pin=int(input('pin'))

pi.set_mode(pin,pigpio.OUTPUT)
pi.set_servo_pulsewidth(pin,0)

def servo(pin1,degree):
    degree=min(max(10*(int((degree*2000/180 + 500)/10)),500),2500)
    pi.set_servo_pulsewidth(pin,degree)

value=0

while(1):
	angle= int(input('Enter angle'))
	if  angle is -1:
		break
	servo(pin,angle)
pi.stop()
