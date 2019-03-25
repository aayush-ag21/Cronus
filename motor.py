import time

import pigpio
pi= pigpio.pi()

MRF1=21
MRF2=26
MRF3=20

pi.set_mode(MRF1, pigpio.OUTPUT)
pi.set_mode(MRF2, pigpio.OUTPUT)
pi.set_mode(MRF3, pigpio.OUTPUT)

def motor(pin1, pin2, pin3, s):     #forward pin1 high, backward pin2 high, pin3 for power
      s=s*255/100
      
      if (s>0):
        pi.write(pin1, 1)
        pi.write(pin2, 0)
      else:
        s = -s
        pi.write(pin2, 1)
        pi.write(pin1, 0)
      pi.set_PWM_dutycycle(pin3, s)  
        
value = 0
while 1:
    speed = int(input('Enter SPEED:  '))
    motor(MRF1,MRF2,MRF3,speed)
