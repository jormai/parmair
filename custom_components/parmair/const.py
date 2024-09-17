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
# Base component constants
NAME = "Parmair MAC v2 ModBus TCP"
DOMAIN = "parmair"
VERSION = "1.0.0"
ATTRIBUTION = "by @jormai"
ISSUE_URL = "https://github.com/alexdejormai/parmair/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Configuration and options
CONF_NAME = "name"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_SLAVE_ID = "slave_id"
CONF_BASE_ADDR = "base_addr"
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_NAME = "Parmair MAC v2"
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 0
DEFAULT_BASE_ADDR = 0
DEFAULT_SCAN_INTERVAL = 60
MIN_SCAN_INTERVAL = 30
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
{ATTRIBUTION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
DEVICE_GLOBAL_STATUS = {
    0: "Sending Parameters",
    6: "Run",
    7: "Recovery",
    999: "Unknown",
}
"""

# Sensors for all 
"""
         sensor_data = {
            "name": sensor_info[0],
            "key": sensor_info[1],
            "unit": sensor_info[2],
            "icon": sensor_info[3],
            "device_class": sensor_info[4],
            "state_class": sensor_info[5],
        }
"""

SENSOR_TYPES_COMMON = {
    # Address: 1020
    "parmair_raitisilma": ["parmair.raitisilma", "parmair_raitisilma", "°C", "mdi:temperature-celsius", "SensorStateClass.TEMPERATURE"],
    
    # Address: 1021
    "parmair_LTO_kylmapiste": ["parmair.LTO_kylmapiste", "parmair_LTO_kylmapiste", "°C", "mdi:temperature-celsius", "SensorStateClass.TEMPERATURE"],
    
    # Address: 1022
    "parmair_tuloilma": ["parmair.tuloilma", "parmair_tuloilma", "°C", "mdi:temperature-celsius", "SensorStateClass.TEMPERATURE"],
    
    # Address: 1023
    "parmair_jateilma": ["parmair.jateilma", "parmair_jateilma", "°C", "mdi:temperature-celsius", "SensorStateClass.TEMPERATURE"],
    
    # Address: 1024
    "parmair_poistoilma": ["parmair.poistoilma", "parmair_poistoilma", "°C", "mdi:temperature-celsius", "SensorStateClass.TEMPERATURE"],
    
    # Address: 1025
    "parmair_kosteusmittaus": ["parmair.kosteusmittaus", "parmair_kosteusmittaus", "%", "mdi:water-percent", "SensorStateClass.MOISTURE"],
    
    # Address: 1026
    "parmair_CO2": ["parmair.CO2", "parmair_CO2", "ppm", "mdi:molecule-co2", "SensorStateClass.CARBON_DIOXIDE"],
    
    # Address: 1040
    "parmair_tulopuhallin_saato": ["parmair.tulopuhallin_saato", "parmair_tulopuhallin_saato", "%", "mdi:fan", "SensorStateClass.SPEED"],
    
    # Address: 1042
    "pa_poistopuhallin_saato": ["pa.poistopuhallin_saato", "pa_poistopuhallin_saato", "%", "mdi:fan", "SensorStateClass.SPEED"],
    
    # Address: 1044
    "parmair_jalkilammitys": ["parmair.jalkilammitys", "parmair_jalkilammitys", "%", "mdi:water-percent", "SensorStateClass.MOISTURE"],
    
    # Address: 1046
    "parmair_saatoasento_LTO": ["parmair.saatoasento_LTO", "parmair_saatoasento_LTO", "%", "mdi:percent-circle", "SensorStateClass.POWER_FACTOR"],
    
    # Address: 1048
    "parmair_ohituslammitys": ["parmair.ohituslammitys", "parmair_ohituslammitys", "%", "mdi:water-percent", "SensorStateClass.MOISTURE"],
    
    # Address: 1060
    "parmair_home_speed_s": ["parmair.home_speed_s", "parmair_home_speed_s", "", "mdi:fan", "SensorStateClass.SPEED"],
    
    # Address: 1061
    "parmair_TE10_MIN_HOME_S": ["parmair.TE10_MIN_HOME_S", "parmair_TE10_MIN_HOME_S", "°C", "mdi:temperature-celsius", "SensorStateClass.TEMPERATURE"],
    
    # Address: 1062
    "parmair_TE10_CONTROL_MODE_S": ["parmair.TE10_CONTROL_MODE_S", "parmair_TE10_CONTROL_MODE_S", "", "mdi:temperature-celsius", "SensorStateClass.TEMPERATURE"],

    # Address: 1125
    "parmair_VENT_MACHINE": ["parmair IV-koneen tyyppikoodi", "parmair_VENT_MACHINE","", "mdi:information-outline", None],
    
    # Address: 1180
    "parmair_UNIT_CONTROL_FO": ["parmair.UNIT_CONTROL_FO", "parmair_UNIT_CONTROL_FO", "", "mdi:percent-circle", "SensorStateClass.POWER"],
    
    # Address: 1181
    "parmair_mac_state": ["parmair.mac_state", "parmair_mac_state", "", "mdi:fan", "SensorStateClass.SPEED"],
    
    # Address: 1187
    "parmair_iv_nopeusasetus": ["parmair.iv-nopeusasetus", "parmair_iv_nopeusasetus", "", "mdi:fan", "SensorStateClass.SPEED"],
    
    # Address: 1192
    "parmair_kosteusmittauksen_24h_ka": ["parmair.kosteusmittauksen_24h_ka", "parmair_kosteusmittauksen_24h_ka", "%", "mdi:water-percent", "SensorStateClass.MOISTURE"]

}
