from custom_components.parmair.api import ParmairAPI
from custom_components.parmair.coordinator import ParmairCoordinator
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

def add_sensor_defs(
    coordinator: ParmairCoordinator,
    config_entry: ParmairAPI,
    sensor_list,
    sensor_definitions,
):
    """Class Initializitation."""

    for sensor_info in sensor_definitions.values():
        sensor_data = {
            "name": sensor_info[0],
            "key": sensor_info[1],
            "unit": sensor_info[2],
            "icon": sensor_info[3],
            "device_class": sensor_info[4],
            "state_class": sensor_info[5],
        }
        sensor_list.append(
            ParmairSensor(coordinator, config_entry, sensor_data)
        )

class ParmairSensor(CoordinatorEntity, SensorEntity):
    """Representation of an ABB SunSpec Modbus sensor."""

    def __init__(self, coordinator, config_entry, sensor_data):
        """Class Initializitation."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = sensor_data["name"]
        self._key = sensor_data["key"]
        self._unit_of_measurement = sensor_data["unit"]
        self._icon = sensor_data["icon"]
        self._device_class = sensor_data["device_class"]
        self._state_class = sensor_data["state_class"]
        self._device_name = self._coordinator.api.name
        self._device_host = self._coordinator.api.host
        self._device_model = self._coordinator.api.data["comm_model"]
        self._device_manufact = self._coordinator.api.data["comm_manufact"]
        self._device_sn = self._coordinator.api.data["comm_sernum"]
        self._device_swver = self._coordinator.api.data["comm_version"]
        self._device_hwver = self._coordinator.api.data["comm_options"]

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
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return the sensor icon."""
        return self._icon

    @property
    def device_class(self):
        """Return the sensor device_class."""
        return self._device_class

    @property
    def state_class(self):
        """Return the sensor state_class."""
        return self._state_class

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
        if self._key in self._coordinator.api.data:
            return self._coordinator.api.data[self._key]
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
        return f"{self._device_sn}_{self._key}"

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
