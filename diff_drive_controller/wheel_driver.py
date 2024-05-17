from machine import Pin, PWM, Timer
from math import pi

class WheelDriver:
    # INITIALIZE
    def __init__(self, enca_pin_id, encb_pin_id, dir_pin_id, pwm_pin_id, slp_pin_id=None, ab=1):
        self.ENCA_PIN = Pin(enca_pin_id, Pin.IN)
        self.ENCB_PIN = Pin(encb_pin_id, Pin.IN)
        self.DIR_PIN = Pin(dir_pin_id, Pin.OUT)
        self.PWM_PIN = PWM(Pin(pwm_pin_id))
        self.PWM_PIN.freq(1000)
        self.SLP_PIN = Pin(slp_pin_id, Pin.OUT)
        self.SLP_PIN.value(1)
        assert abs(ab) == 1
        self.ab = ab
        # Variables
        self.inc = 0
        self.encoder_counts = 0
        self.prev_counts = 0
        self.lin_vel = 0
        # Properties
        self.WHEEL_RADIUS = 0.0375  # m
        self.GEAR_RATIO = 46.8512
        self.CPR = 48
        # Interrupt
        self.ENCA_PIN.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.inc_counts_a)
        self.ENCB_PIN.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.inc_counts_b)
        # Velocity timer
        self.velocity_timer = Timer(
            freq=100,
            mode=Timer.PERIODIC,
            callback=self.velmon_cb
        )

    def velmon_cb(self, timer):
        encoder_diff = self.encoder_counts - self.prev_counts
        ang_vel_motor = encoder_diff / self.CPR * 2 * pi * 100 # rad / s
        ang_vel_wheel = ang_vel_motor / self.GEAR_RATIO
        self.lin_vel = ang_vel_wheel * self.WHEEL_RADIUS
        self.prev_counts = self.encoder_counts

    def inc_counts_a(self, pin):
        # self.encoder_counts += self.inc
        if self.ENCA_PIN.value() == 0:
            if self.ENCB_PIN.value() == 0:
                self.encoder_counts -= self.ab
            else:  # ENCB == 1
                self.encoder_counts += self.ab
        else:  # ENCA == 1
            if self.ENCB_PIN.value() == 0:
                self.encoder_counts += self.ab
            else:
                self.encoder_counts -= self.ab

    def inc_counts_b(self, pin):
        # self.encoder_counts += self.inc
        if self.ENCA_PIN.value() == 0:
            if self.ENCB_PIN.value() == 0:
                self.encoder_counts += self.ab
            else:  # ENCB == 1
                self.encoder_counts -= self.ab
        else:  # ENCA == 1
            if self.ENCB_PIN.value() == 0:
                self.encoder_counts -= self.ab
            else:
                self.encoder_counts += self.ab

    # FUNCTION
    def forward(self, speed=0.):
        assert 0<=speed<=1
        self.DIR_PIN.value(1)
        self.PWM_PIN.duty_u16(int(65535 * speed))
        self.inc = 1
    
    def backward(self, speed=0.):
        assert 0<=speed<=1
        self.DIR_PIN.value(0)
        self.PWM_PIN.duty_u16(int(65535 * speed))
        self.inc = -1

    def stop(self):
        self.PWM_PIN.duty_u16(0)


if __name__ == "__main__":
    from time import sleep
    # wheel = WheelDriver(10, 11, 4, 2, 6, -1)  # left
    wheel = WheelDriver(12, 13, 5, 3, 7, 1)  # right
    for d in range(100):
        wheel.forward(d/100)
        print(wheel.lin_vel)
        sleep(0.05)
    for d in reversed(range(101)):
        wheel.forward(d/100)
        print(wheel.lin_vel)
        sleep(0.05)
    for d in range(100):
        wheel.backward(d/100)
        print(wheel.lin_vel)
        sleep(0.05)
    for d in reversed(range(101)):
        wheel.backward(d/100)
        print(wheel.lin_vel)
        sleep(0.05)
        
    wheel.stop()

