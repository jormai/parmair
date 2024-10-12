"""Parmair sensor."""
from datetime import datetime
from datetime import date
import logging
from . import ParmairConfigEntry
from .const import CONF_NAME, CONF_FC_DATE_YEAR, CONF_FC_DATE_MONTH, CONF_FC_DATE_DAY, DOMAIN, GROUPS, SensorSpec
from .const import SENSOR_DICT
from .coordinator import ParmairCoordinator
from homeassistant.components.date import DateEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory, generate_entity_id
from homeassistant.helpers.update_coordinator import CoordinatorEntity
_LOGGER = logging.getLogger(__name__)

def add_sensor_defs(
    coordinator: ParmairCoordinator,
    config_entry: ParmairConfigEntry,
    sensor_list
):
    """Class Initializitation."""
    sensor_list.append(
                ParmairDateEntity(coordinator, config_entry, (CONF_FC_DATE_DAY, SENSOR_DICT[CONF_FC_DATE_DAY]),
                                  (CONF_FC_DATE_MONTH,SENSOR_DICT[CONF_FC_DATE_MONTH]), (CONF_FC_DATE_YEAR,SENSOR_DICT[CONF_FC_DATE_YEAR]))
            )

async def async_setup_entry(
    hass: HomeAssistant, config_entry: ParmairConfigEntry, async_add_entities
):
    """Sensor Platform setup."""

    # Get handler to coordinator from config
    coordinator: ParmairCoordinator = config_entry.runtime_data.coordinator

    _LOGGER.debug("(sensor) Name: %s", config_entry.data.get(CONF_NAME))

    sensor_list = []
    add_sensor_defs(coordinator, config_entry, sensor_list)

    async_add_entities(sensor_list)

    return True


class ParmairDateEntity(CoordinatorEntity, DateEntity):
    """Representation of an Date sensor."""

    def __init__(self, coordinator: ParmairCoordinator, config_entry: ParmairConfigEntry, sensor_data_day:tuple[str,SensorSpec],
                 sensor_data_month:tuple[str,SensorSpec],sensor_data_year:tuple[str,SensorSpec]):
        """Class Initializitation."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._key_day = sensor_data_day[0]
        self._key_month = sensor_data_month[0]
        self._key_year = sensor_data_year[0]

        # no name defined for the sensor since uses translated name
        # set to use translated name
        self._attr_has_entity_name = True
        self.entity_id = generate_entity_id("date.{}", sensor_data_day[1].name, hass=coordinator.hass)
        self._attr_translation_key = sensor_data_day[1].name

        self._attr_unique_id = f"{config_entry.unique_id}-{self._key_day}"

        #self._attr_native_unit_of_measurement = spec.unit
        self._attr_icon = sensor_data_day[1].icon
        #self._attr_device_class = spec.sensor_device_class
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_should_poll = False


        # To link this entity the Parmair device
        self._attr_device_info = {"identifiers": {(DOMAIN,  f"{config_entry.unique_id}-{GROUPS[sensor_data_day[1].group]}")}}


    @property
    def native_value(self):
        """Return the state of the sensor."""
        keys_to_check = [self._key_day,self._key_month, self._key_year]
        # Check if all keys exist in the dictionary
        if not all(key in self._coordinator.api.data  for key in keys_to_check):
            return None
        day = self._coordinator.api.data[self._key_day]
        month = self._coordinator.api.data[self._key_month]
        year = self._coordinator.api.data[self._key_year]
        date_format = "%m.%d.%Y"
        return datetime.strptime(f"{day}.{month}.{year}", date_format)

    async def async_set_value(self, value: date) -> None:
        """Change the date."""
        _LOGGER.debug(f"Setting data not implemented {value}")
