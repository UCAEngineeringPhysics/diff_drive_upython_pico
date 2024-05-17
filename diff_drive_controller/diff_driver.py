from machine import Timer
from wheel_driver import WheelDriver
from time import sleep

class DiffDriver:
    def __init__(self, left_pins: tuple, right_pins: tuple):
        # Create wheels
        self.left_wheel = WheelDriver(*left_pins)
        self.right_wheel = WheelDriver(*right_pins)
        # Properties
        self.WHEEL_SEP = 0.207  # meters
        # Variables
        self.lin_vel = 0.
        self.ang_vel = 0.
        # Timer
        self.velocity_timer = Timer(
            freq=100,
            mode=Timer.PERIODIC,
            callback=self.velcomp_cb
        )

    def velcomp_cb(self, timer):
        self.lin_vel = (self.left_wheel.lin_vel + self.right_wheel.lin_vel) / 2
        self.ang_vel = (self.right_wheel.lin_vel - self.left_wheel.lin_vel) / self.WHEEL_SEP
        # print(f"{self.lin_vel}, {self.ang_vel}")
    
    def forward(self, speed=0.):
        assert 0<=speed<=1
        self.left_wheel.forward(speed)
        self.right_wheel.forward(speed)      
    
    def backward(self, speed=0.):
        assert 0<=speed<=1
        self.left_wheel.backward(speed)
        self.right_wheel.backward(speed)      
    
    def left_spin(self, speed=0.):
        assert 0<=speed<=1
        self.left_wheel.backward(speed)
        self.right_wheel.forward(speed)      
    
    def right_spin(self, speed=0.):
        assert 0<=speed<=1
        self.left_wheel.forward(speed)
        self.right_wheel.backward(speed)      
    
    def stop(self):
        self.left_wheel.stop()
        self.right_wheel.stop()      

if __name__ == '__main__':
    driver = DiffDriver((10, 11, 4, 2, 6, -1), (12, 13, 5, 3, 7, 1))
    for _ in range(25):
        driver.left_wheel.backward(0.55)
        driver.right_wheel.forward(0.45)
        sleep(0.2)
        print(driver.lin_vel, driver.ang_vel)
    driver.stop()
