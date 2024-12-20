"""Parmair sensor."""
import logging
from . import ParmairConfigEntry
from .const import CONF_NAME, DOMAIN, GROUPS, SensorSpec
from .const import SENSOR_DICT
from .coordinator import ParmairCoordinator
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory, generate_entity_id
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import CoordinatorEntity
_LOGGER = logging.getLogger(__name__)

def add_sensor_defs(
    coordinator: ParmairCoordinator,
    config_entry: ParmairConfigEntry,
    sensor_list
):
    """Class Initializitation."""

    for sensor in SENSOR_DICT.items():
        if sensor[1].platform == Platform.SENSOR:
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
    """Representation of an sensor."""

    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data:tuple[str,SensorSpec]):
        """Class Initializitation."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._key = sensor_data[0]
        spec = sensor_data[1]
        self._unit = spec.unit

        # no name defined for the sensor since uses translated name
        # set to use translated name
        self._attr_has_entity_name = True
        self.entity_id = generate_entity_id("sensor.{}", sensor_data[1].name, hass=coordinator.hass)
        self._attr_translation_key = sensor_data[1].name

        self._attr_unique_id = f"{config_entry.unique_id}-{self._key}"

        self._attr_native_unit_of_measurement = spec.unit
        self._attr_icon = spec.icon
        self._attr_device_class = spec.sensor_device_class
        self._attr_entity_category = EntityCategory.DIAGNOSTIC if spec.sensor_device_class is None else None
        self._attr_should_poll = False

        # To link this entity the Parmair device
        self._attr_device_info = {"identifiers": {(DOMAIN,  f"{config_entry.unique_id}-{GROUPS[spec.group]}")}}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor."""
        if self._key not in self._coordinator.api.data:
            return
        self._state = self._coordinator.api.data[self._key]
        self.async_write_ha_state()
        # write debug log only on first sensor to avoid spamming the log
        if self.name == "Manufacturer":
            _LOGGER.debug(
                "_handle_coordinator_update: sensors state written to state machine"
            )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self._key in self._coordinator.api.data:
            return self._coordinator.api.data[self._key]
        else:
            return None
