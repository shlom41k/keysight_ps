import serial
import serial.tools.list_ports

from time import sleep

from settings.settings import commands as cmd


class PowerSupply:
    """
    Class for work with device COM-port
    """

    # COM port parameters
    parity_params = {
        "None": serial.PARITY_NONE,
        "Even": serial.PARITY_EVEN,
        "Odd": serial.PARITY_ODD,
        "Mark": serial.PARITY_MARK,
        "Space": serial.PARITY_SPACE,
    }

    bytesize = {
        5: serial.FIVEBITS,
        6: serial.SIXBITS,
        7: serial.SEVENBITS,
        8: serial.EIGHTBITS,
    }

    stopbits = {
        1: serial.STOPBITS_ONE,
        1.5: serial.STOPBITS_ONE_POINT_FIVE,
        2: serial.STOPBITS_TWO,
    }

    # List of commands
    commands = cmd

    # coding
    coding = "ascii"

    def __init__(self, port: str, baudrate: int, bytesize: int, stop_bits: int, parity: str):
        self.port = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=self.__class__.bytesize.get(bytesize),
            stopbits=self.__class__.stopbits.get(stop_bits),
            parity=self.__class__.parity_params.get(parity),
        )

    def connect(self):
        if not self.port.isOpen():
            self.port.open()
            sleep(0.1)
            self.port.reset_input_buffer()
            self.port.reset_output_buffer()
            sleep(0.1)

    def disconnect(self):
        if self.port.isOpen():
            self.port.close()

    def send_message(self, message: str):
        self.port.write(bytes(f"{message}\n", self.__class__.coding))
        sleep(0.1)

    def get_message(self) -> str:
        return self.port.read_all().decode(encoding=self.__class__.coding).rstrip("\n")

    def get_raw_message(self) -> str:
        return self.port.read_all().decode(encoding=self.__class__.coding)

    def get_info(self) -> str:
        """
        Get info about power supply device
        """
        self.send_message(self.__class__.commands.get("ID"))
        sleep(0.1)
        return self.get_message()

    def device_reset(self):
        self.send_message(self.__class__.commands.get("reset"))
        sleep(0.1)

    def set_current(self, current: float):
        self.send_message(self.__class__.commands.get("set_current").format(round(current, 3)))
        sleep(0.1)

    def get_current(self) -> str:
        self.send_message(self.__class__.commands.get("get_current"))
        sleep(0.1)
        return self.get_message()

    def set_voltage(self, voltage: float):
        self.send_message(self.__class__.commands.get("set_voltage").format(round(voltage, 3)))
        sleep(0.1)

    def get_voltage(self) -> str:
        self.send_message(self.__class__.commands.get("get_voltage"))
        sleep(0.1)
        return self.get_message()

    def set_output(self, out: str):
        self.send_message(self.__class__.commands.get("set_output").format(out.lower()))
        sleep(0.05)

    def get_voltage_range(self):
        self.send_message(self.__class__.commands.get("get_voltage_range"))
        sleep(0.1)
        return self.get_message()

    def set_voltage_low(self):
        self.send_message(self.__class__.commands.get("set_voltage_low"))
        sleep(0.1)

    def set_voltage_high(self):
        self.send_message(self.__class__.commands.get("set_voltage_high"))
        sleep(0.1)

    @staticmethod
    def get_com_ports() -> dict:
        """
        Get all COM-ports
        """
        ports = dict()

        for port, desc, _ in sorted(serial.tools.list_ports.comports()):
            ports[port] = desc

        return ports


if __name__ == "__main__":

    print(PowerSupply.get_com_ports())

    agilent = PowerSupply(
        port="COM11",
        baudrate=9600,
        bytesize=8,
        stop_bits=2,
        parity="None",
    )

    agilent.connect()
    print(agilent.get_info())
    agilent.device_reset()

    agilent.set_current(0.1)
    agilent.set_voltage(12)
    sleep(1)
    agilent.set_output("on")
    sleep(2)
    print(float(agilent.get_current()))
    print(float(agilent.get_voltage()))
    agilent.set_output("off")
    sleep(1)
    agilent.send_message("VOLTage:RANGe?")
    sleep(0.1)
    print(agilent.get_message())
    sleep(1)
    agilent.send_message("VOLTage:RANGe HIGH")
    sleep(0.1)
    agilent.send_message("DISPlay on")
    agilent.send_message("DISPlay:TEXT:CLEar")
    agilent.send_message("DISPlay:TEXT?")
    agilent.send_message(f'DISP:STATe?')
    print(agilent.get_raw_message())
    agilent.send_message("DISPlay off")




    agilent.disconnect()



