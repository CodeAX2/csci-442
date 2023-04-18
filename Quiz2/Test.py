import cv2
import numpy as np


def main():
    global hsvImg

    face_cascade = cv2.CascadeClassifier(
        "Quiz2/data/haarcascades/haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier("Quiz2/data/haarcascades/haarcascade_eye.xml")

    img = cv2.imread("Quiz2/Michael.jpg")
    cv2.namedWindow("Image")
    cv2.namedWindow("Gray")
    cv2.namedWindow("HSV")
    cv2.namedWindow("Modified")
    cv2.namedWindow("Subtracted")

    cv2.setMouseCallback("HSV", hsvCallback)

    # Convert to gray
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert to hsv
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Example of looping over pixels
    dim = img.shape
    img2 = img.copy()
    for y in range(dim[0]):
        for x in range(dim[1]):
            pixel = img2[y][x]
            pixelHSV = hsvImg[y][x]
            if pixelHSV[2] >= 240 and (pixelHSV[0] >= 70 or pixelHSV[0] <= 10):
                img2[y][x] = [0, 0, 0]

    # Example of subtracting images
    subImg = cv2.subtract(img, cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR))
    # In subtract order matters, in absdiff it does not

    # Example of adding images
    addImg = cv2.add(img, cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR))

    # Get face recognition
    faces = face_cascade.detectMultiScale(grayImg, 1.5, 5)
    print("Faces:", faces)
    for x, y, w, h in faces:
        # Draw face
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Get subimage (these are references, not copies)
        roi_gray = grayImg[y : y + h, x : x + w]
        roi_color = img[y : y + h, x : x + w]

        # Find eyes using subimage
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        print("Eyes:", eyes)

        for ex, ey, ew, eh in eyes:
            # Draw eyes
            cv2.rectangle(roi_color, (ex, ey), (ex + ew + 10, ey + eh), (0, 255, 0), 2)

    while True:
        # Display images
        cv2.imshow("Image", img)
        cv2.imshow("Gray", grayImg)
        cv2.imshow("HSV", hsvImg)
        cv2.imshow("Modified", img2)
        cv2.imshow("Subtracted", subImg)
        cv2.imshow("Added", addImg)

        k: int = cv2.waitKey(1)
        if k == 27:
            break

    cv2.destroyAllWindows()


def hsvCallback(event, x: int, y: int, flags, param) -> None:
    global hsvImg
    if event == cv2.EVENT_LBUTTONDOWN:
        print("HSV at (" + str(x) + ", " + str(y) + "): " + str(hsvImg[y][x]))


main()
