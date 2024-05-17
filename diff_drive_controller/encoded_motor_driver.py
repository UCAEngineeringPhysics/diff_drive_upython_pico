from machine import Pin
from motor_driver import MotorDriver

class EncodedMotorDriver(MotorDriver):
    def __init__(self, 
        dir_pin_id: int, 
        pwm_pin_id: int, 
        enca_pin_id: int, 
        encb_pin_id: int,
    ) -> None:
        super().__init__(dir_pin_id, pwm_pin_id)
        self.ENCA_PIN = Pin(enca_pin_id, Pin.IN, Pin.PULL_DOWN)
        self.ENCA_PIN.irq(trigger=Pin.IRQ_RISING, handler=self.inc_enca_counts)
        self.ENCB_PIN = Pin(encb_pin_id, Pin.IN, Pin.PULL_DOWN)
        self.ENCB_PIN.irq(trigger=Pin.IRQ_RISING, handler=self.inc_encb_counts)
        # Variables
        self.enca_counts = 0
        self.encb_counts = 0

    def inc_enca_counts(self, pin):
        self.enca_counts += 1

    def inc_encb_counts(self, pin):
        self.encb_counts += 1


if __name__ == "__main__":
    machine.freq(250_000_000)
    from time import sleep
    # m = EncodedMotorDriver(16, 17, 18, 19)  # left
    m = EncodedMotorDriver(14, 15, 12, 13)  # right
    for dc in range(0, 65536, 64):
        m.forward(dc)
        print(f"f- dutycycle: {dc}, enca counts: {m.enca_counts}, encb counts: {m.encb_counts}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        m.forward(dc)
        print(f"f- dutycycle: {dc}, enca counts: {m.enca_counts}, encb counts: {m.encb_counts}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        m.backward(dc)
        print(f"b- dutycycle: {dc}, enca counts: {m.enca_counts}, encb counts: {m.encb_counts}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        m.backward(dc)
        print(f"b- dutycycle: {dc}, enca counts: {m.enca_counts}, encb counts: {m.encb_counts}")
        sleep(0.01)
    print("STOP!")
    m.stop()
    print(f"Working CPU freq: {machine.freq()}")
    machine.freq(125_000_000)
    print(f"Rest CPU freq: {machine.freq()}")
