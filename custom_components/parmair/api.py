"""API Platform for ABB Power-One PVI SunSpec.

https://github.com/alexdelprete/ha-abb-powerone-pvi-sunspec
"""

import logging
import socket
import threading

from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException, ModbusException
from pymodbus.payload import BinaryPayloadDecoder

from .const import SENSOR_DICT

_LOGGER = logging.getLogger(__name__)


class ConnectionError(Exception):
    """Empty Error Class."""

    pass


class ModbusError(Exception):
    """Empty Error Class."""

    pass


class ParmairAPI:
    """Thread safe wrapper class for pymodbus."""

    def __init__(
        self,
        hass,
        name,
        host,
        port,
        slave_id,
        base_addr,
        scan_interval,
    ):
        """Initialize the Modbus API Client."""
        self._hass = hass
        self._name = name
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self._base_addr = base_addr
        self._update_interval = scan_interval
        # Ensure ModBus Timeout is 1s less than scan_interval
        # https://github.com/binsentsu/home-assistant-solaredge-modbus/pull/183
        self._timeout = self._update_interval - 1
        self._client = ModbusTcpClient(
            host=self._host, port=self._port, timeout=self._timeout
        )
        self._lock = threading.Lock()
        self._sensors = []
        self.data = {}
        # Initialize ModBus data structure before first read
        self.data = {
            "comm_sernum": "1",
            "comm_manufact": "Parmair"
        }

    @property
    def name(self):
        """Return the device name."""
        return self._name

    @property
    def host(self):
        """Return the device name."""
        return self._host

    def check_port(self) -> bool:
        """Check if port is available."""
        with self._lock:
            sock_timeout = float(3)
            _LOGGER.debug(
                f"Check_Port: opening socket on {self._host}:{self._port} with a {sock_timeout}s timeout."
            )
            socket.setdefaulttimeout(sock_timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_res = sock.connect_ex((self._host, self._port))
            is_open = sock_res == 0  # True if open, False if not
            if is_open:
                sock.shutdown(socket.SHUT_RDWR)
                _LOGGER.debug(
                    f"Check_Port (SUCCESS): port open on {self._host}:{self._port}"
                )
            else:
                _LOGGER.debug(
                    f"Check_Port (ERROR): port not available on {self._host}:{self._port} - error: {sock_res}"
                )
            sock.close()
        return is_open

    def close(self):
        """Disconnect client."""
        try:
            if self._client.is_socket_open():
                _LOGGER.debug("Closing Modbus TCP connection")
                with self._lock:
                    self._client.close()
                    return True
            else:
                _LOGGER.debug("Modbus TCP connection already closed")
        except ConnectionException as connect_error:
            _LOGGER.debug(f"Close Connection connect_error: {connect_error}")
            raise ConnectionError() from connect_error

    def connect(self):
        """Connect client."""
        _LOGGER.debug(
            f"API Client connect to IP: {self._host} port: {self._port} slave id: {self._slave_id} timeout: {self._timeout}"
        )
        if self.check_port():
            _LOGGER.debug("Inverter ready for Modbus TCP connection")
            try:
                with self._lock:
                    self._client.connect()
                if not self._client.connected:
                    raise ConnectionError(
                        f"Failed to connect to {self._host}:{self._port} slave id {self._slave_id} timeout: {self._timeout}"
                    )
                else:
                    _LOGGER.debug("Modbus TCP Client connected")
                    return True
            except ModbusException:
                raise ConnectionError(
                    f"Failed to connect to {self._host}:{self._port} slave id {self._slave_id} timeout: {self._timeout}"
                )
        else:
            _LOGGER.debug("Inverter not ready for Modbus TCP connection")
            raise ConnectionError(f"Inverter not active on {self._host}:{self._port}")

    def read_holding_registers(self, slave, address, count):
        """Read holding registers."""
        kwargs = {"slave": slave} if slave else {}
        try:
            with self._lock:
                return self._client.read_holding_registers(address, count, **kwargs)
        except ConnectionException as connect_error:
            _LOGGER.debug(f"Read Holding Registers connect_error: {connect_error}")
            raise ConnectionError() from connect_error
        except ModbusException as modbus_error:
            _LOGGER.debug(f"Read Holding Registers modbus_error: {modbus_error}")
            raise ModbusError() from modbus_error

    def calculate_value(self, value, scalefactor):
        """Apply Scale Factor."""
        return value * 10**scalefactor

    async def async_get_data(self):
        """Read Data Function."""

        try:
            if self.connect():
                _LOGGER.debug(
                    "Start Get data (Slave ID: %s - Base Address: %s)",
                    self._slave_id,
                    self._base_addr,
                )
                # HA way to call a sync function from async function
                # https://developers.home-assistant.io/docs/asyncio_working_with_async?#calling-sync-functions-from-async
                result = await self._hass.async_add_executor_job(
                    self.read_modbus_registers
                )
                _LOGGER.debug("End Get data")
                if result:
                    _LOGGER.debug("Get Data Result: valid")
                    return True
                else:
                    _LOGGER.debug("Get Data Result: invalid")
                    return False
            else:
                _LOGGER.debug("Get Data failed: client not connected")
                return False
        except ConnectionException as connect_error:
            _LOGGER.debug(f"Async Get Data connect_error: {connect_error}")
            raise ConnectionError() from connect_error
        except ModbusException as modbus_error:
            _LOGGER.debug(f"Async Get Data modbus_error: {modbus_error}")
            raise ModbusError() from modbus_error
        finally:
            self.close()
    

    def read_modbus_registers(self)-> bool:
        """Read the Modbus registers in chunks of up to 64 contiguous addresses."""
        # Extract all addresses (ids)
        count = 64
        last_value = list(SENSOR_DICT.values())[-1].id
        first_value = list(SENSOR_DICT.values())[0].id
        it = iter(SENSOR_DICT.keys())
        key = next(it)
        result = True
        try:
            loop = 0
            for start_address in range(first_value, last_value + 1, count):
                _LOGGER.debug(f"(read_parmair_modbus_v2) loop {loop} first_value {first_value} last {last_value} start {start_address}" )
                _LOGGER.debug(f"(read_parmair_modbus_v2) Slave ID: {self._slave_id}" )
                _LOGGER.debug("(read_parmair_modbus_v2) Base Address: %s", self._base_addr)
                _LOGGER.debug(f"(read_parmair_modbus_v2) Count: {count}")
                # Read registers from Modbus
                read_data = self._client.read_holding_registers(start_address+self._base_addr, count)
                
                # Process the result (store or print the values here)
                _LOGGER.debug(f"Read registers from {start_address} to {start_address + count - 1}: {read_data} : {read_data.registers}")
                
                decoder = BinaryPayloadDecoder.fromRegisters(read_data.registers, byteorder=Endian.BIG)
                
                try:
                    for i in range(0, count):
                        register = first_value + loop * count + i
                        if SENSOR_DICT[key].id == register:
                            self.data[key] = decoder.decode_16bit_int()
                            if (SENSOR_DICT[key].multiplier != 1):
                                self.data[key] = self.data[key] / SENSOR_DICT[key].multiplier
                            _LOGGER.debug(f"reg {register}:{key} = {self.data[key]}. m={SENSOR_DICT[key].multiplier}. {SENSOR_DICT[key].comment}")
                            key = next(it)
                        else:
                            _LOGGER.debug(f"Skipping {register}")
                            decoder.skip_bytes(2)
                except StopIteration:
                    _LOGGER.debug("all sensor items handled")
                    break
                loop+=1
                    
        except Exception as modbus_error:
            _LOGGER.debug(f"read_parmair_modbus: failed with error: {modbus_error}")
            result = False
            raise ModbusError() from modbus_error
        return result

    async def async_write_data_with_key(self, key: str, value: int) -> bool:
        """Write Modbus register."""
        if key not in SENSOR_DICT:
            raise KeyError(key)
        register_address = SENSOR_DICT[key].id
        try:
            if self.connect():
                _LOGGER.debug(
                    "Start Get data (Slave ID: %s - Base Address: %s)",
                    self._slave_id,
                    self._base_addr,
                )
                reg_value = value * SENSOR_DICT[key].multiplier
                response = self._client.write_register(self._base_addr+register_address, reg_value)
                # Check if the write was successful
                if response.isError():
                    _LOGGER.debug(f"Error writing to register {register_address}")
                    return False
                else:
                    _LOGGER.debug(f"Successfully wrote {value}:native={reg_value} to register {register_address}")
                    self.data[key] = value
                    return True
            else:
                _LOGGER.debug("Get Data failed: client not connected")
        except ConnectionException as connect_error:
            _LOGGER.debug(f"Async Get Data connect_error: {connect_error}")
            raise ConnectionError() from connect_error
        except ModbusException as modbus_error:
            _LOGGER.debug(f"Async Get Data modbus_error: {modbus_error}")
            raise ModbusError() from modbus_error
        finally:
            # Close the connection
            self.close()        