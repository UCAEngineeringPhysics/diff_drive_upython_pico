from machine import Pin, PWM

class MotorDriver:
    def __init__(self, dir_pin_id: int, pwm_pin_id: int) -> None:
        self.DIR_PIN = Pin(dir_pin_id, Pin.OUT)
        self.PWM_PIN = PWM(Pin(pwm_pin_id))
        self.PWM_PIN.freq(1000)

    def forward(self, dutycycle: int):
        assert 0<=dutycycle<=65535
        self.DIR_PIN.value(1)
        self.PWM_PIN.duty_u16(dutycycle)
    
    def backward(self, dutycycle: int):
        assert 0<=dutycycle<=65535
        self.DIR_PIN.value(0)
        self.PWM_PIN.duty_u16(dutycycle)

    def stop(self):
        self.PWM_PIN.duty_u16(0)
    
    def halt(self):
        self.PWM_PIN.duty_u16(0)
        self.PWM_PIN.deinit()

if __name__ == "__main__":
    from time import sleep
    # m = MotorDriver(16, 17)  # left
    m = MotorDriver(14, 15)  # left
    for dc in range(0, 65536, 64):
        m.forward(dc)
        print(f"forward: {dc}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        m.forward(dc)
        print(f"forward: {dc}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        m.backward(dc)
        print(f"backward: {dc}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        m.backward(dc)
        print(f"backward: {dc}")
        sleep(0.01)
    print("STOP!")
    m.stop()

