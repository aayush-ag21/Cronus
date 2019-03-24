import cv2
import numpy as np
import datetime
import time
import sys

sys.stdout("echo hi")
import pigpio
pi= pigpio()

RFU=0
RFD=0
RBU=0
RBL=0
LFU=0
LFL=0
LBU=0
LBL=0

MRF1=0
MRB1=0
MLF1=0
MLB1=0
MRF2=0
MRB2=0
MLF2=0
MLB2=0
MRF3=0
MRB3=0
MLF3=0
MLB3=0

pi.set_mode(RFU, pigpio.OUTPUT)
pi.set_mode(RFD, pigpio.OUTPUT)
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

def fed() :

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap = cv2.VideoCapture(0)
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    out1 = cv2.VideoWriter('output1.avi',fourcc,10.0,(640,480))
    
    itime=time.time()
    
    while 1:
        
        ret, img = cap.read()
       
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        x,y,w,h = 0,0,0,0
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h+25, x:x+w+25]
            roi_color = img[y:y+h+25, x:x+w+25]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            if len(eyes) <2*len(faces)+1 :
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
                    
        currentDT = datetime.datetime.now()
        font = cv2.FONT_HERSHEY_SIMPLEX

        
        cv2.putText(img,currentDT.strftime("%Y-%m-%d %H:%M:%S"),(450,420), font, 0.5,(255,255,255),2,cv2.LINE_AA)

        ctime=time.time()
        if len(faces) != 0:    
            out1.write(img)
            itime=time.time()
        elif ctime-itime<10:
            out1.write(img)
        else  :   
            out1.release()
                
        cv2.imshow('videofeed_fgmask',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break;
        
    out1.release()
    cap.release()
    cv2.destroyAllWindows()

def md() :

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap = cv2.VideoCapture(0)

    fgbg = cv2.createBackgroundSubtractorMOG2()
    
    out2 = cv2.VideoWriter('output2.avi',fourcc,10.0,(640,480))
   
    while 1:
        
        ret, img1 = cap.read()
        fgmask = fgbg.apply(img1)
        img2 = cv2.medianBlur(cv2.cvtColor(fgmask,cv2.COLOR_GRAY2RGB),9)
        currentDT = datetime.datetime.now()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img2,currentDT.strftime("%Y-%m-%d %H:%M:%S"),(450,420), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        if img2.any()!= 0:
            out2.write(img2)
        cv2.imshow('fgmask',img2)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break;
        
    out2.release()

    cap.release()
    cv2.destroyAllWindows()

def servo(pin1,pin2,degree) :
    degree=int(degree*2000/180 + 500)
    pi.set_servo_pulsewidth(pin1, degree)
    pi.set_servo_pulsewidth(pin2, degree)

def motor(pin1, pin2, pin3, s):     #forward pin1 high, backward pin2 high, pin3 for power
      s=s*255/100
      
      if (s>0):
        pi.write(pin1, 1)
        pi.write(pin2, 0)
      else:
        s = -s
        pi.write(pin2, s)
        pi.write(pin1, 0)
      pi.set_PWM_dutycycle(pin3, s)  
        
def holo(x,y,r):  #positive r is anticlockwise
     motor(MRF, (y-x)/(2**0.5)+r)
     motor(MLB, (y-x)/(2**0.5)+r)
     motor(MLF, (y+x)/(2**0.5)-r)
     motor(MRB, (y+x)/(2**0.5)-r)
     
#positive deg is right down

      
def height(h, tx, ty) :
      servo(RFU, RFL, (h+tx+ty))
      servo(RBU, RBL, (h+tx-ty))
      servo(LFU, LFL, (h-tx+ty))
      servo(LBU, LBL, (h-tx-ty))

value = [0,0,0,0,0,0]
while 1:
    para = input('Enter parameter\n').split(' ')
    parameters = ['X','Y','R','H','TX','TY','FED','MD']
    for item in para:
                if item in parameters:
                    try:
                        value[parameters.index(item)]=int(para[para.index(item)+1])
                        if(item=='FED'):
                            print('FED')
                            fed()
                        if(item=='MD'):
                            print('MD')
                            md()
                    except:
                        print("Error")
                                       
    print(*value)
    holo(value[0],value[1],value[2])
    height(value[3], value[4], value[5])

    #Y is front ,X is side
    #X for X axis locomotion,Y for Y axis locomotion,R for rotate,H is chassis height,TX for tilt in X,TY for tilt in Y
    
    pi.stop()
    break;import cv2
import numpy as np
import datetime
import time
import sys

sys.stdout("echo hi")
import pigpio
pi= pigpio()

RFU=0
RFD=0
RBU=0
RBL=0
LFU=0
LFL=0
LBU=0
LBL=0

MRF1=0
MRB1=0
MLF1=0
MLB1=0
MRF2=0
MRB2=0
MLF2=0
MLB2=0
MRF3=0
MRB3=0
MLF3=0
MLB3=0

pi.set_mode(RFU, pigpio.OUTPUT)
pi.set_mode(RFD, pigpio.OUTPUT)
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

def fed() :

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap = cv2.VideoCapture(0)
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    out1 = cv2.VideoWriter('output1.avi',fourcc,10.0,(640,480))
    
    itime=time.time()
    
    while 1:
        
        ret, img = cap.read()
       
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        x,y,w,h = 0,0,0,0
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h+25, x:x+w+25]
            roi_color = img[y:y+h+25, x:x+w+25]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            if len(eyes) <2*len(faces)+1 :
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
                    
        currentDT = datetime.datetime.now()
        font = cv2.FONT_HERSHEY_SIMPLEX

        
        cv2.putText(img,currentDT.strftime("%Y-%m-%d %H:%M:%S"),(450,420), font, 0.5,(255,255,255),2,cv2.LINE_AA)

        ctime=time.time()
        if len(faces) != 0:    
            out1.write(img)
            itime=time.time()
        elif ctime-itime<10:
            out1.write(img)
        else  :   
            out1.release()
                
        cv2.imshow('videofeed_fgmask',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break;
        
    out1.release()
    cap.release()
    cv2.destroyAllWindows()

def md() :

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap = cv2.VideoCapture(0)

    fgbg = cv2.createBackgroundSubtractorMOG2()
    
    out2 = cv2.VideoWriter('output2.avi',fourcc,10.0,(640,480))
   
    while 1:
        
        ret, img1 = cap.read()
        fgmask = fgbg.apply(img1)
        img2 = cv2.medianBlur(cv2.cvtColor(fgmask,cv2.COLOR_GRAY2RGB),9)
        currentDT = datetime.datetime.now()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img2,currentDT.strftime("%Y-%m-%d %H:%M:%S"),(450,420), font, 0.5,(255,255,255),2,cv2.LINE_AA)
        if img2.any()!= 0:
            out2.write(img2)
        cv2.imshow('fgmask',img2)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break;
        
    out2.release()

    cap.release()
    cv2.destroyAllWindows()

