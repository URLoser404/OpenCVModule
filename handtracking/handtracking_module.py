import cv2
import mediapipe as mp
import time

class landmark:
    def __init__(self,id,x,y):
        self.id=id
        self.x=x
        self.y=y

        
class handDector():
    def __init__(self,mode =False,maxHands =1,dectionCon = 0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.dectionCon = dectionCon
        self.trackCon = trackCon


        self.mpHands =  mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,
                                        self.dectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self,img,handNo=0,draw= True):
        handList = []
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                lmList = []
                for id,lm in enumerate(myHand.landmark):
                    h,w,c = img.shape
                    cx,cy = int(lm.x*w) , int(lm.y*h)
                    # print(f"id:{id} pos:({cx},{cy})")
                    
                    lmList.append(landmark(id,cx,cy))
                    if draw:
                        cv2.circle(img,(cx,cy),10,(0,0,255),cv2.FILLED)
                handList.append(lmList)
        return handList


def main():
    wCam, hCam = 1280,720
    cap = cv2.VideoCapture(0)  
    cap.set(3,wCam)
    cap.set(4,hCam)
    pTime = 0
    cTime = 0
    dector = handDector()
    while True:
        success, img = cap.read()
        img = dector.findHands(img)
        handList = dector.findPosition(img,draw=False)
        if len(handList) != 0:
            point = handList[0][8]
            print(f"id:{point.id} pos:({point.x},{point.y})")
        
        # show fps 
        # cTime = time.time()
        # fps = 1/(cTime-pTime)
        # pTime = cTime
        # cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)




        cv2.imshow("Image",img)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break



if __name__ == "__main__":
    main()