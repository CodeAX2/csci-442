class MotorController:
    def __init__(self) -> None:
        self.__queuedTargets = []
        pass

    def setTarget(self, channel: int, target: int) -> None:
        """
        Sets the target for a specific channel to the desired PWM value
        """
        self.__queuedTargets.append((channel, target))

    def start(self) -> None:
        """
        Begins the update loop for sending signals to the motor controller
        """
        self.__running = True
        while self.__running:
            while len(self.__queuedTargets) != 0:
                channel, target = self.__queuedTargets.pop(0)
                # TODO: Set motor target

    def stop(self) -> None:
        """
        Stops the motor controller update loop
        """
        self.__running = False
