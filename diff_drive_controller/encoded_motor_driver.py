from machine import Pin
from motor_driver import MotorDriver

class EncodedMotorDriver(MotorDriver):
    def __init__(self, 
        dir_pin_id: int, 
        pwm_pin_id: int, 
        enca_pin_id: int, 
        # encb_pin_id: int,
    ) -> None:
        super().__init__(dir_pin_id, pwm_pin_id)
        self.ENCA_PIN = Pin(enca_pin_id, Pin.IN, Pin.PULL_DOWN)
        self.ENCA_PIN.irq(trigger=Pin.IRQ_RISING, handler=self.increment_counter)
        # self.ENCB_PIN = Pin(encb_pin_id, Pin.IN, Pin.PULL_DOWN)
        # Variables
        self.enc_counter = 0

    def increment_counter(self, pin):
        self.enc_counter += 1

    
if __name__ == "__main__":
    from time import sleep
    # m = EncodedMotorDriver(16, 17, 18)  # left
    m = EncodedMotorDriver(14, 15, 12)  # right
    for dc in range(0, 65536, 64):
        m.forward(dc)
        print(f"forward: {m.enc_counter}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        m.forward(dc)
        print(f"forward: {m.enc_counter}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        m.backward(dc)
        print(f"backward: {m.enc_counter}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        m.backward(dc)
        print(f"backward: {m.enc_counter}")
        sleep(0.01)
    print("STOP!")
    m.stop()
