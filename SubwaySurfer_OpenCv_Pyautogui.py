from cvzone.PoseModule import PoseDetector
import cv2
import pyautogui
# import urllib.request
# import numpy as np
# url = "http://192.168.1.41:8080/shot.jpg"
cap = cv2.VideoCapture(0)
detector = PoseDetector()

move_x = 1
move_y = 1
current_location_x = ""
current_location_y = ""
startFlag = False
right_shoulder_x = 0
left_shoulder_x = 0
right_shoulder_y = 0
left_shoulder_y = 0


while True:
    success, img = cap.read()
    # img_arr = np.array(bytearray(urllib.request.urlopen(url).read()), dtype= np.uint8)
    # img = cv2.imdecode (img_arr, -1)
    img = cv2.flip(img,1)
    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)
    height = img.shape[0]
    width = img.shape[1]
    cv2.line(img, (width//2, 0), (width//2, height), (0,0,0), 1)
    # cv2.line(img, (0, height//2-50), (width,height//2-50), (0,0,0), 3)
    # cv2.line(img, (0, height//2-50-50), (width,height//2-50-50), (0,0,0), 3)
    # cv2.line(img, (0, height//2), (width,height//2), (0,0,0), 3)
    img = detector.findPose(img)
    if bboxInfo:
        
        right_shoulder_x = lmList[11][1]
        left_shoulder_x = lmList[12][1]
        right_shoulder_y = lmList[11][2]
        left_shoulder_y = lmList[12][2]
        mid_y = (left_shoulder_y+right_shoulder_y)//2

        if startFlag == False:
            startFlag=True
            pyautogui.click(1180, 150)
        # for horizontal movement
        if left_shoulder_x<width//2 and right_shoulder_x<width//2:
            # print ("Left")
            current_location_x = "left"
        elif left_shoulder_x>width//2 and right_shoulder_x>width//2:
            current_location_x = "right"
            # print ("Right")
        elif left_shoulder_x < width//2 and right_shoulder_x > width//2:
            current_location_x = "center"
            # print ("Center")
        # for vertical movement
        if mid_y<(height//2-50)-50:
            # print ("Left")
            current_location_y = "jump"
        elif mid_y>(height//2-50)+50:
            current_location_y = "down"
            # print ("Right")
        elif mid_y < (height//2-50)+50 and mid_y > (height//2-50)-50:
            current_location_y = "standing"
            # print ("Center")

        if (current_location_x=="center" and move_x==2) or (current_location_x=="left" and move_x==1):
            # print ("move Left")
            pyautogui.press("left")
            move_x-=1
        elif (current_location_x=="right" and move_x==1) or (current_location_x=="center" and move_x==0):
            # print ("move Right")
            pyautogui.press("right")
            move_x+=1
        # elif (current_location=="right" and move_x==1) or (current_location=="center" and move_x==0)

        if (current_location_y=="jump" and move_y==1 ):
            # print ("move Up")
            pyautogui.press("up")
            move_y = 0
        elif (current_location_y=="down" and move_y==1 ):
            # print ("move Down")
            pyautogui.press("down")
            move_y = 2
        elif (current_location_y == "standing"):
            move_y=1


        # print (lmList[0]) # x = at 1 index, y at 2 index 

    cv2.imshow("Image", img)
    if cv2.waitKey(1)==27 :
        break


cap.release()
cv2.destroyAllWindows()