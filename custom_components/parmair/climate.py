"""Support for Parmair number."""

from __future__ import annotations

from dataclasses import dataclass
import logging


from config.custom_components.parmair.coordinator import ParmairCoordinator
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVAC_MODES, PRESET_ECO, PRESET_NONE, ClimateEntityFeature, HVACAction, HVACMode
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
from .const import CONF_UNIT_CONTROL_FO, DOMAIN, PRESET_MODES, SENSOR_DICT, SensorSpec

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
        self._attr_preset_modes = PRESET_MODES
        self._attr_hvac_modes = HVAC_MODES   
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.TURN_ON
        )
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        #_enable_turn_on_off_backwards_compatibility = False

    @property
    def hvac_mode(self) -> HVACMode | None:
        """Return hvac operation ie. heat, cool mode."""
        power_on = int(self._coordinator.api.data[CONF_UNIT_CONTROL_FO])
        return HVACMode.HEAT_COOL if power_on else HVACMode.OFF


    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        if (
            self.hvac_mode == HVACMode.AUTO
            and self.coordinator.data.state.hvac_mode.value == PRESET_ECO
        ):
            return PRESET_ECO
        return PRESET_NONE

    @callback
    def _async_update_attrs(self) -> None:
        """Update attrs from device."""
        power_on = int(self._coordinator.api.data[CONF_UNIT_CONTROL_FO])
        self._attr_hvac_mode = HVACMode.HEAT_COOL if power_on else HVACMode.OFF
        self._attr_hvac_action = HVACAction.FAN if power_on.speed else HVACAction.OFF


    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set the HVAC mode."""
        _LOGGER.debug(f"Set HVACMode {HVACMode}")


    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        _LOGGER.debug(f"Set async_set_temperature")

