"""Support for Parmair number."""

from __future__ import annotations

from dataclasses import dataclass
import logging


from .coordinator import ParmairCoordinator
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVAC_MODES, PRESET_AWAY, PRESET_BOOST, PRESET_ECO, PRESET_HOME, PRESET_NONE, ClimateEntityFeature, HVACAction, HVACMode
from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.components.number.const import NumberDeviceClass
from homeassistant.const import CONF_NAME, EntityCategory, Platform, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.enum import try_parse_enum
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ParmairConfigEntry
from .const import CONF_CURRENT_AIRFLOW_INPUT, CONF_CURRENT_FAN_SPEED, CONF_CURRENT_HUMIDITY, CONF_POWER_SWITCH, CONF_PRESET_MODE, DOMAIN, SENSOR_DICT

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ParmairConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Parmair MAC v2."""
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator
    async_add_entities([ParmairClimate(coordinator, config_entry)])


class ParmairClimate(CoordinatorEntity, ClimateEntity):
    """Parmair climate entity."""
    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry) -> None:
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._key = "parmair_climate"
        
        # no name defined for the sensor since uses translated name
        # set to use translated name
        self._attr_has_entity_name = True
        self.entity_id = "climate.parmair"
        self._attr_translation_key = "parmair_climate"
        
        self._attr_unique_id = f"{config_entry.unique_id}-{self._key}"
        self._attr_translation_key = self._key

        self._attr_should_poll = False
        # To link this entity the Parmair device
        self._attr_device_info = {"identifiers": {(DOMAIN,  f"{config_entry.unique_id}-ESSENTIALS")}}
        self._attr_fan_modes = [
            "0",
            "1",
            "2",
            "3",
            "4"
        ]
        self._attr_preset_modes = [
            "Off", 
            PRESET_AWAY, 
            PRESET_HOME, 
            PRESET_BOOST,
            "Sauna", 
            "Fireplace"
        ]
        self._attr_hvac_modes = [
            HVACMode.HEAT_COOL,
            HVACMode.OFF
        ]   
        self._attr_supported_features = (
            ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.PRESET_MODE
        )
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        
        #_enable_turn_on_off_backwards_compatibility = False
        self._async_update_attrs()

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return hvac operation ie. heat, cool mode."""
        power_on = int(self._coordinator.api.data[CONF_POWER_SWITCH])
        return HVACMode.HEAT_COOL if power_on else HVACMode.OFF


    @callback
    def _async_update_attrs(self) -> None:
        """Update attrs from device."""
        power_on = int(self._coordinator.api.data[CONF_POWER_SWITCH])
        self._attr_hvac_mode = HVACMode.HEAT_COOL if power_on else HVACMode.OFF
        self._attr_hvac_action = HVACAction.FAN if power_on else HVACAction.OFF
        self._attr_current_humidity = int(self._coordinator.api.data[CONF_CURRENT_HUMIDITY])
        self._attr_current_temperature = float(self._coordinator.api.data[CONF_CURRENT_AIRFLOW_INPUT])
        self._attr_fan_mode = self._coordinator.api.data[CONF_CURRENT_FAN_SPEED]
        self._attr_preset_mode = self._attr_preset_modes[int(self._coordinator.api.data[CONF_PRESET_MODE])]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Fetch new state data for the sensor."""
        self._async_update_attrs()
        self.async_write_ha_state()
        _LOGGER.debug("_handle_coordinator_update: sensors state written to state machine")

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""
        _LOGGER.debug(f"Set HVACMode {HVACMode}")

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        value = self._attr_preset_modes.index(preset_mode)
        
        result = await self._coordinator.async_write_data(CONF_PRESET_MODE , value)
        _LOGGER.debug(f"Setting value for {CONF_PRESET_MODE}, result {result}")
        self._async_update_attrs()
        #if result == True:
        #    await self.coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        _LOGGER.debug(f"Set async_set_temperature")

