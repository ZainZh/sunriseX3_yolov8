from pymodbus.client import ModbusSerialClient


# from mighty_tools.common import timeit


class ModbusController(object):
    def __init__(self, address="/dev/ttyUSB0", baud_rate=9600, timeout=0.1):
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

if __name__ == "__main__":
    gas_control = ModbusController()
    gas_control.write_coil(1, False)
    print("a")
