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
    
    def putText(text):
        cv.putText(image,text,(40,100),font,2,(255,0,0),3)

    fingerFoldStatus=[]
    fingerTips=[8,12,16,20]
    thumb=4
    
    # [8, 395, 584]
    # [12, 344, 609]
    # [16, 286, 630]
    # [20, 221, 648]
    cv.circle(image,(lst[thumb][1],lst[thumb][2]),15,(0,0,255),cv.FILLED)
    for fin in fingerTips:
        # print(lst[fin])
        cv.circle(image,(lst[fin][1],lst[fin][2]),15,(255,0,0),cv.FILLED)

        #   8           5
        if lst[fin][1] < lst[fin-3][1]:
            # cv.circle(image,(lst[fin][1],lst[fin][2]),15,(0,0,255),cv.FILLED)
            fingerFoldStatus.append(True)
        else:
            fingerFoldStatus.append(False)
            
            
    if lst[4][2] < lst[2][2] and lst[8][2] < lst[6][2] and lst[12][2] < lst[10][2] and \
                    lst[16][2] < lst[14][2] and lst[20][2] < lst[18][2] and lst[17][1] < lst[0][1] < \
                    lst[5][1]:
        putText("STOP")
        print("STOP")

    # Forward
    if lst[3][1] > lst[4][1] and lst[8][2] < lst[6][2] and lst[12][2] > lst[10][2] and \
            lst[16][2] > lst[14][2] and lst[20][2] > lst[18][2]:
        putText("FORWARD")
        print("FORWARD")

    # Backward
    if lst[3][1] > lst[4][1] and lst[3][2] < lst[4][2] and lst[8][2] > lst[6][2] and lst[12][2] < lst[10][2] and \
            lst[16][2] < lst[14][2] and lst[20][2] < lst[18][2]:
        putText("BACKWARD")
        print("BACKWARD")

    # Left
    if lst[4][2] < lst[2][2] and lst[8][1] < lst[6][1] and lst[12][1] > lst[10][1] and \
            lst[16][1] > lst[14][1] and lst[20][1] > lst[18][1] and lst[5][1] < lst[0][1]:
        putText("LEFT")
        print("LEFT")

    # Right
    if lst[4][2] < lst[2][2] and lst[8][1] > lst[6][1] and lst[12][1] < lst[10][1] and \
            lst[16][1] < lst[14][1] and lst[20][1] < lst[18][1]:
        cv.putText(image, "RIGHT", (20, 30),font, 1, (0, 0, 255), 3)
        print("RIGHT")
    if all(fingerFoldStatus):
        if lst[thumb][2] < lst[thumb-1][2] <lst[thumb-2][2]:
            putText("like")
        if lst[thumb][2] > lst[thumb-1][2] >lst[thumb-2][2]:
              putText("Dislike")
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