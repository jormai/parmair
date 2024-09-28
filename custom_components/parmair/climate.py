"""Support for Parmair number."""

from __future__ import annotations

from dataclasses import dataclass
import logging


from config.custom_components.parmair.coordinator import ParmairCoordinator
from config.custom_components.parmair.entity import ParmairEntity
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature, HVACAction, HVACMode
from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.components.number.const import NumberDeviceClass
from homeassistant.const import CONF_NAME, EntityCategory, Platform, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ParmairConfigEntry
from .const import SENSOR_DICT, SensorSpec

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ParmairConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BAF fan auto comfort."""
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator
    async_add_entities([ParmairClimate("Parmair MAC", coordinator)])


class ParmairClimate(ParmairEntity, ClimateEntity):
    """Parmair climate entity."""

    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_OFF
        | ClimateEntityFeature.TURN_ON
    )
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.FAN_ONLY]
    _attr_translation_key = "auto_comfort"
    _enable_turn_on_off_backwards_compatibility = False

    @callback
    def _async_update_attrs(self) -> None:
        """Update attrs from device."""
        device = self._device
        auto_on = device.auto_comfort_enable
        self._attr_hvac_mode = HVACMode.FAN_ONLY if auto_on else HVACMode.OFF
        self._attr_hvac_action = HVACAction.FAN if device.speed else HVACAction.OFF
        self._attr_target_temperature = device.comfort_ideal_temperature
        self._attr_current_temperature = device.temperature

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""
        self._device.auto_comfort_enable = hvac_mode == HVACMode.FAN_ONLY

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        if not self._device.auto_comfort_enable:
            self._device.auto_comfort_enable = True
        self._device.comfort_ideal_temperature = kwargs[ATTR_TEMPERATURE]
