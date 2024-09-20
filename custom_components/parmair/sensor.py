import logging
from typing import Any
from custom_components.parmair import ParmairConfigEntry
from custom_components.parmair.api import ParmairAPI
from custom_components.parmair.const import CONF_NAME, DOMAIN, SensorSpec
from custom_components.parmair.const import SENSOR_DICT
from custom_components.parmair.coordinator import ParmairCoordinator
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
_LOGGER = logging.getLogger(__name__)

def add_sensor_defs(
    coordinator: ParmairCoordinator,
    config_entry: ParmairConfigEntry,
    sensor_list
):
    """Class Initializitation."""

    for sensor in SENSOR_DICT.items():        
        sensor_list.append(
            ParmairSensor(coordinator, config_entry, sensor)
        )

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ParmairConfigEntry, async_add_entities
):
    """Sensor Platform setup."""

    # Get handler to coordinator from config
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator

    _LOGGER.debug("(sensor) Name: %s", config_entry.data.get(CONF_NAME))
    _LOGGER.debug("(sensor) FW Version: %s", coordinator.api.data["MULTI_FW_VER"])
    _LOGGER.debug("(sensor) SW Version: %s", coordinator.api.data["MULTI_SW_VER"])
    _LOGGER.debug("(sensor) BL Version: %s", coordinator.api.data["MULTI_BL_VER"])
    _LOGGER.debug("(sensor) Vent machine type code #: %s", coordinator.api.data["VENT_MACHINE"])

    sensor_list = []
    add_sensor_defs(coordinator, config_entry, sensor_list)

    async_add_entities(sensor_list)

    return True


class ParmairSensor(CoordinatorEntity, SensorEntity):
    """Representation of an ABB SunSpec Modbus sensor."""

    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data:tuple[str,SensorSpec]):
        """Class Initializitation."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = sensor_data[0]
        self._spec = sensor_data[1]
        self._device_name = self._coordinator.api.name
        self._device_host = self._coordinator.api.host
        self._device_model = self._coordinator.api.data["VENT_MACHINE"]
        self._device_manufact = self._coordinator.api.data["comm_manufact"]
        self._device_sn = self._coordinator.api.data["VENT_MACHINE"]
        self._device_swver = self._coordinator.api.data["MULTI_SW_VER"]
        self._device_hwver = self._coordinator.api.data["MULTI_FW_VER"]


    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._state = self._coordinator.api.data[self._key]
        self.async_write_ha_state()
        # write debug log only on first sensor to avoid spamming the log
        if self.name == "Manufacturer":
            _LOGGER.debug(
                "_handle_coordinator_update: sensors state written to state machine"
            )

    @property
    def has_entity_name(self):
        """Return the name state."""
        return True

    @property
    def name(self):
        """Return the name."""
        return f"{self._name}"

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._spec.unit

    @property
    def icon(self):
        """Return the sensor icon."""
        return self._spec.icon

    @property
    def device_class(self):
        """Return the sensor device_class."""
        return self._spec.sensor_device_class

    @property
    def state_class(self):
        """Return the sensor state_class."""
        if self._spec.sensor_device_class == None:
            return None
        return SensorStateClass.MEASUREMENT

    @property
    def entity_category(self):
        """Return the sensor entity_category."""
        if self._state_class is None:
            return EntityCategory.DIAGNOSTIC
        else:
            return None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self._name in self._coordinator.api.data:
            return self._coordinator.api.data[self._name]
        else:
            return None

    @property
    def state_attributes(self) -> dict[str, Any] | None:
        """Return the attributes."""
        return None

    @property
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self._device_model}_{self._name}"

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "configuration_url": f"http://{self._device_host}",
            "hw_version": None,
            "identifiers": {(DOMAIN, self._device_sn)},
            "manufacturer": self._device_manufact,
            "model": self._device_model,
            "name": self._device_name,
            "serial_number": self._device_sn,
            "sw_version": self._device_swver,
            "via_device": None,
        }
