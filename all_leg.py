import time

import pigpio
pi= pigpio.pi()

RFU=2
RFL=3
RBU=4	#INVERT
RBL=17
LFU=27	#INVERT
LFL=22
LBU=10
LBL=9

pi.set_mode(RFU, pigpio.OUTPUT)
pi.set_mode(RFL, pigpio.OUTPUT)
pi.set_mode(RBU, pigpio.OUTPUT)
pi.set_mode(RBL, pigpio.OUTPUT)
pi.set_mode(LFU, pigpio.OUTPUT)
pi.set_mode(LFL, pigpio.OUTPUT)
pi.set_mode(LBU, pigpio.OUTPUT)
pi.set_mode(LBL, pigpio.OUTPUT)

def servo(pin,degree) :
    degree=int(degree*2000/180 + 500)
    pi.set_servo_pulsewidth(pin, degree)

def height(h, tx, ty) :
      servo(RFU,min(max(0,(h+tx+ty)),180))
      servo(RFL,min(max(0,(h+tx+ty)),180))
      servo(RBU,min(max(0,180-(h+tx-ty)),180))
      servo(RBL,min(max(0,(h+tx-ty)),180))
      servo(LFU,min(max(0,105-(h-tx+ty)),180))
      servo(LFL,min(max(0,(h-tx+ty)),180))
      servo(LBU,min(max(0,(h-tx-ty)),180))
      servo(LBL,min(max(0,(h-tx-ty)),180))

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
    height(value[0],value[1],value[2])
