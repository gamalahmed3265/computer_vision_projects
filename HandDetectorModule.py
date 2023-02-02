import cv2 as cv
import mediapipe as mp


class HandDetector():
    def __init__(self,mode=False,maxNumHand=2,minDetectCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxNumHand=maxNumHand
        self.minDetectCon=minDetectCon
        self.trackCon=trackCon
        
        self.mpHand=mp.solutions.hands
        
        self.hands=self.mpHand.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxNumHand,
            min_detection_confidence=self.minDetectCon,
            )
        self.mpDrawing=mp.solutions.drawing_utils
        

    def findHind(self,image,draw=True):
        self.results = self.hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
        
        if self.results.multi_hand_landmarks:
            # print(self.results.multi_hand_landmarks)
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDrawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mpHand.HAND_CONNECTIONS)
                # landmark {
                #   x: 0.057027705
                #   y: 0.65548986
                #   z: -0.04419796
                # }
        return image
    def findPostions(self,image,handNum=0,draw=True):
        # (
        # 20,
        # x: 0.5539701
        # y: 0.68431175
        # z: -0.061464716
        # )
        
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNum]
            for idd,lan in enumerate(myHand.landmark):
                h,w,c=image.shape
                cx,cy=int(lan.x*w),int(lan.y*h)
                
                lmList.append([idd,cx,cy])
                if draw:
                    cv.circle(image,(cx,cy),5,(255,0,255),cv.FILLED)
        return lmList