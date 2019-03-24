import time
import pigpio

pi= pigpio.pi()

RFU=2
RFL=3

pi.set_mode(RFU, pigpio.OUTPUT)
pi.set_mode(RFL, pigpio.OUTPUT)

def servo(pin1,pin2,degree) :
    degree=int(degree*2000/180 + 500)
    pi.set_servo_pulsewidth(pin1, degree)
    pi.set_servo_pulsewidth(pin2, degree)

def height(h, tx, ty) :
      servo(RFU, RFL,110- (h+tx+ty))

value = [0,0,0]
while 1:
    para = input('Enter parameter\n').split(' ')
    parameters = ['H','TX','TY']
    for item in para:
                if item in parameters:
                    try:
                        value[parameters.index(item)]=int(para[para.index(item)+1])
                    except:
                        print("Error")
                                       
    print(*value)
    height(value[0], value[1], value[2])

    #Y is front ,X is side
    #X for X axis locomotion,Y for Y axis locomotion,R for rotate,H is chassis height,TX for tilt in X,TY for tilt in Y
