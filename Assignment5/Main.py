import FrameBuffer as fb
import MotorController as mc
import LineFollower as lf

# Create the controller and buffer
motorController = mc.MotorController()
buffer = fb.FrameBuffer()

# Run the line follower
lineFollower = lf.LineFollower(motorController, buffer)
lineFollower.start()