def servo(pin1,pin2,degree) :
    degree=int(degree*2000/180 + 500)
    pi.set_servo_pulsewidth(pin1, degree)
    pi.set_servo_pulsewidth(pin2, degree)

def motor(pin1, pin2, pin3, s):     #forward pin1 high, backward pin2 high, pin3 for power
      s=s*255/100
      
      if (s>0):
        pi.write(pin1, 1)
        pi.write(pin2, 0)
      else:
        s = -s
        pi.write(pin2, s)
        pi.write(pin1, 0)
      pi.set_PWM_dutycycle(pin3, s)  
        
def holo(x,y,r):  #positive r is anticlockwise
     motor(MRF, (y-x)/(2**0.5)+r)
     motor(MLB, (y-x)/(2**0.5)+r)
     motor(MLF, (y+x)/(2**0.5)-r)
     motor(MRB, (y+x)/(2**0.5)-r)
     
#positive deg is right down

      
def height(h, tx, ty) :
      servo(RFU, RFL, (h+tx+ty))
      servo(RBU, RBL, (h+tx-ty))
      servo(LFU, LFL, (h-tx+ty))
      servo(LBU, LBL, (h-tx-ty))

value = [0,0,0,0,0,0]
while 1:
    para = input('Enter parameter\n').split(' ')
    parameters = ['X','Y','R','H','TX','TY','FED','MD']
    for item in para:
                if item in parameters:
                    try:
                        value[parameters.index(item)]=int(para[para.index(item)+1])
                        if(item=='FED'):
                            print('FED')
                            fed()
                        if(item=='MD'):
                            print('MD')
                            md()
                    except:
                        print("Error")
                                       
    print(*value)
    holo(value[0],value[1],value[2])
    height(value[3], value[4], value[5])

    #Y is front ,X is side
    #X for X axis locomotion,Y for Y axis locomotion,R for rotate,H is chassis height,TX for tilt in X,TY for tilt in Y
    
    pi.stop()
    break;
