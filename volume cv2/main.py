import cv2
import time
from cv2 import putText
import numpy as np
from pyparsing import empty
import handtrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

w_cam,h_cam = 240 ,280

cap = cv2.VideoCapture(0)

detector = htm.handDetector()

prev_time = 0
curr_time = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


vol_range = volume.GetVolumeRange()
vol = 0
vol_perc = 0
vol_bar = 400
min_vol = vol_range[0]
max_vol = vol_range[1]


while True:
    success, img = cap.read()
    img = detector.find_hands(img)

    lmk_list = detector.find_hand_pos(img)
    if len(lmk_list) != 0:
        
        x1,y1 = lmk_list[4][1],lmk_list[4][2]
        x2,y2 = lmk_list[8][1],lmk_list[8][2]
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
        cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        
        # range 300 - 50
        #volume range -65 - 0
        #convert volume range
        vol = np.interp(length,[50,300],[min_vol,max_vol])
        vol_bar = np.interp(length,[50,300],[400,80])
        vol_perc = np.interp(length,[50,300],[0,100])
        print(vol,int(length))
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)            

    #volue bar
    cv2.rectangle(img,(10,80),(50,400),(0,0,255),3)
    cv2.rectangle(img,(10,int(vol_bar)),(50,400),(0,0,255),cv2.FILLED)
    cv2,putText(img,f'{int(vol_perc)}%',(10,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)

    curr_time = time.time()
    fps = 1/(curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(img,f'FPS: {int(fps)}',(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,160),3)#draw text on the screen

    cv2.imshow("img",img)
    if cv2.waitKey(1) == ord('q'):#if the asci key is of q then we breka out of the loop
        break 

