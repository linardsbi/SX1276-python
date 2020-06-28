from SX1276 import SX1276
from time import sleep
from pyA20.gpio import port

if __name__ == "__main__":
    # (not necessary) options for message formatting
    # "terminator" - adds 0xFF to end of message
    # "length" - adds a message length byte
    formatting_options = ["terminator", "length"]
    ports = {
            "M0":  port.PA18,
            "M1":  port.PA21,
            "AUX": port.PG8,
            "SERIAL":  "/dev/ttyS1"
            }

    # these are optional
    address = {"HEAD": 0xC0,"ADDH": 0x0,"ADDL": 0x02}
    speed = {"adr": 0b010,"baudrate": 0b011,"parity": 0b00}
    options = {"power": SX1276.Power.PWR_17DB, "FEC": 1, "wakeup": 0b011, "drive_mode": 1,"transmission_mode": 1, "channel": 0x4}

    module = SX1276.begin(ports, address, speed, options)
    print("Started.")
    i = 0
    while True:
        sleep(2)
        module.sendMessage(message=[0x0,0x1,0x4,i], formatting=True, options=formatting_options)
        i += 1
