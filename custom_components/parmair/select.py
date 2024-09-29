import logging
from typing import Any
from custom_components.parmair import ParmairConfigEntry
from custom_components.parmair.api import ParmairAPI
from custom_components.parmair.const import CONF_NAME, DOMAIN, SensorSpec
from custom_components.parmair.const import SENSOR_DICT
from custom_components.parmair.coordinator import ParmairCoordinator
from homeassistant.components.select import SelectEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import Platform

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
)
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
    """Representation of an Parmair binart sensor."""

    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data:tuple[str,SensorSpec]):
        """Class Initializitation."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._key = sensor_data[0]
        self._spec = sensor_data[1]
        self._attr_name = sensor_data[1].comment
        self._attr_unique_id = f"{config_entry.unique_id}-{self._key}"
        self._attr_translation_key = self._key
        self._attr_unit_of_measurement =  self._spec.unit
        self._attr_icon = self._spec.icon
        self._attr_device_class = self._spec.sensor_device_class
        self._attr_entity_category = EntityCategory.DIAGNOSTIC if self._spec.sensor_device_class is None else None
        self._attr_should_poll = False
        # To link this entity the Parmair device
        self._attr_device_info = {"identifiers": {(DOMAIN,  config_entry.unique_id)}}
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
        if self._spec.writeable == False:
            _LOGGER.warning(f"Read only entity {self._key}")
            return
        if self._spec.options == None:
            _LOGGER.warning(f"Options are not defined for {self._key}")
            return
        try:
            selected = self.options.index(option)
            result = await self._coordinator.api.async_write_data(self._spec.id, selected)
            _LOGGER.debug(f"Selected option {selected} for {self._key}, set value result {result}")
            if result == True:
                self._coordinator.api.data[self._key] = f"{selected}"
            _LOGGER.debug(f"TODO: Selected option {selected} for {self._key}")
        except ValueError:
            _LOGGER.warning(f"Option {option} was not found in {self._key}")
            return
        