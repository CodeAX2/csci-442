import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
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

# Create the tracker
tracker = cv2.TrackerKCF_create()
initialized = False
objectDistance = 0

# Create align object
align_to = rs.stream.color
align = rs.align(align_to)

# Start streaming
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        # Align the frames
        aligned_frames = align.process(frames)

        # Get the frames
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if not initialized:
            # Initialize tracking

            bbox = (
                int(color_image.shape[1] / 2 - 50),
                int(color_image.shape[0] / 2 - 50),
                100,
                100
            )

            # Uncomment below to allow user to select tracking region
            # bbox = cv2.selectROI("Select Tracking Box", color_image, True)
            # cv2.destroyWindow("Select Tracking Box")

            # Init tracker
            tracker.init(color_image, bbox)
            initialized = True
        else:
            # Update tracking
            updated, newBBox = tracker.update(color_image)

            if updated:
                # If we didn't lose the tracking, get the distance
                bbox = newBBox
                newDistance = depth_image[int(bbox[3] / 2) + bbox[1]][
                    int(bbox[2] / 2) + bbox[0]
                ]
                # If distance is 0, invalid reading, use previous reading
                if newDistance != 0:
                    objectDistance = newDistance
                    print(objectDistance)
            else:
                # Lost tracking, restart tracker

                bbox = (
                int(color_image.shape[1] / 2 - 50),
                int(color_image.shape[0] / 2 - 50),
                100,
                100
            )

                tracker = cv2.TrackerKCF_create()
                tracker.init(color_image, bbox)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_HOT
        )

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # Draw rectangle on the color image
        if initialized:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(color_image, p1, p2, (255, 0, 0), 2, 1)

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(
                color_image,
                dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
                interpolation=cv2.INTER_AREA,
            )
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        # Create the black image
        blackImg = np.zeros_like(images)

        # Draw red box denoting the camera
        blackCenter = (int(blackImg.shape[1] * 0.5), int(blackImg.shape[0] * 0.5))
        cv2.rectangle(
            blackImg,
            (blackCenter[0] - 5, blackCenter[1] - 5),
            (blackCenter[0] + 5, blackCenter[1] + 5),
            (0, 0, 255),
            -1,
        )

        # Draw tracked object, scaling at 1/20 (this was tested in a large room), can change by modifying depthScale
        xMin = bbox[0]
        xMax = bbox[0] + bbox[2]
        imageCenter = (int(color_image.shape[1] * 0.5), int(color_image.shape[0] * 0.5))

        depthScale = 1.0/10.0

        cv2.rectangle(
            blackImg,
            (
                blackCenter[0] + xMin - imageCenter[0],
                blackCenter[1] - int(objectDistance * depthScale),
            ),
            (
                blackCenter[0] + xMax - imageCenter[0],
                blackCenter[1] - int(objectDistance * depthScale) - 3,
            ),
            (255, 0, 0),
            -1,
        )

        # Add black image to the set of images
        images = np.vstack((images, blackImg))

        # Show images
        cv2.namedWindow("RealSense", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("RealSense", images)
        k = cv2.waitKey(1)
        if k == 27:
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    pipeline.stop()
