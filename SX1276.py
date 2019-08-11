from pyA20.gpio import gpio
from pyA20.gpio import port
import serial
import time.sleep

gpio.init()

ports = {
         "M0":  port.PA18,
         "M1":  port.PA21,
         "AUX": port.PG8,
         "UART":  "/dev/ttyS1"}

address = {"HEAD": 0xC0,"ADDH": 0x01,"ADDL": 0x02}
speed = {"adr": 0b010,"baudrate": 0b011,"parity": 0b00}
options = {"power": TransmitPower.PWR_17DB, "FEC": 1, "wakeup": 0b000, "drive_mode": 1,"transmission_mode": 1}

# 410~441MHz : 410M + CHAN*1M
# 855~880.5MHz : 855 + channel * 0.1M
# eg. channel val (in decimal) = 441 - 410 * 1M || channel val (dec) = (880.5 - 855) * 10M

module = SX1276.begin(ports, address, speed, options)

class ChannelType:
    channel_410 = 0x00
    channel_433 = 0x17
    channel_441 = 0x1F
    channel_855 = 0x00
    channel_868 = 0x82
    channel_880 = 0xFF
class TransmitPower:
    PWR_20DB = 0x00
    PWR_17DB = 0x01
    PWR_14DB = 0x02
    PWR_10DB = 0x03
class ModuleMode:
    NORMAL = 0
    WAKEUP = 1
    POWERSAVE = 2
    SLEEP = 3

required_ports = ["M0", "M1", "AUX", "SERIAL"] 
default_address = {"HEAD": 0xC0,"ADDH": 0x01,"ADDL": 0x02}
default_speed = {"adr": 0b010,"baudrate": 0b011,"parity": 0b00}
default_options = {"power": TransmitPower.PWR_17DB, "FEC": 1, "wakeup": 0b000, "drive_mode": 1,"transmission_mode": 1, "channel": ChannelType.channel_868}

class SX1276:
    __ports = {}

    def begin(ports, address, speed, options):
        __configPorts(ports)

        # override defaults with specified
        address = dict(default_address.items() + address.items())
        speed = dict(default_speed.items() + speed.items())
        options = dict(default_options.items() + options.items())
        
        # bitwise magic!
        SPED = hex(speed["parity"] << 6 | speed["baudrate"] << 3 | speed["adr"])
        CHAN = options["channel"]
        OPTION = hex(options["transmission_mode"] << 7 | options["drive_mode"] << 6 | options["wakeup"] << 3 | options["FEC"] << 2 | options["power"])

        parameters = [address["HEAD"], address["ADDH"], address["ADDL"],SPED, CHAN, OPTION]
        __writeParameters(parameters)

        return self

    def __configPorts(ports):
        for port in required_ports:
            if port not in ports:
                raise ValueError("Missing port: {}".format(port))

        gpio.setcfg(ports["M0"], gpio.OUTPUT)
        gpio.setcfg(ports["M1"], gpio.OUTPUT)
        gpio.setcfg(ports["AUX"], gpio.INPUT)
        serial.Serial(port=ports["SERIAL"], baudrate=9600)
        
        __ports = ports

    def sendMessage(message):
        pass
    def receiveMessage():
        return ""
    def changeMode(mode):
        if (mode == ModuleMode.NORMAL):
            gpio.output(__ports["M0"], port.LOW)
            gpio.output(__ports["M1"], port.LOW)
        elif (mode == ModuleMode.WAKEUP):
            gpio.output(__ports["M0"], port.HIGH)
            gpio.output(__ports["M1"], port.LOW)
        elif (mode == ModuleMode.POWERSAVE):
            gpio.output(__ports["M0"], port.LOW)
            gpio.output(__ports["M1"], port.HIGH)
        elif (mode == ModuleMode.SLEEP):
            gpio.output(__ports["M0"], port.HIGH)
            gpio.output(__ports["M1"], port.HIGH)
        
        sleep(0.1)            

    def __readBuffer():
        data = ""

        while True:
            line = ""
            line = serial.readline()
            
            if line == "": break

            data += line
        return data


    def getParameters():
         __writeParameters([0xC1,0xC1,0xC1])
        sleep(0.1)

        return __getBuffer()

    def getVersion():
        __writeParameters([0xC3,0xC3,0xC3])
        sleep(0.1)

        return __getBuffer()
    
    def __resetModule():
        __writeParameters([0xC4,0xC4,0xC4])
        
        sleep(1.2)

    def __writeParameters(parameters):
        assert(type(parameters) == list)

        serial.write(parameters)
