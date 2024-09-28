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

from . import ParmairConfigEntry
from .const import SENSOR_DICT, SensorSpec



@dataclass(frozen=True, kw_only=True)
class ParmairNumberDescription(NumberEntityDescription):
    """Class describing Parmair sensor entities."""
    multiplier: int
    coordinator: ParmairCoordinator
    writeable: bool

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

class ParmairNumber(NumberEntity):
    """Parmair number."""
    entity_description: ParmairNumberDescription

    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data:tuple[str,SensorSpec]):
        """Class Initializitation."""
        _LOGGER.debug(f"ParmairNumber {sensor_data[0]}")
        #super().__init__(coordinator)
        self.entity_description = ParmairNumberDescription(
            key=sensor_data[0],
            translation_key=sensor_data[0],
            native_step=1,
            native_min_value=float(sensor_data[1].min_limit),
            native_max_value=float(sensor_data[1].max_limit),
            entity_category=EntityCategory.CONFIG if sensor_data[1].writeable==True else EntityCategory.DIAGNOSTIC,
            native_unit_of_measurement=sensor_data[1].unit,
            multiplier=int(sensor_data[1].multiplier),
            mode=NumberMode.BOX,
            coordinator=coordinator,
            writeable=sensor_data[1].writeable,
            device_class=sensor_data[1].sensor_device_class
        )
    
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

    @callback
    def _async_update_attrs(self) -> None:
        """Update attrs from device."""
        if (value := self._coordinator.api.data[self.entity_description.key]) is not None:
            value = value / self.entity_description.multiplier
            self._attr_native_value = float(value)

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        if self.entity_description.writeable == False:
            return
        _LOGGER.debug(f"TODO: Set value for {self.entity_description.key} {value}x{self.entity_description.multiplier}")
        #setattr(self._device, self.entity_description.key, int(value))
