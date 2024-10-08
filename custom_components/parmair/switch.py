"""Parmair switch."""
import logging
from typing import Any
from . import ParmairConfigEntry
from .const import CONF_NAME, DOMAIN, GROUPS, SensorSpec
from .const import SENSOR_DICT
from .coordinator import ParmairCoordinator
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import Platform

from homeassistant.components.switch import (
    SwitchEntity,
)
_LOGGER = logging.getLogger(__name__)

def add_sensor_defs(
    coordinator: ParmairCoordinator,
    config_entry: ParmairConfigEntry,
    sensor_list
):
    """Class Initializitation."""

    for sensor in SENSOR_DICT.items():
        if sensor[1].platform == Platform.SWITCH:
            sensor_list.append(
                ParmairSwitch(coordinator, config_entry, sensor)
            )

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ParmairConfigEntry, async_add_entities
):
    """Sensor Platform setup."""

    # Get handler to coordinator from config
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator

    _LOGGER.debug("(switch) Name: %s", config_entry.data.get(CONF_NAME))

    sensor_list = []
    add_sensor_defs(coordinator, config_entry, sensor_list)

    async_add_entities(sensor_list)

    return True


class ParmairSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of an Parmair binart sensor."""

    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data:tuple[str,SensorSpec]):
        """Class Initializitation."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._spec = sensor_data[1]
        self._key = sensor_data[0]
        # no name defined for the sensor since uses translated name
        # set to use translated name
        self._attr_has_entity_name = True
        self.entity_id = generate_entity_id("switch.{}", sensor_data[1].name, hass=coordinator.hass)
        self._attr_translation_key = sensor_data[1].name

        self._attr_unique_id = f"{config_entry.unique_id}-{self._key}"
        #self._attr_entity_category = EntityCategory.DIAGNOSTIC if self._spec.sensor_device_class is None else None
        self._attr_should_poll = False
        # To link this entity the Parmair device
        self._attr_device_info = {"identifiers": {(DOMAIN,  f"{config_entry.unique_id}-{GROUPS[sensor_data[1].group]}")}}


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
    def native_value(self):
        """Return the state of the sensor."""
        if self._key in self._coordinator.api.data:
            return self._coordinator.api.data[self._key]
        else:
            return None

    @property
    def is_on(self):
        """Return the state of the sensor."""
        if self._key in self._coordinator.api.data:
            return int(self._coordinator.api.data[self._key])>0
        else:
            return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """turn_on the switch."""
        result = await self._coordinator.async_write_data(self._key, 1)
        _LOGGER.debug(f"Turn on {self._key}, set value result {result}")
        #if result == True:
        #    await self.coordinator.async_request_refresh()
        _LOGGER.debug(f"data {self._coordinator.api.data[self._key]}")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """turn_off the switch."""
        result = await self._coordinator.async_write_data(self._key, 0)
        _LOGGER.debug(f"Turn off {self._key}, set value result {result}")
        #if result == True:
        #    await self.coordinator.async_request_refresh()
        _LOGGER.debug(f"data {self._coordinator.api.data[self._key]}")
