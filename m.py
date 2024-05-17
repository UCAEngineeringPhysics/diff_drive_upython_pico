from diff_driver import DiffDriver
from time import sleep

# SETUP
robot = DiffDriver((10, 11, 4, 2, 6), (12, 13, 5, 3, 7))
while True:
    print(f"{robot.lin_vel}, {robot.ang_vel}")
    sleep(0.02)

# robot.forward(0.4)
# sleep(10)
# robot.stop()
