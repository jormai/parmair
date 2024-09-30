"""Support for Parmair number."""

from __future__ import annotations

from dataclasses import dataclass
import logging


from config.custom_components.parmair.coordinator import ParmairCoordinator
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
from .const import CONF_CURRENT_AIRFLOW_INPUT, CONF_CURRENT_FAN_SPEED, CONF_CURRENT_HUMIDITY, CONF_POWER_SWITCH, CONF_PRESET_MODE, DOMAIN, PRESET_MODES, SENSOR_DICT, SensorSpec

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
        self._attr_name = "Parmair Climate"
        self._key = "Parmair_climate"
        self._attr_unique_id = f"{config_entry.unique_id}-{self._key}"
        self._attr_translation_key = self._key
        #self._attr_device_class = self._spec.sensor_device_class
        self._attr_should_poll = False
        # To link this entity the Parmair device
        self._attr_device_info = {"identifiers": {(DOMAIN,  config_entry.unique_id)}}
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


    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""
        _LOGGER.debug(f"Set HVACMode {HVACMode}")


    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        _LOGGER.debug(f"Set async_set_temperature")

