# This is formal final code for whole system, all motors and all servos
import os
import threading
import time
os.system("sudo pigpiod")
import pigpio
pi= pigpio.pi()

RFU=2
RFL=3
RBU=7	#INVERT
RBL=17
LFU=27	#INVERT
LFL=22
LBU=10
LBL=9

#1=FRONT	2=BACK		3=PWM

MRF1=26
MRF2=21
MRF3=20

MRB1=12
MRB2=5
MRB3=19

MLF1=15
MLF2=18
MLF3=14

MLB1=24
MLB2=25
MLB3=23

pi.set_mode(RFU, pigpio.OUTPUT)
pi.set_mode(RFL, pigpio.OUTPUT)
pi.set_mode(RBU, pigpio.OUTPUT)
pi.set_mode(RBL, pigpio.OUTPUT)
pi.set_mode(LFU, pigpio.OUTPUT)
pi.set_mode(LFL, pigpio.OUTPUT)
pi.set_mode(LBU, pigpio.OUTPUT)
pi.set_mode(LBL, pigpio.OUTPUT)
pi.set_mode(MRF1, pigpio.OUTPUT)
pi.set_mode(MRF2, pigpio.OUTPUT)
pi.set_mode(MRF3, pigpio.OUTPUT)
pi.set_mode(MRB1, pigpio.OUTPUT)
pi.set_mode(MRB2, pigpio.OUTPUT)
pi.set_mode(MRB3, pigpio.OUTPUT)
pi.set_mode(MLB1, pigpio.OUTPUT)
pi.set_mode(MLB2, pigpio.OUTPUT)
pi.set_mode(MLB3, pigpio.OUTPUT)
pi.set_mode(MLF1, pigpio.OUTPUT)
pi.set_mode(MLF2, pigpio.OUTPUT)
pi.set_mode(MLF3, pigpio.OUTPUT)

pi.set_servo_pulsewidth(RFU,660)
pi.set_servo_pulsewidth(RFL,1500)
pi.set_servo_pulsewidth(RBU,2500)
pi.set_servo_pulsewidth(RBL,1500)
pi.set_servo_pulsewidth(LFU,1660)
pi.set_servo_pulsewidth(LFL,1500)
pi.set_servo_pulsewidth(LBU,660)
pi.set_servo_pulsewidth(LBL,1500)
pi.write(MRF1,0)
pi.write(MRF2,0)
pi.write(MRF3,0)
pi.write(MRB1,0)
pi.write(MRB2,0)
pi.write(MRB3,0)
pi.write(MLF1,0)
pi.write(MLF2,0)
pi.write(MLF3,0)
pi.write(MLB1,0)
pi.write(MLB2,0)
pi.write(MLB3,0)

def servo(pin,degree) :
    degree=min(max(10*(int((degree*2000/180 + 500)/10)),500),2500)
    while(pi.get_servo_pulsewidth(pin)>degree):
        pi.set_servo_pulsewidth(pin,pi.get_servo_pulsewidth(pin)-10)
        time.sleep(0.02)
    while(pi.get_servo_pulsewidth(pin)<degree):
        pi.set_servo_pulsewidth(pin,pi.get_servo_pulsewidth(pin)+10)
        time.sleep(0.02)

def height(h, tx, ty) :
      t1=threading.Thread(target=servo,args=(RFU,min(max(15,(h+tx+ty)),75 )))
      t1.start()
      t2=threading.Thread(target=servo,args=(RFL,90-min(max(15,(h+tx+ty)),75)))
      t2.start()
      t3=threading.Thread(target=servo,args=(RBU,180-min(max(15,(h+tx-ty)),75)))
      t3.start()
      t4=threading.Thread(target=servo,args=(RBL,90-min(max(15,(h+tx-ty)),75)))
      t4.start()
      t5=threading.Thread(target=servo,args=(LFU,105-min(max(15,(h-tx+ty)),75)))
      t5.start()
      t6=threading.Thread(target=servo,args=(LFL,90-min(max(15,(h-tx+ty)),75)))
      t6.start()
      t7=threading.Thread(target=servo,args=(LBU,min(max(15,(h-tx-ty)),75)))
      t7.start()
      t8=threading.Thread(target=servo,args=(LBL,90-min(max(15,(h-tx-ty)),75)))
      t8.start()

def motor(pin1, pin2, pin3, s):     #front pin1, back pin2 , PWM pin3
      s=s*255/100

      if (s>0):
        pi.write(pin1, 1)
        pi.write(pin2, 0)
      else:
        s = -s
        pi.write(pin2, 1)
        pi.write(pin1, 0)
      pi.set_PWM_dutycycle(pin3, s)

def holo(x,y,r): 		     #positive r is anticlockwise
     motor(MRF1,MRF2,MRF3, (y-x)/(2**0.5)+r)
     motor(MLB1,MLB2,MLB3, (y-x)/(2**0.5)-r)
     motor(MLF1,MLF2,MLF3,1.15*((y+x)/(2**0.5)-r))
     motor(MRB1,MRB2,MRB3, (y+x)/(2**0.5)+r)
				     #positive deg is right downvalue = [0,0,0]

value=[0,0,0,0,0,0]
height(value[3],value[4],value[5])
holo(value[0],value[1],value[2])

print("Y - FORWARD, RANGE -100 TO 100","X - RIGHT, RANGE -100 TO 100","R - ROTATE,RANGE -60 TO 60")

try:
 while 1:
    para = input('Enter parameter\n').split(' ')
    parameters = ['X','Y','R','H','TX','TY']
    for item in para:
                if item in parameters:
                    try:
                        value[parameters.index(item)]=int(para[para.index(item)+1])
                    except:
                        print("Error")

    print(*value)
    height(value[3],value[4],value[5])
    holo(value[0],value[1],value[2])
except KeyboardInterrupt:
    pass
print("closed successfully")
