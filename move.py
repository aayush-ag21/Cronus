import time

import pigpio
pi= pigpio.pi()

#1=FRONT	2=BACK		3=PWM

MRF1=26
MRF2=21
MRF3=20

MRB1=12
MRB2=6
MRB3=19

MLF1=15
MLF2=18
MLF3=14

MLB1=24
MLB2=25
MLB3=23

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
				     #positive deg is right down

value = [0,0,0]
while 1:
    para = input('Enter parameter\n').split(' ')
    parameters = ['X','Y','R']
    for item in para:
                if item in parameters:
                    try:
                        value[parameters.index(item)]=int(para[para.index(item)+1])
                    except:
                        print("Error")
    print(*value)
    holo(value[0],value[1],value[2])
