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
    print(lst)
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