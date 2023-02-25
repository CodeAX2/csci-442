import cv2 as cv
import numpy as np


class MotionTracker:
    # The base image
    __bgrImg: cv.Mat

    # The various images used for motion capture
    __grayImg: cv.Mat
    __curDst: cv.Mat
    __capture1: cv.Mat
    __absDiffImg: cv.Mat
    __contourImg: cv.Mat

    __capture: cv.VideoCapture

    def __init__(self) -> None:
        self.__capture = cv.VideoCapture(0)
        # Create Windows
        cv.namedWindow("Original")
        cv.namedWindow("Difference")
        cv.namedWindow("Threshold")
        cv.namedWindow("Contours")

        # Capture initial image (step 1)
        _, self.__bgrImg = self.__capture.read()

        # Create blank images (step 2)
        self.__grayImg = np.zeros_like(self.__bgrImg)
        self.__curDst = np.zeros_like(self.__bgrImg, dtype=np.float32)
        self.__capture1 = np.zeros_like(self.__bgrImg)
        self.__absDiffImg = np.zeros_like(self.__bgrImg)
        self.__contourImg = np.zeros_like(self.__bgrImg)

    def startLoop(self) -> None:
        # Loop (step 3)
        while True:
            # Grab frame (step 4)
            _, self.__bgrImg = self.__capture.read()

            # Brighten image (step 4.1)
            self.__bgrImg = cv.convertScaleAbs(self.__bgrImg, 1, 1.25)

            # Copy image
            self.__capture1 = self.__bgrImg.copy()

            # Blur image (step 5)
            blured = cv.blur(self.__capture1, (3, 3))

            # Convert to 32f
            blured = np.float32(blured)

            # Accumulate Weighted (step 6)
            self.__curDst = cv.accumulateWeighted(blured, self.__curDst, 0.5)

            # Convert back to 8bit (step 7)
            self.__capture1 = cv.convertScaleAbs(self.__curDst)

            # Get abs diff (step 8)
            self.__absDiffImg = cv.absdiff(self.__capture1, self.__bgrImg)

            # Convert to grayscale (step 9)
            self.__absDiffImg = cv.cvtColor(self.__absDiffImg, cv.COLOR_BGR2GRAY)

            # Threshold (low number, step 10)
            self.__grayImg = cv.inRange(self.__absDiffImg, 20, 255)

            # Blur (step 11)
            self.__grayImg = cv.blur(self.__grayImg, (15, 15))

            # Threshold (high number, step 12)
            self.__grayImg = cv.inRange(self.__grayImg, 120, 255)

            # Find contours (step 13)
            contours, _ = cv.findContours(
                self.__grayImg, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE
            )

            # Make contour image white and draw contours
            self.__contourImg.fill(255)

            # Find blobs/rectangles from contours (step 14)
            i = 0
            for contour in contours:
                # Cutoff for small contours
                if contour.size <= 75:
                    i = i + 1
                    continue
                # Draw contours of blobs (step 15)
                cv.drawContours(self.__contourImg, contours, i, (0, 0, 0), -1)

                # Draw rectangles (step 16)
                x, y, w, h = cv.boundingRect(contour)
                cv.rectangle(self.__bgrImg, (x, y), (x + w, y + h), (0, 0, 255), 2)
                i = i + 1

            # Draw images
            cv.imshow("Original", self.__bgrImg)
            cv.imshow("Difference", self.__absDiffImg)
            cv.imshow("Threshold", self.__grayImg)
            cv.imshow("Contours", self.__contourImg)

            # Exit with esc
            k: int = cv.waitKey(1)
            if k == 27:
                break

        cv.destroyAllWindows()

# Create the program
def main():
    tracker: MotionTracker = MotionTracker()
    tracker.startLoop()


main()
