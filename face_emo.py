import cv2
from fer import FER
# detector = FER(mtcnn=True)
detector = FER() 


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    ret, image = cap.read()


    try:

        print(detector.top_emotion(image))
    except:
        pass


    k = cv2.waitKey(0) & 0xFF
    if k == 27:  # esc key ends process
        cap.release()
        break


cv2.destroyAllWindows()