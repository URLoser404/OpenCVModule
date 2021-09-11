import cv2 as cv
import mediapipe as mp
import time


class PoseDetector():

    def __init__(self , mode=False , upBody = False , smooth = True,detectionCon = 0.5 , trackCon = 0.5):


        self.mode  = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
    
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.upBody,self.smooth,self.detectionCon,self.trackCon)

    def findPose(self, img,draw = True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img ,draw = True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c, = img.shape

                cx, cy = int(lm.x * w) , int(lm.y * h)
                lmList.append({
                    "id" : id,
                    "x" : cx,
                    "cy" : cy 
                })
                if draw:
                    cv.circle(img,(cx,cy) , 5 , (255,0,0),cv.FILLED)
        return lmList


wCam, hCam = 1920,1080
cap = cv.VideoCapture(0)  
cap.set(3,wCam)
cap.set(4,hCam)


detector = PoseDetector(detectionCon=1,trackCon=1)

def main():
    while True:
        img = cv.imread(r"D:\data\coding\test files\python_testing\Pose\85d.jpg")
        img = detector.findPose(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            # print(lmList)
            pass

        
        if cv.waitKey(1) == ord('q'):
            cap.release()
            cv.destroyAllWindows()
            break
        cv.imshow("image" ,img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()