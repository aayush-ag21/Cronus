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

def height(h, tx, ty) :
      servos=[2,3,8,17,27,22,10,9]
      border=[min(max(15,(h+tx+ty)),75),min(max(15,(h+tx+ty)),75),180-min(max(15,(h+tx-ty)),75),min(max(15,(h+tx-ty)),75),105-min(max(15,(h-tx+ty)),75),min(max(15,(h-tx+ty)),75),min(max(15,(h-tx-ty)),75),min(max(15,(h-tx-ty)),75)]
      for j in range(8):
         while( pi.get_servo_pulsewidth(servos[j]) != (int(border[j]/10)*10) ) :
            for i in range(8):
                degree = ( int( border[i]/10 ) *10 )
                if(pi.get_servo_pulsewidth(servos[i])>degree):
                   pi.set_servo_pulsewidth( servos[i], min( max( pi.get_servo_pulsewidth(servos[i])-10,500 ),2500 ))
                   time.sleep(0.02)
                if(pi.get_servo_pulsewidth(servos[i])<degree):
                   pi.set_servo_pulsewidth(servos[i],min(max(pi.get_servo_pulsewidth(servos[i])+10,500),2500))
                   time.sleep(0.02)
      print(*border)
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
