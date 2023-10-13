import time

from pymodbus.client import ModbusSerialClient
from src.tools.common import timeit


# from mighty_tools.common import timeit


class ModbusController(object):
    def __init__(self, address="/dev/ttyUSB0", baud_rate=38400, timeout=0.001):
        self.client = ModbusSerialClient(
            address, baudrate=baud_rate, timeout=timeout, parity="N"
        )
        self.client.connect()

    def write_coil(self, address: int, value: bool):
        """
        Write a coil to the modbus server.
            self.client.write_coil(0x01, False)
        Args:
            address: Address to write to
            value: Value to write to

        Returns:

        """
        self.client.write_coil(address, value)

    @timeit
    def execute(self, address):
        self.client.write_coil(address, True)
        time.sleep(0.1)
        self.client.write_coil(address, False)
        time.sleep(0.1)


if __name__ == "__main__":
    gas_control = ModbusController()
    # while True:
    gas_control.execute(1)
    print("a")
