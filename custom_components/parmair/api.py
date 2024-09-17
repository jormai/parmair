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
            "parmair_raitisilma": 1,
            "parmair_LTO_kylmapiste": 1,
            "parmair_tuloilma": 1,
            "parmair_jateilma": 1,
            "parmair_poistoilma": 1,
            "parmair_kosteusmittaus": 1,
            "parmair_CO2": 1,
            "parmair_tulopuhallin_saato": 1,
            "pa_poistopuhallin_saato": 1,
            "parmair_jalkilammitys": 1,
            "parmair_saatoasento_LTO": 1,
            "parmair_ohituslammitys": 1,
            "parmair_home_speed_s": 1,
            "parmair_TE10_MIN_HOME_S": 1,
            "parmair_TE10_CONTROL_MODE_S": 1,
            "parmair_UNIT_CONTROL_FO": 1,
            "parmair_mac_state": 1,
            "parmair_iv_nopeusasetus": 1,
            "parmair_kosteusmittauksen_24h_ka": 1
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
                    self.read_parmair_modbus
                )
                self.close()
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

    def read_parmair_modbus(self):
        """Read Modbus Data Function."""
        try:
            self.read_parmair_modbus_v2()
            result = True
            _LOGGER.debug(f"read_parmair_modbus: success {result}")
        except Exception as modbus_error:
            _LOGGER.debug(f"read_parmair_modbus: failed with error: {modbus_error}")
            result = False
            raise ModbusError() from modbus_error
        return result

    
    
    def read_parmair_modbus_v2(self):
        """Read parmair modubus V2."""
        # Max number of registers in one read for Modbus/TCP is 123
        # https://control.com/forums/threads/maximum-amount-of-holding-registers-per-request.9904/post-86251
        #
        # So we have to do 2 read-cycles, one for M1 and the other for M103+M160
        #
        # Start address 4 read 64 registers to read M1 (Common Inverter Info) in 1-pass
        # Start address 70 read 94 registers to read M103+M160 (Realtime Power/Energy Data) in 1-pass
        try:
            offset = 1020
            count = 86
            read_v2_data = self.read_holding_registers(
                slave=self._slave_id, address=(self._base_addr + offset), count=count
            )
            _LOGGER.debug(f"(read_parmair_modbus_v2) Slave ID: {self._slave_id}" )
            _LOGGER.debug("(read_parmair_modbus_v2) Base Address: %s", self._base_addr)
            _LOGGER.debug("(read_parmair_modbus_v2) Offset: %s", offset)
            _LOGGER.debug(f"(read_parmair_modbus_v2) Count: {count}")
        except ModbusException as modbus_error:
            _LOGGER.debug(f"Read read_parmair_modbus_v2 modbus_error: {modbus_error}")
            raise ModbusError() from modbus_error

        # No connection errors, we can start scraping registers
        decoder = BinaryPayloadDecoder.fromRegisters(
            read_v2_data.registers, byteorder=Endian.BIG
        )

        # register 1020
        _LOGGER.debug("(read_parmair_modbus_v2) Decoding")

        self.data["parmair_raitisilma"] = decoder.decode_16bit_int()  # Address 1020
        self.data["parmair_LTO_kylmapiste"] = decoder.decode_16bit_int()  # Address 1021
        self.data["parmair_tuloilma"] = decoder.decode_16bit_int()  # Address 1022
        self.data["parmair_jateilma"] = decoder.decode_16bit_int()  # Address 1023
        self.data["parmair_poistoilma"] = decoder.decode_16bit_int()  # Address 1024
        self.data["parmair_kosteusmittaus"] = decoder.decode_16bit_int()  # Address 1025
        self.data["parmair_CO2"] = decoder.decode_16bit_int()  # Address 1026
        decoder.skip_bytes(13*2)  # Skipping address 1027 .. 1039
        self.data["parmair_tulopuhallin_saato"] = decoder.decode_16bit_int()  # Address 1040
        decoder.skip_bytes(2)
        self.data["pa_poistopuhallin_saato"] = decoder.decode_16bit_int()  # Address 1042
        decoder.skip_bytes(2)
        self.data["parmair_jalkilammitys"] = decoder.decode_16bit_int()  # Address 1044
        decoder.skip_bytes(2)
        self.data["parmair_saatoasento_LTO"] = decoder.decode_16bit_int()  # Address 1046
        decoder.skip_bytes(2)
        self.data["parmair_ohituslammitys"] = decoder.decode_16bit_int()  # Address 1048
        decoder.skip_bytes(11*2)  # Skipping addresses 1049 - 1059
        self.data["parmair_home_speed_s"] = decoder.decode_16bit_int()  # Address 1060
        self.data["parmair_TE10_MIN_HOME_S"] = decoder.decode_16bit_int()  # Address 1061
        self.data["parmair_TE10_CONTROL_MODE_S"] = decoder.decode_16bit_int()  # Address 1062

        try:
            offset = 1180
            count = 18
            read_v2_data = self.read_holding_registers(
                slave=self._slave_id, address=(self._base_addr + offset), count=count
            )
            _LOGGER.debug("(read_parmair_modbus_v2) Slave ID: %s", self._slave_id)
            _LOGGER.debug("(read_parmair_modbus_v2) Base Address: %s", self._base_addr)
            _LOGGER.debug("(read_parmair_modbus_v2) Offset: %s", offset)
            _LOGGER.debug(f"(read_parmair_modbus_v2) Count: {count}")
        except ModbusException as modbus_error:
            _LOGGER.debug(f"Read read_parmair_modbus_v2 modbus_error: {modbus_error}")
            raise ModbusError() from modbus_error

        # No connection errors, we can start scraping registers
        decoder = BinaryPayloadDecoder.fromRegisters(
            read_v2_data.registers, byteorder=Endian.BIG
        )
        self.data["parmair_UNIT_CONTROL_FO"] = decoder.decode_16bit_int()  # Address 1180
        self.data["parmair_mac_state"] = decoder.decode_16bit_int()  # Address 1181
        decoder.skip_bytes(10)  # Skipping addresses 1182-86
        self.data["parmair_iv_nopeusasetus"] = decoder.decode_16bit_int()  # Address 1187
        self.data["parmair_kosteusmittauksen_24h_ka"] = decoder.decode_16bit_int()  # Address 1192

        _LOGGER.debug("(read_parmair_modbus_v2) Check Model # todo")
    
        _LOGGER.debug("(read_parmair_modbus_v2) Completed")
        return True
