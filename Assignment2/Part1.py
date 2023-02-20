import cv2 as cv
import numpy as np


class ObjectTracker:
    __bgrImg: cv.Mat
    __hsvImg: cv.Mat
    __thresholdImg: cv.Mat

    __capture: cv.VideoCapture

    __minScalar: np.array
    __maxScalar: np.array

    __erosionSize: int = 0
    __dilationSize: int = 0

    def __init__(self) -> None:
        self.__capture = cv.VideoCapture(0)
        # Create Windows
        cv.namedWindow("BGR")
        cv.namedWindow("HSV")
        cv.namedWindow("Threshold")
        cv.namedWindow("Trackbars")
        cv.resizeWindow("Trackbars", 250, 400)

        # Add events
        cv.setMouseCallback("BGR", self.videoCallback)
        cv.setMouseCallback("HSV", self.hsvCallback)

        # Create trackbars

        cv.createTrackbar(
            "minH",
            "Trackbars",
            0,
            255,
            lambda v: self.trackbarChanged(v, "minH"),
        )
        cv.createTrackbar(
            "maxH",
            "Trackbars",
            0,
            255,
            lambda v: self.trackbarChanged(v, "maxH"),
        )

        cv.createTrackbar(
            "minS",
            "Trackbars",
            0,
            255,
            lambda v: self.trackbarChanged(v, "minS"),
        )
        cv.createTrackbar(
            "maxS",
            "Trackbars",
            0,
            255,
            lambda v: self.trackbarChanged(v, "maxS"),
        )

        cv.createTrackbar(
            "minV",
            "Trackbars",
            0,
            255,
            lambda v: self.trackbarChanged(v, "minV"),
        )
        cv.createTrackbar(
            "maxV",
            "Trackbars",
            0,
            255,
            lambda v: self.trackbarChanged(v, "maxV"),
        )
        cv.createTrackbar(
            "dilation",
            "Trackbars",
            0,
            20,
            lambda v: self.trackbarChanged(v, "dilation"),
        )
        cv.createTrackbar(
            "erosion",
            "Trackbars",
            0,
            20,
            lambda v: self.trackbarChanged(v, "erosion"),
        )

        self.__minScalar = np.array([0, 0, 0])
        self.__maxScalar = np.array([0, 0, 0])

    def startLoop(self) -> None:
        while True:
            _, self.__bgrImg = self.__capture.read()

            self.__hsvImg = cv.cvtColor(self.__bgrImg, cv.COLOR_BGR2HSV)
            self.__thresholdImg = cv.inRange(
                self.__hsvImg, self.__minScalar, self.__maxScalar
            )

            dilateElement = cv.getStructuringElement(
                cv.MORPH_RECT,
                (2 * self.__dilationSize + 1, 2 * self.__dilationSize + 1),
                (self.__dilationSize, self.__dilationSize),
            )

            erodeElement = cv.getStructuringElement(
                cv.MORPH_RECT,
                (2 * self.__erosionSize + 1, 2 * self.__erosionSize + 1),
                (self.__erosionSize, self.__erosionSize),
            )

            self.__thresholdImg = cv.dilate(self.__thresholdImg, dilateElement)
            self.__thresholdImg = cv.erode(self.__thresholdImg, erodeElement)

            cv.imshow("BGR", self.__bgrImg)
            cv.imshow("HSV", self.__hsvImg)
            cv.imshow("Threshold", self.__thresholdImg)

            k: int = cv.waitKey(1)
            if k == 27:
                break

        cv.destroyAllWindows()

    def hsvCallback(self, event, x: int, y: int, flags, param) -> None:
        if event == cv.EVENT_LBUTTONDOWN:
            print(
                "HSV at (" + str(x) + ", " + str(y) + "): " + str(self.__hsvImg[y][x])
            )

    def videoCallback(self, event, x: int, y: int, flags, param) -> None:
        if event == cv.EVENT_LBUTTONDOWN:
            print(
                "BGR at (" + str(x) + ", " + str(y) + "): " + str(self.__bgrImg[y][x])
            )

    def trackbarChanged(self, value: int, trackbarName: str) -> None:
        # Update the corresponding element of the min/max scalar
        if trackbarName == "minH":
            self.__minScalar[0] = value
        elif trackbarName == "maxH":
            self.__maxScalar[0] = value
        elif trackbarName == "minS":
            self.__minScalar[1] = value
        elif trackbarName == "maxS":
            self.__maxScalar[1] = value
        elif trackbarName == "minV":
            self.__minScalar[2] = value
        elif trackbarName == "maxV":
            self.__maxScalar[2] = value
        elif trackbarName == "dilation":
            self.__dilationSize = value
        elif trackbarName == "erosion":
            self.__erosionSize = value


def main():
    tracker: ObjectTracker = ObjectTracker()
    tracker.startLoop()


main()
