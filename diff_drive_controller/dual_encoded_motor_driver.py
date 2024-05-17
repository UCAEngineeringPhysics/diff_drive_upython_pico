from encoded_motor_driver import EncodedMotorDriver

class DualEncodedMotorDriver:
    """
    A combination of 2 EncodedMotorDriver objects. 
    Controls both motors speed and reads encoders counts.
    """
    def __init__(self, left_pins: tuple, right_pins: tuple) -> None:
        self.left_motor = EncodedMotorDriver(*left_pins)
        self.right_motor = EncodedMotorDriver(*right_pins)

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
    machine.freq(250_000_000)
    from time import sleep
    dm = DualEncodedMotorDriver((16, 17, 18, 19), (14, 15, 12, 13))
    for dc in range(0, 65536, 64):
        dm.forward(dc)
        print(f"f- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.forward(dc)
        print(f"f- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        dm.backward(dc)
        print(f"b- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.backward(dc)
        print(f"b- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        dm.spin_ccw(dc)
        print(f"ccw- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.spin_ccw(dc)
        print(f"ccw- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    for dc in range(0, 65536, 64):
        dm.spin_cw(dc)
        print(f"cw- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    for dc in reversed(range(0, 65536, 64)):
        dm.spin_cw(dc)
        print(f"cw- dc: {dc}, la: {dm.left_motor.enca_counts}, lb: {dm.left_motor.encb_counts}, ra: {dm.right_motor.enca_counts}, rb: {dm.right_motor.encb_counts}")
        sleep(0.01)
    print("STOP!")
    dm.stop()
    print(f"Working CPU freq: {machine.freq()}")
    machine.freq(25_000_000)
    print(f"Rest CPU freq: {machine.freq()}")

