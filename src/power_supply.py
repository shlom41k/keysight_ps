import serial
import serial.tools.list_ports

from time import sleep, time

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

    def send_message(self, message: str, send_delay=True):
        self.port.write(bytes(f"{message}\n", self.__class__.coding))
        if send_delay:
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
        # sleep(0.1)

    def set_current(self, current: float):
        self.send_message(self.__class__.commands.get("set_current").format(round(current, 3)))
        # sleep(0.1)

    def get_current(self) -> str:
        self.send_message(self.__class__.commands.get("get_current"))
        # sleep(0.1)
        return self.get_message()

    def get_current_limit(self) -> str:
        self.send_message(self.__class__.commands.get("get_current_limit"))
        # sleep(0.2)
        return self.get_message()

    def set_voltage(self, voltage: float):
        self.send_message(self.__class__.commands.get("set_voltage").format(round(voltage, 3)))
        # sleep(0.1)

    def get_voltage(self) -> str:
        self.send_message(self.__class__.commands.get("get_voltage"))
        # sleep(0.1)
        return self.get_message()

    def get_voltage_limit(self) -> str:
        self.send_message(self.__class__.commands.get("get_voltage_limit"))
        # sleep(0.2)
        return self.get_message()

    def set_output(self, out: str, set_delay=True):
        d = True if set_delay else False
        self.send_message(self.__class__.commands.get("set_output").format(out.lower()), send_delay=d)
        if d:
            sleep(0.05)

    def get_voltage_range(self):
        self.send_message(self.__class__.commands.get("get_voltage_range"))
        # sleep(0.1)
        return self.get_message().rstrip()

    def set_voltage_low(self):
        self.send_message(self.__class__.commands.get("set_voltage_low"))
        # sleep(0.1)

    def set_voltage_high(self):
        self.send_message(self.__class__.commands.get("set_voltage_high"))
        # sleep(0.1)

    def beep(self):
        self.send_message(self.__class__.commands.get("beep"))

    def get_dev_version(self) -> str:
        self.send_message(self.__class__.commands.get("version"))
        return self.get_message()

    def get_dev_errors(self) -> str:
        self.send_message(self.__class__.commands.get("get_errors"))
        return self.get_message()

    def set_local_control(self):
        self.send_message(self.__class__.commands.get("set_local_control"))

    def set_remote_control(self):
        self.send_message(self.__class__.commands.get("set_remote_control"))

    def set_display(self, out: str):
        self.send_message(self.__class__.commands.get("set_display").format(out.lower()))

    def clear_display(self):
        self.send_message(self.__class__.commands.get("clear_display"))

    def display_text(self, text: str):
        self.send_message(self.__class__.commands.get("display_text").format(text))

    def save_state(self, state: int):
        self.send_message(self.__class__.commands.get("save_state").format(f"{state}"))

    def load_state(self, state: int):
        self.send_message(self.__class__.commands.get("load_state").format(f"{state}"))

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

    # Create devices
    agilent_12V = PowerSupply(
        port="COM8",
        baudrate=9600,
        bytesize=8,
        stop_bits=2,
        parity="None",
    )

    """
    agilent_5V = PowerSupply(
        port="COM8",
        baudrate=9600,
        bytesize=8,
        stop_bits=2,
        parity="None",
    )
    """
    agilent_12V.connect()
    agilent_12V.device_reset()
    agilent_12V.set_current(0.2)
    agilent_12V.send_message("VOLTage:RANGe HIGN")
    agilent_12V.set_voltage(60)

    """
    agilent_5V.connect()
    agilent_5V.device_reset()
    agilent_5V.send_message("VOLTage:RANGe LOW")
    agilent_5V.set_current(1.5)
    agilent_5V.set_voltage(5)
    """


    #start_time = time()
    agilent_12V.set_output("on", set_delay=False)
    sleep(0.5)
    agilent_12V.set_voltage(27)
    sleep(2)
    agilent_12V.set_output("off")
    #end_time = time() - start_time
    # agilent_5V.set_output("on", set_delay=False)
    #print(end_time)

    while True:
        e = input("Press '0' for DISABLE output: ")
        if e == "0":
            break

    #agilent_12V.set_output("off")
    #agilent_5V.set_output("off")

    print("Output OFF")

    agilent_12V.disconnect()
    #agilent_5V.disconnect()



