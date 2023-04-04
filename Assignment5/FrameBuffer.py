import pyrealsense2 as rs
import numpy as np

class FrameBuffer:
    def __init__(self) -> None:
        self.__initCamera()
        pass

    def __initCamera(self) -> None:
        """
        Initializes the camera and polls the first frame
        """
        self.__pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.__pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # Look for camera
        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == "RGB Camera":
                found_rgb = True
                break
        if not found_rgb:
            print("Camera not found!")
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == "L500":
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Create align object
        align_to = rs.stream.color
        self.__align = rs.align(align_to)

        # Start streaming
        self.__pipeline.start(config)

        # Poll one frame of images
        self.__pollImages()

    def __pollImages(self) -> None:
        """
        Polls a single frame of images and saves them into __last_depth_image and __last_color_image
        """
        # Wait for a coherent pair of frames: depth and color
        frames = self.__pipeline.wait_for_frames()

        # Align the frames
        aligned_frames = self.__align.process(frames)

        # Get the frames
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            return

        # Convert images to numpy arrays
        self.__last_depth_image = np.asanyarray(depth_frame.get_data())
        self.__last_color_image = np.asanyarray(color_frame.get_data())

    def start(self) -> None:
        """
        Begins the continuous loop of polling images
        """
        self.__running = True

        while self.__running:
            self.__pollImages()

        self.__pipeline.stop()

    def stop(self) -> None:
        """
        Stops the polling loop
        """
        self.__running = False

    def getLastDepth(self):
        """
        Returns the last polled depth image
        """
        return self.__last_depth_image

    def getLastColor(self):
        """
        Returns the last polled color image
        """
        return self.__last_color_image
