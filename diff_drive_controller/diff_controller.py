from diff_driver import DiffDriver
from wheel_controller import WheelController

class DiffController(DiffDriver):
    def __init__(self, left_pins: tuple, right_pins: tuple):
        super().__init__(left_pins, right_pins)
        self.left_wheel = WheelController(*left_pins)
        self.right_wheel = WheelController(*right_pins)

    def set_velocity(self, ref_lin_vel, ref_ang_vel):
        v_l = ref_lin_vel - 0.5 * (ref_ang_vel * self.WHEEL_SEP)
        v_r = ref_lin_vel + 0.5 * (ref_ang_vel * self.WHEEL_SEP)
        self.left_wheel.set_velocity(v_l)
        self.right_wheel.set_velocity(v_r)


if __name__ == '__main__':
    from time import sleep
    bot = DiffController((10, 11, 4, 2, 6, -1), (12, 13, 5, 3, 7, 1))
    bot.set_velocity(0.3, 0.)
    for _ in range(50):
        # print(bot.lin_vel, bot.ang_vel)
        sleep(0.1)

    bot.left_wheel.controller_timer.deinit()
    bot.right_wheel.controller_timer.deinit()
    bot.stop()
