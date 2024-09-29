"""Support for Parmair number."""

from __future__ import annotations

from dataclasses import dataclass
import logging


from config.custom_components.parmair.coordinator import ParmairCoordinator
from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.components.number.const import NumberDeviceClass
from homeassistant.const import CONF_NAME, EntityCategory, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ParmairConfigEntry
from .const import DOMAIN, SENSOR_DICT, SensorSpec


_LOGGER = logging.getLogger(__name__)

def add_sensor_defs(
    coordinator: ParmairCoordinator,
    config_entry: ParmairConfigEntry,
    sensor_list
):
    """Class Initializitation."""

    for sensor in SENSOR_DICT.items():
        if sensor[1].platform == Platform.NUMBER:
            sensor_list.append(ParmairNumber(coordinator, config_entry, sensor))

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ParmairConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up Parmair numbers."""
    sensor_list = []
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator

    _LOGGER.debug("(select) Name: %s", config_entry.data.get(CONF_NAME))
    _LOGGER.debug("(select) FW Version: %s", coordinator.api.data["MULTI_FW_VER"])
    _LOGGER.debug("(select) SW Version: %s", coordinator.api.data["MULTI_SW_VER"])
    _LOGGER.debug("(select) BL Version: %s", coordinator.api.data["MULTI_BL_VER"])
    _LOGGER.debug("(select) Vent machine type code #: %s", coordinator.api.data["VENT_MACHINE"])

    add_sensor_defs(coordinator, config_entry, sensor_list)
    async_add_entities(sensor_list)

class ParmairNumber(CoordinatorEntity, NumberEntity):
    """Parmair number."""
    
    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data:tuple[str,SensorSpec]):
        """Class Initializitation."""
        _LOGGER.debug(f"ParmairNumber {sensor_data[0]}")
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
        self._attr_device_info = {"identifiers": {(DOMAIN,  config_entry.unique_id)}}
        self._attr_should_poll = False
        self._attr_native_step = 1
        self._attr_native_min_value = float(sensor_data[1].min_limit)
        self._attr_native_max_value=float(sensor_data[1].max_limit)
        self._attr_mode=NumberMode.BOX


    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self._key not in self._coordinator.api.data:
            return None
        if (svalue := self._coordinator.api.data[self._key]) is not None:
            return int(svalue)
        return None
            
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


    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        if self._spec.writeable == False:
            return
        
        reg_value = int(value*self._spec.multiplier)
        result = await self._coordinator.api.async_write_data(self._spec.id, reg_value)
        _LOGGER.debug(f"Setting value for {self._key}, result {result}")
        if result == True:
            self._coordinator.api.data[self._key] = f"{value}"


