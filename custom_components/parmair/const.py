DOMAIN = "parmair"
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
# Sensors for all 
SENSOR_TYPES_COMMON = {
    "Manufacturer": [
        "Manufacturer",
        "comm_manufact",
        None,
        "mdi:information-outline",
        None,
        None,
    ]}