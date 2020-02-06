# This Code carries out face detection on camera stream
import cv2
import numpy as np
import datetime
import time

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out1 = cv2.VideoWriter('output1.avi',fourcc,10.0,(640,480))
out2 = cv2.VideoWriter('output2.avi',fourcc,10.0,(640,480))

itime=time.time()


while 1:
    
    ret, img = cap.read()
    fgmask = fgbg.apply(img)

    img4 = img
    img3= img
   
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
    
                
    """
    img[0:1000-y:y+h+25 , 0:1000-x:x+w+25 ] = [0,0,0]         
    
    img3[0:y-25 ,0:1000]=(0,0,0)
    img3[0:1000 ,0:x-25]=(0,0,0)
    img3[0:1000, x+w+25:1000]=(0,0,0)
    img3[y+h+25:1000, 0:1000]=(0,0,0)
  
    img3[0:y-25 ,0:1000]=cv2.cvtColor(img[0:y-25 ,0:1000], cv2.COLOR_BGR2GRAY)
    img3[0:1000 ,0:x-25]=cv2.cvtColor(img[0:1000 ,0:x-25], cv2.COLOR_BGR2GRAY)
    img3[0:1000, x+w+25:1000]=cv2.cvtColor(img[0:1000, x+w+25:1000], cv2.COLOR_BGR2GRAY)
    img3[y+h+25:1000, 0:1000]=cv2.cvtColor(img[y+h+25:1000, 0:1000], cv2.COLOR_BGR2GRAY)
    """
   
    
    
    img2 = cv2.medianBlur(cv2.cvtColor(fgmask,cv2.COLOR_GRAY2RGB),9)#9 IS SENSITIVITY COUNTER,DECREASE TO MAKE SENSITIVE,USE ODD NUMBERS ONLY
    currentDT = datetime.datetime.now()
    font = cv2.FONT_HERSHEY_SIMPLEX

    
    cv2.putText(img2,currentDT.strftime("%Y-%m-%d %H:%M:%S"),(450,420), font, 0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img,currentDT.strftime("%Y-%m-%d %H:%M:%S"),(450,420), font, 0.5,(255,255,255),2,cv2.LINE_AA)
    if img2.any()!= 0:
        out2.write(img2)
        
        
    ctime=time.time()
    if len(faces) != 0:    
        out1.write(img)
        itime=time.time()
    elif ctime-itime<10:
        out1.write(img)
    else  :   
        out1.release()
        out2.release()

        cap.release()
        cv2.destroyAllWindows()   
        break
    """
        itime=time.time()
        while(len(faces)==0):
            
            ctime=time.time()
            if(len(faces)=!=0out1.write(img)
               break
    """



    cv2.imshow('fgmask',img2)
    cv2.imshow('videofeed_fgmask',img)

        
        
       
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break;

    
    """   
    itime=time.time()
    while(len(faces)==0):
        ctime=time.time()
        if(ctime-itime>10):
            esc=1
            break
        


    ctr = 0
    itime=time.time()
    while 1:
        ctime=time.time()
        if(tim

        for all in range (time.time(),finaltime) :
            if img2.any()==0 :
                
                out2.release()
                ctr+=1
            
        for all  in range (currentDT,finaltime ):
            if len(faces) == 0:
                 
                out1.release()
                ctr+=1
                if ctr==2:
                
    """

out1.release()
out2.release()

cap.release()
cv2.destroyAllWindows()
