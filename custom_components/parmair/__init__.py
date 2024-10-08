"""parmair: Parmair MAC v2 integration for home assistant.

This package provides Home Assistant Custom component for integrating Parmair energy recovery ventilator units using Parmair MAC v2 control.
https://github.com/jormai/parmair
"""
import logging
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.parmair.coordinator import ParmairCoordinator

from .const import (
    CONF_HOST,
    CONF_NAME,
    DOMAIN,
    GROUPS,
    STARTUP_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SELECT,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.CLIMATE
    ]

# The type alias needs to be suffixed with 'ConfigEntry'.
type ParmairConfigEntry = ConfigEntry[RuntimeData]

@dataclass
class RuntimeData:
    """Class to hold your data."""

    coordinator: DataUpdateCoordinator
    update_listener: Callable


def get_instance_count(hass: HomeAssistant) -> int:
    """Return number of instances."""
    entries = [
        entry
        for entry in hass.config_entries.async_entries(DOMAIN)
        if not entry.disabled_by
    ]
    return len(entries)

async def _async_update_listener(hass: HomeAssistant, config_entry):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)

async def async_update_device_registry(
    hass: HomeAssistant, config_entry: ParmairConfigEntry
):
    """Manual device registration."""
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator
    device_registry = dr.async_get(hass)

    for _, value in GROUPS.items():
        device_registry.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            hw_version=None,
            configuration_url=f"http://{config_entry.data.get(CONF_HOST)}",
            identifiers={(DOMAIN, f"{config_entry.unique_id}-{value}")},
            manufacturer=coordinator.api.data["comm_manufact"],
            model=coordinator.api.data["VENT_MACHINE"],
            name=f"{config_entry.data.get(CONF_NAME)}.{value}",
            #serial_number="1", #coordinator.api.data["comm_sernum"],
            sw_version=coordinator.api.data["MULTI_SW_VER"],
            translation_key=value,
            via_device=None,
        )



async def async_setup_entry(
    hass: HomeAssistant, config_entry: ParmairConfigEntry
):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)
    _LOGGER.debug(f"Setup config_entry for {DOMAIN} uid {config_entry.unique_id}")

    # Initialise the coordinator that manages data updates from your api.
    # This is defined in coordinator.py
    coordinator = ParmairCoordinator(hass, config_entry)


    # If the refresh fails, async_config_entry_first_refresh() will
    # raise ConfigEntryNotReady and setup will try again later
    # ref.: https://developers.home-assistant.io/docs/integration_setup_failures
    await coordinator.async_config_entry_first_refresh()

    # Test to see if api initialised correctly, else raise ConfigNotReady to make HA retry setup
    # Change this to match how your api will know if connected or successful update
    if not coordinator.api.data["comm_sernum"]:
        raise ConfigEntryNotReady(
            f"Timeout connecting to {config_entry.data.get(CONF_NAME)}"
        )

    # Initialise a listener for config flow options changes.
    # See config_flow for defining an options setting that shows up as configure on the integration.
    update_listener = config_entry.add_update_listener(_async_update_listener)

    # Add the coordinator and update listener to hass data to make
    # accessible throughout your integration
    # Note: this will change on HA2024.6 to save on the config entry.
    config_entry.runtime_data = RuntimeData(coordinator, update_listener)

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    # Regiser device
    await async_update_device_registry(hass, config_entry)

    # Return true to denote a successful setup.
    _LOGGER.debug("Parmair async setup complete!")
    return True
