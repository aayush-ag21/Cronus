#This code is for all servos
import time

import pigpio
pi= pigpio.pi()

RFU=2
RFL=3
RBU=8	#INVERT
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

pi.set_servo_pulsewidth(RFU,660)
pi.set_servo_pulsewidth(RFL,660)
pi.set_servo_pulsewidth(RBU,2500)
pi.set_servo_pulsewidth(RBL,660)
pi.set_servo_pulsewidth(LFU,1660)
pi.set_servo_pulsewidth(LFL,660)
pi.set_servo_pulsewidth(LBU,660)
pi.set_servo_pulsewidth(LBL,660)

def servo(pin,degree) :
    degree=min(max(10*(int((degree*2000/180 + 500)/10)),500),2500)
    while(pi.get_servo_pulsewidth(pin)>degree):
        pi.set_servo_pulsewidth(pin,pi.get_servo_pulsewidth(pin)-10)
        time.sleep(0.02)
    while(pi.get_servo_pulsewidth(pin)<degree):
        pi.set_servo_pulsewidth(pin,pi.get_servo_pulsewidth(pin)+10)
        time.sleep(0.02)

def height(h, tx, ty) :
      servo(RFU,min(max(15,(h+tx+ty)),75))
      servo(RFL,min(max(15,(h+tx+ty)),75))
      servo(RBU,180-min(max(15,(h+tx-ty)),75))
      servo(RBL,min(max(15,(h+tx-ty)),75))
      servo(LFU,105-min(max(15,(h-tx+ty)),75))
      servo(LFL,min(max(15,(h-tx+ty)),75))
      servo(LBU,min(max(15,(h-tx-ty)),75))
      servo(LBL,min(max(15,(h-tx-ty)),75))

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
