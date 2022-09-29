
import cv2 
import time
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.8, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,self.maxHands,self.modelComplex,self.detectionCon,self.trackCon)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self,img,draw =True):
        
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        #print(results.multi_hand_landmarks)q

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                #must only draw when asked 
                if draw:
                    self.mp_draw.draw_landmarks(img,hand_lms,self.mp_hands.HAND_CONNECTIONS)#how to draw on the screen
                
        return img    

    def find_hand_pos(self,img,hand_no= 0 , draw = True):
        
        lm_lst = []
        if self.results.multi_hand_landmarks:
            my_hand=self.results.multi_hand_landmarks[hand_no]
            for id,lm in enumerate(my_hand.landmark):
                    #print(id,lm)
                    h,w,c = img.shape
                    cx, cy = int(lm.x*w),int(lm.y*h)
                    #print(id,cx,cy)
                    lm_lst.append([id,cx,cy])


        return lm_lst
                
#dummy code
def main():
    
    prev_time = 0
    curr_time = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    
    while True:
        success, img = cap.read()# returns video/image
        img = detector.find_hands(img)

        lmlst = detector.find_hand_pos(img)#position of hand coordinates
        if len(lmlst) != 0:
            print(lmlst[3])
        curr_time = time.time()
        fps = 1/(curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,160),3)#draw text on the screen

        cv2.imshow("image",img)#creates the window to display the vid/image
        if cv2.waitKey(1) == ord('q'):#if the asci key is of q then we breka out of the loop
            break


if __name__ == "__main__":
    main()