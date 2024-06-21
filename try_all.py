import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

current_dir = os.path.dirname(os.path.abspath(__file__))
input_video_path = os.path.join(current_dir, "Resources/Videos/lidan.mp4")

cap = cv2.VideoCapture(input_video_path)
detector = PoseDetector()

shirtFolderPath = os.path.join(current_dir, "similar_recommendation/Shirts_recommendation")
listShirts = os.listdir(shirtFolderPath)
fixedRatioShirt = 262 / 190
shirtRatioHeightWidth = 581 / 440
imageNumberShirt = 0

pantsFolderPath = os.path.join(current_dir, "similar_recommendation/Pants_recommendation")
listPants = os.listdir(pantsFolderPath)
fixedRatioPants = 232 / 100
pantsRatioHeightWidth = 581 / 250
imageNumberPants = 0

button_path = os.path.join(current_dir, "Resources/button.png")
imgButtonRight = cv2.imread(button_path, cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

# Setup output video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (frame_width, frame_height))

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)

    if lmList:
        lm11 = lmList[11][0:2]
        lm12 = lmList[12][0:2]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumberShirt]), cv2.IMREAD_UNCHANGED)
        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatioShirt)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        lm23 = lmList[23][0:2]
        lm24 = lmList[24][0:2]
        imgPant = cv2.imread(os.path.join(pantsFolderPath, listPants[imageNumberPants]), cv2.IMREAD_UNCHANGED)

        widthOfPant = int((lm23[0] - lm24[0]) * fixedRatioPants)
        imgPant = cv2.resize(imgPant, (widthOfPant, int(widthOfPant * pantsRatioHeightWidth)))
        currentScale = (lm23[0] - lm24[0]) / 100
        offset = int(60 * currentScale), int(20 * currentScale)

        try:
            img = cvzone.overlayPNG(img, imgPant, (lm24[0] - offset[0], lm24[1] - offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        # Left button for shirts
        if lmList[16][0] < 500:
            counterLeft += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0, counterLeft * selectionSpeed, (255, 192, 203), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                imageNumberShirt = (imageNumberShirt + 1) % len(listShirts)


        # Right button for pants
        elif lmList[15][0] > 900:
            counterRight += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, counterRight * selectionSpeed, (255, 192, 203), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                imageNumberPants = (imageNumberPants + 1) % len(listPants)

        else:
            counterRight = 0
            counterLeft = 0

    out.write(img)

# Release resources
cap.release()
out.release()

# display the video with "try it now" button without need for downloading the video
'''import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector


cap = cv2.VideoCapture("../Resources/Videos/lidan.mp4")
detector = PoseDetector()

#variables for the shirts
shirtFolderPath = "./Shirts_recommendation"
listShirts = os.listdir(shirtFolderPath)
fixedRatioShirt = 262 / 190
shirtRatioHeightWidth = 581 / 440
imageNumberShirt = 0


#variables for the pants
pantsFolderPath = "./Pants_recommendation"
listPants = os.listdir(pantsFolderPath)
fixedRatioPants = 232 / 100
pantsRatioHeightWidth = 581 / 250
imageNumberPants = 0

#variables for the buttons
imgButtonRight = cv2.imread("../Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10


while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)
    if lmList:
        lm11 = lmList[11][0:2]
        lm12 = lmList[12][0:2]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumberShirt]), cv2.IMREAD_UNCHANGED)
        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatioShirt)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        lm23 = lmList[23][0:2]
        lm24 = lmList[24][0:2]
        imgPant = cv2.imread(os.path.join(pantsFolderPath, listPants[imageNumberPants]), cv2.IMREAD_UNCHANGED)

        widthOfPant = int((lm23[0] - lm24[0]) * fixedRatioPants)
        imgPant = cv2.resize(imgPant, (widthOfPant, int(widthOfPant * pantsRatioHeightWidth)))
        currentScale = (lm23[0] - lm24[0]) / 100
        offset = int(60 * currentScale), int(20 * currentScale)

        try:
            img = cvzone.overlayPNG(img, imgPant, (lm24[0] - offset[0], lm24[1] - offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        # Left button for shirts
        if lmList[16][0] < 500:
            counterLeft += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0, counterLeft * selectionSpeed, (255, 192, 203), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                imageNumberShirt = (imageNumberShirt + 1) % len(listShirts)


        # Right button for pants
        elif lmList[15][0] > 900:
            counterRight += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0, counterRight * selectionSpeed, (255, 192, 203), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                imageNumberPants = (imageNumberPants + 1) % len(listPants)

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)'''