import cv2
import handTracking


def main():
    wCam, hCam = 1920,1080
    cap = cv2.VideoCapture(0)  
    cap.set(3,wCam)
    cap.set(4,hCam)
    pTime = 0
    cTime = 0
    dector = handTracking.handDector()
    while True:
        success, img = cap.read()
        img = dector.findHands(img,draw=False)
        handList = dector.findPosition(img,draw=False)
        if len(handList) != 0:

            for hand in handList:

                fingers = []

                # Thumb
                fingers.append(hand[5].y > hand[4].y)
                # 4 Fingers
                for finger in [8,12,16,20]:
                    fingers.append(hand[finger].y < hand[finger-2].y)

                print(fingers)
                    


        cv2.imshow("Image",img)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break



if __name__ == "__main__":
    main()