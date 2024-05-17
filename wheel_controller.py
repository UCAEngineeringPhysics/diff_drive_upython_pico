from wheel_driver import WheelDriver
from machine import Timer

class WheelController(WheelDriver):
    def __init__(self, enca_pin_id, encb_pin_id, dir_pin_id, pwm_pin_id, slp_pin_id=None, ab=1):
        super().__init__(enca_pin_id, encb_pin_id, dir_pin_id, pwm_pin_id, slp_pin_id, ab)
        self.dc = 0.
        self.err = 0.
        self.prev_err = 0.
        # Constants
        self.K_P = 0.1
        self.K_I = 0.01
        self.K_D = 0.05
        self.controller_timer = Timer()
        self.controller_timer.init(
            mode=Timer.PERIODIC, 
            freq=100, 
            callback=self.velcon_cb
        )

    def velcon_cb(self, timer):
        self.err = self.ref_vel - self.lin_vel
        self.err_sum += self.err  # err_sum = err_sum + err
        self.err_diff = self.err - self.prev_err
        self.prev_err = self.err
        dc_inc = self.K_P * self.err + self.K_I * self.err_sum + self.K_D * self.err_diff  # Proportional, Integral, Derivative
        self.dc += dc_inc
        if self.dc > 0:  # forward
            if self.dc >= 1:
                self.dc = 0.999
            self.forward(self.dc)
        elif self.dc < 0:  # backward
            if self.dc <= -1:
                self.dc = -0.999
            self.backward(-self.dc)
        else:
            self.stop()
        if self.ref_vel == 0:
            self.dc = 0.
            self.stop()

    def set_velocity(self, ref):
        self.ref_vel = ref
        self.err_sum = 0.

if __name__=='__main__':
    from time import sleep
    # wheel = WheelController(10, 11, 4, 2, 6, -1)  # left
    wheel = WheelController(12, 13, 5, 3, 7, 1)
    for v in range(50):
        wheel.set_velocity(0.3)
        print(f"target vel: {wheel.ref_vel}, actual vel: {wheel.lin_vel}, duty cycle: {wheel.dc}")
        sleep(0.1)
    # for d in range(100):
    #     wheel.set_velocity(d/100)
    #     print(f"target vel: {wheel.ref_vel}, actual vel: {wheel.lin_vel}, duty cycle: {wheel.dc}")
    #     sleep(0.05)
    # for d in reversed(range(101)):
    #     wheel.set_velocity(d/100)
    #     print(f"target vel: {wheel.ref_vel}, actual vel: {wheel.lin_vel}, duty cycle: {wheel.dc}")
    #     sleep(0.05)
    # for d in range(100):
    #     wheel.set_velocity(-d/100)
    #     print(f"target vel: {wheel.ref_vel}, actual vel: {wheel.lin_vel}, duty cycle: {wheel.dc}")
    #     sleep(0.05)
    # for d in reversed(range(101)):
    #     wheel.set_velocity(-d/100)
    #     print(f"target vel: {wheel.ref_vel}, actual vel: {wheel.lin_vel}, duty cycle: {wheel.dc}")
    #     sleep(0.05)

    wheel.controller_timer.deinit()
    wheel.stop()