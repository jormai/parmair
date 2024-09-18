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
"""
"""
#not used
DEVICE_GLOBAL_STATUS = {
    0: "Sending Parameters",
    6: "Run",
    7: "Recovery",
    999: "Unknown"
}
"""


SENSOR_DEFS = {
    "ACK_ALARMS": [3, "Hälytysten kuittaus (0=ODOTETAAN KUITTAUSTA, 1=OK/KUITTAA)", "1", "1", "0", "1", "", "ReadWrite"],
    "ALARM_COUNT": [4, "Aktiivisten hälytysten määrä", "1", "1", "0", "100", "", "ReadOnly"],
    "TIME_YEAR": [9, "Vuosi", "1", "2023", "2000", "3000", "", "ReadWrite"],
    "TIME_MONTH": [10, "Kuukausi", "1", "8", "1", "12", "", "ReadWrite"],
    "TIME_DAY": [11, "Päivä", "1", "1", "1", "31", "", "ReadWrite"],
    "TIME_HOUR": [12, "Tunnit", "1", "1", "0", "23", "", "ReadWrite"],
    "TIME_MIN": [13, "Minuutit", "1", "1", "0", "59", "", "ReadWrite"],
    "MULTI_FW_VER": [14, "Multi24 firmware versio", "1", "2.00", "0.00", "100.00", "", "ReadOnly"],
    "MULTI_SW_VER": [15, "Multi24 sovelluksen ohjelmaversio", "1", "2.00", "0.00", "100.00", "", "ReadOnly"],
    "MULTI_BL_VER": [16, "Multi24 bootloaderin ohjelmaversio", "1", "2.00", "0.00", "100.00", "", "ReadOnly"],
    "TE01_M": [20, "Lämpötilamittaus, raitisilma", "2", "0.0", "-50.0", "120.0", "°C", "ReadWrite"],
    "TE05_M": [21, "Lämpötilamittaus, LTO kylmäpiste", "2", "0.0", "-50.0", "120.0", "°C", "ReadOnly"],
    "TE10_M": [22, "Lämpötilamittaus, tuloilma", "2", "0.0", "-50.0", "120.0", "°C", "ReadOnly"],
    "TE31_M": [23, "Lämpötilamittaus, jäteilma", "2", "0.0", "-50.0", "120.0", "°C", "ReadOnly"],
    "TE30_M": [24, "Lämpötilamittaus, poistoilma", "2", "0.0", "-50.0", "120.0", "°C", "ReadOnly"],
    "ME05_M": [25, "Kosteusmittaus, LTO-laite", "2", "0", "0", "100", "%", "ReadOnly"],
    "QE05_M": [26, "Hiilidioksidimittaus, poistoilma", "2", "0", "-1", "2000", "ppm", "ReadOnly"],
    "TF10_I": [27, "Indikointi, tulopuhallin", "2", "0", "0", "1", "", "ReadOnly"],
    "PF30_I": [28, "Indikointi, poistopuhallin", "2", "0", "0", "1", "", "ReadOnly"],
    "ME20_M": [29, "Kosteusmittaus, kostea tila", "2", "0", "-1", "100", "%", "ReadOnly"],
    "QE20_M": [30, "Hiilidioksidimittaus, sisäilma", "2", "0", "-1", "2000", "ppm", "ReadOnly"],
    "EXTERNAL_M": [31, "Ulkoinen ohjaussignaali (0-10V)", "2", "0.0", "-1.0", "100.0", "%", "ReadOnly"],
    "EXTERNAL_BOOST_M": [35, "Ulkoinen tehostussignaali (1-10V)", "2", "0.0", "-1.0", "100.0", "%", "ReadOnly"],
    "TE10_DEFLECTION_M": [36, "Tulolämpötilan poikkeutus (+/- 3 astetta), (-9.9=EI käytössä)", "2", "0.0", "-9.9", "3.0", "°C", "ReadOnly"],
    "TF10_Y": [40, "Säätö, tulopuhallin", "3", "0.0", "0.0", "100.0", "%", "ReadOnly"],
    "PF30_Y": [42, "Säätö, poistopuhallin", "3", "0.0", "0.0", "100.0", "%", "ReadOnly"],
    "TV45_Y": [44, "Säätö, jälkilämmityspatteri", "3", "0.0", "0.0", "100.0", "%", "ReadOnly"],
    "FG50_Y": [46, "Säätö, LTO", "3", "0.0", "0.0", "100.0", "%", "ReadOnly"],
    "EC05_Y": [48, "Säätö, esilämmityspatteri", "3", "0.0", "0.0", "100.0", "%", "ReadOnly"],
    "HP_RAD_O": [50, "Ohjaus, maalämpömoduli", "3", "0", "0", "1", "", "ReadOnly"],
    "HOME_SPEED_S": [60, "Asetusarvo, Ilmanvaihtoasetus kotona-tilassa", "4", "3", "1", "5", "", "ReadWrite"],
    "TE10_MIN_HOME_S": [61, "Asetusarvo, Tulolämpötilan minimiarvo kotona-tilassa", "4", "17.0", "10.0", "28.0", "°C", "ReadWrite"],
    "TE10_CONTROL_MODE_S": [62, "Asetusarvo, lämpötilan säätö (ECO, Vakio)", "4", "0", "0", "1", "", "ReadWrite"],
    "AWAY_SPEED_S": [63, "Asetusarvo, Ilmanvaihtoasetus poissa-tilassa", "4", "1", "1", "5", "", "ReadWrite"],
    "TE10_MIN_AWAY_S": [64, "Asetusarvo, Tulolämpötilan minimiarvo poissa-tilassa", "4", "15.0", "10.0", "28.0", "°C", "ReadWrite"],
    "BOOST_SETTING_S": [65, "Asetusarvo, Tehostuksen nopeusasetus (nopeus 3-5)", "4", "4", "3", "5", "", "ReadWrite"],
    "OVERP_AMOUNT_S": [68, "Asetusarvo, Puhaltimien ylipainetilanteen ylipaineen määrä", "4", "20", "0", "100", "%", "ReadWrite"],
    "TP_ENABLE_S": [70, "Asetusarvo, Aikaohjelmakäyttö (0=ei käytössä, 1=käytössä)", "4", "1", "0", "1", "", "ReadWrite"],
    "AUTO_SUMMER_COOL_S": [71, "Asetus, Kesäviilennystoiminto (0=ei käytössä, 1=on, 2=automaatti)", "4", "2", "0", "2", "", "ReadWrite"],
    "AUTO_SUMMER_POWER_S": [72, "Asetus, Kesäkäytön tehomuutokset (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", "ReadWrite"],
    "TE30_S": [73, "Asetusarvo, Poistolämpötila (Tavoiteltava huonelämpötila kesäkaudella)", "4", "18.0", "15.0", "25.0", "°C", "ReadWrite"],
    "AUTO_HEATER_ENABLE_S": [74, "Asetus, Jälkilämmitysvastus (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", "ReadWrite"],
    "AUTO_COLD_LOWSPEED_S": [75, "Asetus, Automaattinen tehonpudotus kylmissä olosuhteissa (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "","ReadWrite"]
}
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
    # Address: 1014 
    "MULTI_FW_VER": ["Multi24 firmware versio", "parmair_MULTI_FW_VER","", "mdi:information-outline", None],
    # Address: 1015
    "MULTI_SW_VER": ["Multi24 sovelluksen ohjelmaversio", "parmair_MULTI_SW_VER","", "mdi:information-outline", None],
    # Address: 1016
     "MULTI_BL_VER": ["Multi24 bootloader ohjelmaversio", "parmair_MULTI_BL_VER","", "mdi:information-outline", None],
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
