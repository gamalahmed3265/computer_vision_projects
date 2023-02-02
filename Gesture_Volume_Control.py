import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import HandDetectorModule as HDM
import pyautogui as auto
import math
from pynput.Keyboard import Key,Controller 

Keyboard=Controller()

wCam,hCam=1280,720

handDetector=HDM.HandDetector()
cap=cv.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)


maxHand=300
minHand=50

maxAngle=0
minAngle=-95

colorCircle=(255,140,0)

lastLength=None
lastAngle=None

font=cv.FONT_HERSHEY_PLAIN

def gestureVolumeControl(image,lst):
   
    thumb_tic=4
    index_finger_Tp=8

    # [4, 332, 369]
    # [8, 382, 205] 
    x1,y1=lst[thumb_tic][1],lst[thumb_tic][2]
    x2,y2=lst[index_finger_Tp][1],lst[index_finger_Tp][2]
    
    
    cv.circle(image,(x1,y1),15,(0,0,255),cv.FILLED)
    cv.circle(image,(x2,y2),15,(0,0,255),cv.FILLED)
    
    cv.line(image,(x1,y1),(x2,y2),(30,34,0),3)
    
    cx,cy=(x1+x2)//2,(y1+y2)//2

    length=math.hypot(x2-x1,y2-y1)

    cv.circle(image,(cx,cy),15,colorCircle,cv.FILLED)

    #to convert range to onther range    
    angle=np.interp(length,[minHand,maxHand],[minAngle,maxAngle])
    angleBar=np.interp(length,[minHand,maxHand],[400,150])
    angleDeg=np.interp(length,[minHand,maxHand],[0,100])
 
    if lastLength:
        if length>lastLength:
            Keyboard.press(Key.media_volume_up)
            Keyboard.release(Key.media_volume_up)
                
        elif length<lastLength:
            Keyboard.press(Key.media_volume_down)
            Keyboard.release(Key.media_volume_down)
    
    lastAngle=angle
    lastLength=length
    
    # draw bar volumn
    cv.putText(image,str(int(angleDeg))+"%",(40,100),font,2,colorCircle,3)
    cv.rectangle(image,(50,150),(85,400),(255,0,0),3)
    cv.rectangle(image,(50,int(angleBar)),(85,400),colorCircle,cv.FILLED)

def main():
    font=cv.FONT_HERSHEY_PLAIN
    pTime=0
    cTime=0
    
    while True:
        rat,frame=cap.read()
        frame = cv.flip(frame, 1)
        try:
            frame=handDetector.findHind(frame)
            lmList=handDetector.findPostions(frame)
            
            if len(lmList) != 0:
                gestureVolumeControl(frame,lmList)
                
            
            cTime=time.time()
            fbs=1/(cTime-pTime)
            pTime=cTime
            
            cv.putText(frame,str(int(fbs)),(wCam-100,70),font,3,(255,0,255),3)
        except:
            print("error")
        cv.imshow("frame",frame)
        if cv.waitKey(1)& 0xFF ==ord("q"):
           break
        
    cap.release()
    cv.destroyAllWindows()

if __name__ =="__main__":
    main()