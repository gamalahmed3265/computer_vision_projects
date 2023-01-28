import cv2 as cv
import time
import mediapipe as mp

OutputName="Hand landmarks using mediapipe"
wCam,hCam=640,480


cap=cv.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
cTime=0
pTime=0

# For static images:
hands = mp_hands.Hands(
    static_image_mode=True, # only static images
    max_num_hands=2, # max 2 hands detection
    min_detection_confidence=0.5) # detection confidence

# we are not using tracking confidence as static_image_mode is true.


def processImage(image):
    results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

    if not results.multi_hand_landmarks:
        return # if there are no detections, we can skip the rest of the code in this function

    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS)

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
        processImage(frame)
        
        # to write in video each frame
        
        # get fbs: num.of frame 
        cTime=time.time()
        fbs=1/(cTime-pTime)
        pTime=cTime
        # write text in image
        cv.putText(frame,str(int(fbs)),(15,60),font,3,(44,34,67),3)
        
        output.write(frame)
        cv.imshow("frame",frame)
     
        if cv.waitKey(1)& 0xFF ==ord("q"):
            break
    except:
        print("error")

output.release()
cap.release()
cv.destroyAllWindows()        

