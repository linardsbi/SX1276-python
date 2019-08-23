from SX1276 import SX1276

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
    address = {"HEAD": 0xC0,"ADDH": 0x05,"ADDL": 0x02}
    speed = {"adr": 0b010,"baudrate": 0b011,"parity": 0b00}
    options = {"power": SX1276.Power.PWR_17DB, "FEC": 1, "wakeup": 0b011, "drive_mode": 1,"transmission_mode": 1}

    module = SX1276.begin(ports, address, speed, options)
    while True:
        sleep(0.5)
        module.sendMessage(message=[0xa,0xb,0xc,0xFFF], formatting=True, options=formatting_options)
