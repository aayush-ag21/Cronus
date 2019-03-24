import pigpio
pi= pigpio.pi()

pi.set_mode(2,pigpio.OUTPUT)

def servo(pin1,degree) :
    degree=int(degree*2000/180 + 500)
    pi.set_servo_pulsewidth(pin1, degree)
#    pi.set_servo_pulsewidth(pin2, degree)

value=0

while(1):
	angle= int(input('Enter angle'))
	if  angle is -1:
		break
	servo(2,angle)
pigpio.stop()
