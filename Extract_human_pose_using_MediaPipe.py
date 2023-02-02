import cv2 as cv
import mediapipe as mp
import numpy as np
import time


wCam,hCam=640,480


cap=cv.VideoCapture(0)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


pose=mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)




while True:
    # read frame in video
    ret,image=cap.read()
    h,w,c=image.shape
    # print(w,h,c)
    imgPose=np.zeros([h,w,c])
    imgPose.fill(0)
    try:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        
        
      
        mp_drawing.draw_landmarks(
            imgPose,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        
        
      
    except:
        print("error")
        
    cv.imshow("frame",image)
    cv.imshow("imgPose",imgPose)
    if cv.waitKey(1)& 0xFF ==ord("q"):
        break

cap.release()
cv.destroyAllWindows()        
