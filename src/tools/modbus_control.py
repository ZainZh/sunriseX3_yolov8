from pymodbus.client import ModbusSerialClient
# from mighty_tools.common import timeit


class ModbusController(object):
    def __init__(self):
        self.client = ModbusSerialClient("/dev/ttyUSB0", baudrate=9600, timeout=0.1, parity="N")
        self.client.connect()

    # @timeit
    def close_gas(self):
        print("Gas is closed")
        self.client.write_coil(0x00, True)

    # @timeit
    def open_gas(self):
        print("Gas is opened")
        self.client.write_coil(0x00, False)

    # @timeit
    def start_conveyor(self):
        print("Conveyor is started")
        self.client.write_coil(0x01, False)

    # @timeit
    def stop_conveyor(self):
        print("Conveyor is stopped")
        self.client.write_coil(0x01, True)


if __name__ == "__main__":
    gas_control = ModbusController()
    # gas_control.stop_conveyor()
    gas_control.open_gas()
    # gas_control.close_gas()
    # gas_control.start_conveyor()
    print("a")
