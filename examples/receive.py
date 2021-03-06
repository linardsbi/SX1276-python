from SX1276 import SX1276
from pyA20.gpio import port
if __name__ == "__main__":

    ports = {
        "M0":  port.PA18,
        "M1":  port.PA21,
        "AUX": port.PG8,
        "SERIAL":  "/dev/ttyS1"
        }

    address = {"HEAD": 0xC0,"ADDH": 0x0,"ADDL": 0x03}
    speed = {"adr": 0b010,"baudrate": 0b011,"parity": 0b00}
    options = {"power": 0b1, "FEC": 1, "wakeup": 0, "drive_mode": 1,"transmission_mode": 1, "channel": 0x4}

    module = SX1276.begin(ports, address, options=options)
    
    print(module.getParameters())
    print(module.getVersion())
    
    module.changeMode(SX1276.Mode.NORMAL)
    
    print("Started. Waiting for messages.")
    
    while True:
        if module.messageAvailable():
            message = module.getMessage()
            if message: 
                print("Received message: {}".format(message))
                module.sendMessage([0x0,0x1,0x4,0xFF])
