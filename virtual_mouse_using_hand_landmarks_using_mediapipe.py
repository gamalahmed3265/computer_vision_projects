import cv2 as cv
import time
import mediapipe as mp
import pyautogui as auto
import numpy as np
import win32api

OutputName="Hand landmarks using mediapipe"
wCam,hCam=640,480

click=0

cap=cv.VideoCapture(0)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pTime=0 # previous time
cTime=0 # current time

wScr,hScr=auto.size() # Size(width=1920, height=1080)


px,py=0,0 # previous x, y location
cx,cy=0,0 # current x, y location

# For static images:
hands = mp_hands.Hands(
    static_image_mode=True, # only static images
    max_num_hands=2, # max 2 hands detection
    min_detection_confidence=0.5) # detection confidence

# we are not using tracking confidence as static_image_mode is true.


def processImage(image):
    landMarkList=[]
    results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    landmarkCheck=results.multi_hand_landmarks
    if not landmarkCheck:
        return # if there are no detections, we can skip the rest of the code in this function

    for hand_landmarks in landmarkCheck:
        
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS)
        
        
        for index,lmm in enumerate(hand_landmarks.landmark) :
            # print(index,lmm)
            
            h,w,s=image.shape
            centerX,CenterY=int(lmm.x*w),int(lmm.y*h)
            
            # print(centerX,CenterY)
            landMarkList.append([index,centerX,CenterY])
            
    return landMarkList


def fingers(landMark):
    fingrsTips=[]
    tipId=[4,8,12,16,20]
    # check 4 ✋
    if landMark[tipId[0]][1] > landMark[ tipId[0]-1 ][1]:
        fingrsTips.append(1)
    else:
        fingrsTips.append(0)     
        # check 8 12 16 20 🖐
    for idd in range(1,5):
        if landMark[tipId[idd]][2] < landMark[tipId[idd] -3][2]:
            fingrsTips.append(1)
        else:
            fingrsTips.append(0)
    return fingrsTips

# remove noise
fource=cv.VideoWriter_fourcc(*"XVID")
# create video with name video
output=cv.VideoWriter(f"{OutputName}.avi",fource,30.0,(wCam,hCam))

# font famaily
font=cv.FONT_HERSHEY_PLAIN

# set the hight, width video
# cap.set(3,wCam)
# cap.set(4,hCam)

while True:
    # read frame in video
    ret,frame=cap.read()
   
    try:
        # to procss the processImage in video each frame
        
        landMarkList=processImage(frame)
        # print("landMarkList",landMarkList)
        
        
        # landMarkList [
        #     [4, 278, 360],
        #     [8, 356, 99],
        #     [12, 441, 52],
        #     [16, 504, 48],
        #     [18, 580, 159],
        #     [20, 613, 90]]
        
        if landMarkList is not None:
            
            x1,y1=landMarkList[8][1:] #  [5, 430, 296],
            x2,y2=landMarkList[12][1:]# [12, 425, 179],
            
            fingersList=fingers(landMarkList)
            # fingersList=[0,1,1,1,1]
            if fingersList[1]==1 and fingersList[2]==0:
                x3=np.interp(x1,(0,wCam),(0,wScr))
                y3=np.interp(y1,(0,hCam),(0,wScr))

                cx=px+(x3-px)/7
                cy=px+(y3-py)/7
                messsage=f"""
                x1:{x1} , y1: {y1}
                x2:{x2} , y2: {y2}
                x3:{x3} , y3: {y3}
                cx:{cx} , cy: {cy}
                        """
                
                auto.moveTo(wCam-cx,cy)
                print(messsage)
                px,py=cx,cy
            if fingersList[1]==0 and fingersList[0]==1:
                # auto.click()
                print("click")
        
        # get fbs: num.of frame 
        cTime=time.time()
        fbs=1/(cTime-pTime)
        pTime=cTime
        # write text in image
        cv.putText(frame,str(int(fbs)),(15,60),font,3,(44,34,67),3)
        
        # to write in video each frame
        output.write(frame)
        cv.imshow("frame",frame)
     
        if cv.waitKey(1)& 0xFF ==ord("q"):
            break
    except:
        print("error")

output.release()
cap.release()
cv.destroyAllWindows()        

