import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import HandDetectorModule as HDM
import pyautogui as auto
import math

wCam,hCam=1280,720

handDetector=HDM.HandDetector()
cap=cv.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)


font=cv.FONT_HERSHEY_PLAIN

def SignLanguageRecognitionUsingMediapipe(image,lst):
    fingerTips=[8,12,16,20]
    thumb=4
    
    # [8, 395, 584]
    # [12, 344, 609]
    # [16, 286, 630]
    # [20, 221, 648]
    
    for fin in fingerTips:
        # print(lst[fin])
        cv.circle(image,(lst[fin][1],lst[fin][2]),15,(255,0,0),cv.FILLED)

        #   8           5
        if lst[fin][1] < lst[fin-3][1]:
            # cv.circle(image,(lst[fin][1],lst[fin][2]),15,(0,0,255),cv.FILLED)
            cv.putText(image,"Dislike",(40,100),font,2,(255,0,0),3)
        else:
            cv.putText(image,"like",(40,100),font,2,(255,0,0),3)


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
                SignLanguageRecognitionUsingMediapipe(frame,lmList)
            
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