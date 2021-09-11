import cv2
import mediapipe as mp
import time
import handtracking_module as htm
import math
import numpy as np
import pycaw 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# htm init
wCam, hCam = 1280,720
cap = cv2.VideoCapture(0)  
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
cTime = 0
dector = htm.handDector(dectionCon=0.9)

# volume init
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#(-96.0, 0.0, 1.5)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

minLength = 50
maxLength = 300

vol = volume.GetMasterVolumeLevel()
volBar = np.interp(vol,
                    [minVol,maxVol],
                    [400,150])

while True:
    success, img = cap.read()
    img = dector.findHands(img)
    handList = dector.findPosition(img,draw=False)
    # if len(handList) != 0:
    #     print(handList[0][8])
    
    # show fps 
    # cTime = time.time()
    # fps = 1/(cTime-pTime)
    # pTime = cTime
    # cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    if len(handList) != 0:
        firstHand = handList[0]
        x1 , y1 = firstHand[4].x , firstHand[4].y
        x2 , y2 = firstHand[8].x , firstHand[8].y
        cx , cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

        length = math.hypot(x1-x2,y1-y2)
        

        vol = np.interp(length,
                        [minLength,maxLength],
                        [minVol,maxVol])
        volBar=np.interp(length,
                        [minLength,maxLength],
                        [400,150])

        # print(int(length),vol)
        # volume.SetMasterVolumeLevel(vol, None)
        


        if length<minLength:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
    
    
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)

    cv2.imshow("Image",img)
    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
