import MotorController as mc
import FrameBuffer as fb
import numpy as np
import cv2
import threading


class LineFollower:
    def __init__(
        self, motorController: mc.MotorController, frameBuffer: fb.FrameBuffer
    ) -> None:
        self.__motorController = motorController
        self.__frameBuffer = frameBuffer

    def start(self) -> None:
        """
        Begins the main loop of the line follower
        """
        # Begin the threads
        mcThread = threading.Thread(target=self.__motorController.start)
        mcThread.start()

        bufferThread = threading.Thread(target=self.__frameBuffer.start)
        bufferThread.start()

        # Init things here

        # Start main loop
        try:
            while True:
                if not self.__loopIter():
                    break
        finally:
            # Stop the sub-threads
            self.__motorController.stop()
            self.__frameBuffer.stop()

            mcThread.join()
            bufferThread.join()

    def __loopIter(self) -> bool:
        """
        Calls logic for an iteration of the loop.
        Returns false to signify the loop should end
        """

        # TODO: Actually implement line follower logic

        # Get images
        depth_image = self.__frameBuffer.getLastDepth()
        color_image = self.__frameBuffer.getLastColor()

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_image = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_HOT
        )

        # Get sizes of images
        depth_image_dim = depth_image.shape
        color_image_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_image_dim != color_image_dim:
            resized_color_image = cv2.resize(
                color_image,
                dsize=(depth_image_dim[1], depth_image_dim[0]),
                interpolation=cv2.INTER_AREA,
            )
            images = np.hstack((resized_color_image, depth_image_dim))
        else:
            images = np.hstack((color_image, depth_image_dim))

        # Set robot speed to move forward
        self.__motorController.setTarget(1, 7000)

        # Show images
        cv2.namedWindow("RealSense", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("RealSense", images)
        k = cv2.waitKey(1)
        if k == 27:
            cv2.destroyAllWindows()
            # Should exit loop
            return False

        return True
