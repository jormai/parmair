"""Parmair select."""
import logging
from . import ParmairConfigEntry
from .const import CONF_NAME, DOMAIN, GROUPS, SensorSpec
from .const import SENSOR_DICT
from .coordinator import ParmairCoordinator
from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory, generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

def add_sensor_defs(
    coordinator: ParmairCoordinator,
    config_entry: ParmairConfigEntry,
    sensor_list
):
    """Class Initializitation."""

    for sensor in SENSOR_DICT.items():
        if sensor[1].platform == Platform.SELECT:
            sensor_list.append(
                ParmairSelect(coordinator, config_entry, sensor)
            )

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ParmairConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Sensor Platform setup."""

    # Get handler to coordinator from config
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator

    _LOGGER.debug("(select) Name: %s", config_entry.data.get(CONF_NAME))
    _LOGGER.debug("(select) FW Version: %s", coordinator.api.data["MULTI_FW_VER"])
    _LOGGER.debug("(select) SW Version: %s", coordinator.api.data["MULTI_SW_VER"])
    _LOGGER.debug("(select) BL Version: %s", coordinator.api.data["MULTI_BL_VER"])
    _LOGGER.debug("(select) Vent machine type code #: %s", coordinator.api.data["VENT_MACHINE"])

    sensor_list = []
    add_sensor_defs(coordinator, config_entry, sensor_list)

    async_add_entities(sensor_list)

    return True


class ParmairSelect(CoordinatorEntity, SelectEntity):
    """Representation of an Parmair select sensor."""

    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data:tuple[str,SensorSpec]):
        """Class Initializitation."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._key = sensor_data[0]
        # no name defined for the sensor since uses translated name
        # set to use translated name
        self._attr_has_entity_name = True
        self.entity_id = generate_entity_id("select.{}", sensor_data[1].name, hass=coordinator.hass)
        self._attr_translation_key = sensor_data[1].name

        self._spec = sensor_data[1]
        self._attr_unique_id = f"{config_entry.unique_id}-{self._key}"
        self._attr_unit_of_measurement =  self._spec.unit
        self._attr_icon = self._spec.icon
        self._attr_device_class = self._spec.sensor_device_class
        self._attr_entity_category = EntityCategory.DIAGNOSTIC if self._spec.sensor_device_class is None else None
        self._attr_should_poll = False
        # To link this entity the Parmair device
        self._attr_device_info = {"identifiers": {(DOMAIN,  f"{config_entry.unique_id}-{GROUPS[sensor_data[1].group]}")}}
        self._current_index = 0
        self._current_index = int(self._coordinator.api.data[self._key])
        self._attr_options = sensor_data[1].options


    @property
    def current_option(self) -> str:
        """Get the current option."""
        return self._spec.options[self._current_index]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._current_index = int(self._coordinator.api.data[self._key])
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

    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        if not self._spec.writeable:
            _LOGGER.warning(f"Read only entity {self._key}")
            return
        if self._spec.options is None:
            _LOGGER.warning(f"Options are not defined for {self._key}")
            return
        try:
            selected = self.options.index(option)
            result = await self._coordinator.async_write_data(self._key, selected)
            _LOGGER.debug(f"Selected option {selected} for {self._key}, set value result {result}")
        except ValueError:
            _LOGGER.warning(f"Option {option} was not found in {self._key}")
            return
