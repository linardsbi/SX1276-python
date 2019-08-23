from pyA20.gpio import gpio
from pyA20.gpio import port
import serial
from time import sleep

gpio.init()

required_ports = ["M0", "M1", "AUX", "SERIAL"] 
default_address = {"HEAD": 0xC0,"ADDH": 0x01,"ADDL": 0x02}
default_speed = {"adr": 0b010,"baudrate": 0b011,"parity": 0b00}
default_options = {"power": 0x02, "FEC": 1, "wakeup": 0b000, "drive_mode": 1,"transmission_mode": 1, "channel": 0x82}

class SX1276:
    __ports = {}
    __serial = None

    # 410~441MHz: 410M + CHAN*1M
    # 855~880.5MHz: 855 + channel * 0.1M
    # eg. channel val (in decimal) = 441 - 410 * 1M 
    #     channel val (in decimal) = (880.5 - 855) * 10M
    class Channel:
        CHN_410 = 0x00
        CHN_433 = 0x17
        CHN_441 = 0x1F
        CHN_855 = 0x00
        CHN_868 = 0x82
        CHN_880 = 0xFF

    class Power:
        PWR_20DB = 0x00
        PWR_17DB = 0x01
        PWR_14DB = 0x02
        PWR_10DB = 0x03

    class Mode:
        NORMAL = 0
        WAKEUP = 1
        POWERSAVE = 2
        SLEEP = 3

    def __init__(self, ports):
        self.__ports = ports

    def __clearBuffer(self):
       self.__serial.flushInput()
       self.__serial.flushOutput()

    @classmethod
    def begin(cls, ports, address=default_address, speed=default_speed, options=default_options):
        module = cls(ports)
 
        module.configPorts()
        
        # override defaults with provided
        tmp = {**default_address}
        tmp.update(address)
        address = {**tmp}

        tmp = {**default_speed}
        tmp.update(speed)
        speed = {**tmp}

        tmp = {**default_options}
        tmp.update(options)
        options = {**tmp}

        # bitwise magic!
        SPED = int(speed["parity"] << 6 | speed["baudrate"] << 3 | speed["adr"])
        CHAN = options["channel"]
        OPTION = int(options["transmission_mode"] << 7 | options["drive_mode"] << 6 | options["wakeup"] << 3 | options["FEC"] << 2 | options["power"])
        
        parameters = [address["HEAD"], address["ADDH"], address["ADDL"],SPED,CHAN, OPTION]
        
        module.changeMode(SX1276.Mode.SLEEP)
        module.__writeParameters(parameters)
        module.__resetModule()

        module.__clearBuffer()

        return module

    def configPorts(self):
        for port in required_ports:
            if port not in self.__ports:
                raise ValueError("Missing port: {}".format(port))

        gpio.setcfg(self.__ports["M0"], gpio.OUTPUT)
        gpio.setcfg(self.__ports["M1"], gpio.OUTPUT)
        gpio.setcfg(self.__ports["AUX"], gpio.INPUT)
        
        try:
            self.__serial = serial.Serial(port=self.__ports["SERIAL"], baudrate=9600, timeout=0.5)
        except Exception as e:
            print("Serial error. {} - check README.MD to fix".format(e))
            exit()

    def sendMessage(self, message):
        pass

    def messageAvailable(self):
        return self.busy()

    def getMessage(self):
        return self.__readBuffer()

    def changeMode(self, mode):
        if (mode == self.Mode.NORMAL):
            gpio.output(self.__ports["M0"], gpio.LOW)
            gpio.output(self.__ports["M1"], gpio.LOW)
        elif (mode == self.Mode.WAKEUP):
            gpio.output(self.__ports["M0"], gpio.HIGH)
            gpio.output(self.__ports["M1"], gpio.LOW)
        elif (mode == self.Mode.POWERSAVE):
            gpio.output(self.__ports["M0"], gpio.LOW)
            gpio.output(self.__ports["M1"], gpio.HIGH)
        elif (mode == self.Mode.SLEEP):
            gpio.output(self.__ports["M0"], gpio.HIGH)
            gpio.output(self.__ports["M1"], gpio.HIGH)
    
        while self.busy():
            sleep(0.05)

    def __readBuffer(self):
        data = []

        while True:
            line = ""
            line = self.__serial.readline()
            
            if not line: break
            data = ["%02x" % i for i in list(line)]
        
        return list(data)

    def getParameters(self):
        self.changeMode(self.Mode.SLEEP)

        self.__writeParameters([0xC1,0xC1,0xC1])
        sleep(1)
        return self.__readBuffer()

    def getVersion(self):
        self.changeMode(self.Mode.SLEEP)

        self.__writeParameters([0xC3,0xC3,0xC3])

        return self.__readBuffer()
    
    def busy(self):
        return not gpio.input(self.__ports["AUX"])

    def __resetModule(self):
        self.changeMode(self.Mode.SLEEP)
        self.__writeParameters([0xC4,0xC4,0xC4])
        sleep(1)
        while self.busy():
            sleep(0.05)

    def __writeParameters(self,parameters):
        assert(type(parameters) == list)
        self.__serial.write(bytes(parameters))

ports = {
         "M0":  port.PA18,
         "M1":  port.PA21,
         "AUX": port.PG8,
         "SERIAL":  "/dev/ttyS1"}

address = {"HEAD": 0xC0,"ADDH": 0x05,"ADDL": 0x02}
speed = {"adr": 0b010,"baudrate": 0b011,"parity": 0b00}
options = {"power": SX1276.Power.PWR_17DB, "FEC": 1, "wakeup": 0b011, "drive_mode": 1,"transmission_mode": 1}

module = SX1276.begin(ports, address, options=options)
print(module.getParameters())
print(module.getVersion())
module.changeMode(SX1276.Mode.NORMAL)
print("Started. Waiting for messages.")
while True:
    if module.messageAvailable():
        message = module.getMessage()
        print("Received message: {}".format(message))
