from machine import Pin, PWM
from motor_driver import MotorDriver

class DualMotorDriver:
    def __init__(self, left_pins: tuple, right_pins: tuple) -> None:
        self.left_motor = MotorDriver(*left_pins)
        self.right_motor = MotorDriver(*right_pins)

    def forward(self, dutycycle: int):
        assert 0<=dutycycle<=65535
        self.left_motor.forward(dutycycle)
        self.right_motor.forward(dutycycle)
    
    def backward(self, dutycycle: int):
        assert 0<=dutycycle<=65535
        self.left_motor.backward(dutycycle)
        self.right_motor.backward(dutycycle)

    def spin_cw(self, dutycycle: int):
        assert 0<=dutycycle<=65535
        self.left_motor.forward(dutycycle)
        self.right_motor.backward(dutycycle)
    
    def spin_ccw(self, dutycycle: int):
        assert 0<=dutycycle<=65535
        self.left_motor.backward(dutycycle)
        self.right_motor.forward(dutycycle)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()


if __name__ == "__main__":
    from time import sleep
    dm = DualMotorDriver((16, 17), (14, 15))
    for dc in range(0, 65536, 64):
        dm.forward(dc)
        print(f"forward: {dc}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.forward(dc)
        print(f"forward: {dc}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        dm.backward(dc)
        print(f"backward: {dc}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.backward(dc)
        print(f"backward: {dc}")
        sleep(0.01)
    print("STOP!")
    for dc in range(0, 65536, 64):
        dm.spin_ccw(dc)
        print(f"spin counter-clockwise: {dc}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.spin_ccw(dc)
        print(f"spin counter-clockwise: {dc}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        dm.spin_cw(dc)
        print(f"spin clockwise: {dc}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.spin_cw(dc)
        print(f"spin clockwise: {dc}")
        sleep(0.01)
    print("STOP!")
    dm.stop()

