DOMAIN = "parmair"
from enum import Enum
from homeassistant.components.climate.const import PRESET_ECO, PRESET_NONE, HVACMode
from homeassistant.components.number.const import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    Platform,
)
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
# Base component constants
NAME = "Parmair MAC v2 ModBus TCP"
DOMAIN = "parmair"
DEFAULT_NAME = "parmair"
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
HVAC_MODES = [
    HVACMode.AUTO,
    HVACMode.HEAT,
    HVACMode.OFF,
]

PRESET_MODES = [
    PRESET_ECO,
    PRESET_NONE,
]
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

READ_ONLY = False
READ_WRITE = True

    
class SensorSpec:
    def __init__(self, id: int, multiplier: int, comment: str, group: str, factory_setting: str,  min_limit: str, max_limit: str, unit: str, sensor_device_class: SensorDeviceClass|BinarySensorDeviceClass|None, icon: str, writeable: bool, platform:Platform=Platform.SENSOR,options:list[str]=None):
        self.id = id
        self.comment = comment
        self.group = group
        self.factory_setting = factory_setting
        self.multiplier = multiplier
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.unit = unit
        self.sensor_device_class = sensor_device_class
        self.icon = icon
        self.writeable = writeable
        self.platform = platform
        self.options = options

    def __repr__(self):
        return f"DataRow({self.id}, {self.comment}, {self.group}, {self.multiplier}, {self.min_limit}, {self.max_limit}, {self.unit}, {self.sensor_device_class}, {self.icon}, {self.writeable})"
CONF_TE10_MIN_AWAY_S="TE10_MIN_AWAY_S"
CONF_UNIT_CONTROL_FO="UNIT_CONTROL_FO"
# note, id must be ascending    
SENSOR_DEFS = {
    "ACK_ALARMS": [3,1, "Hälytysten kuittaus (0=ODOTETAAN KUITTAUSTA, 1=OK/KUITTAA)", "1", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Odotetaan kuittausta","OK/Kuittaa"]],
    "ALARM_COUNT": [4,1, "Aktiivisten hälytysten määrä", "1", "0", "0", "100", None, None, "mdi:information-outline", READ_ONLY,Platform.NUMBER],
    "TIME_YEAR": [9,1, "Vuosi", "1", "2023", "2000", "3000", None, None, "mdi:information-outline", READ_WRITE],
    "TIME_MONTH": [10,1, "Kuukausi", "1", "8", "1", "12", None, None, "mdi:information-outline", READ_WRITE],
    "TIME_DAY": [11,1, "Päivä", "1", "1", "1", "31", None, None, "mdi:information-outline", READ_WRITE],
    "TIME_HOUR": [12,1, "Tunnit", "1", "1", "0", "23", None, None, "mdi:information-outline", READ_WRITE],
    "TIME_MIN": [13,1, "Minuutit", "1", "1", "0", "59", None, None, "mdi:information-outline", READ_WRITE],
    "MULTI_FW_VER": [14,100, "Multi24 firmware versio", "1", "2.00", "0.00", "100.00", None, None, "mdi:information-outline", READ_ONLY],
    "MULTI_SW_VER": [15,100, "Multi24 sovelluksen ohjelmaversio", "1", "2.00", "0.00", "100.00", None, None, "mdi:information-outline", READ_ONLY],
    "MULTI_BL_VER": [16,100, "Multi24 bootloaderin ohjelmaversio", "1", "2.00", "0.00", "100.00", None, None, "mdi:information-outline", READ_ONLY],
    "TE01_M": [20,10, "Lämpötilamittaus, raitisilma", "2", "0.0", "-50.0", "120.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_ONLY],
    "TE05_M": [21,10, "Lämpötilamittaus, LTO kylmäpiste", "2", "0.0", "-50.0", "120.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_ONLY],
    "TE10_M": [22,10, "Lämpötilamittaus, tuloilma", "2", "0.0", "-50.0", "120.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_ONLY],
    "TE31_M": [23,10, "Lämpötilamittaus, jäteilma", "2", "0.0", "-50.0", "120.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_ONLY],
    "TE30_M": [24,10, "Lämpötilamittaus, poistoilma", "2", "0.0", "-50.0", "120.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_ONLY],
    "ME05_M": [25,1, "Kosteusmittaus, LTO-laite", "2", "0", "0", "100", "%", SensorDeviceClass.MOISTURE, "mdi:water-percent", READ_ONLY],
    "QE05_M": [26,1, "Hiilidioksidimittaus, poistoilma", "2", "0", "-1", "2000", "ppm", SensorDeviceClass.CO2, "mdi:molecule-co2", READ_ONLY],
    "TF10_I": [27,1, "Indikointi, tulopuhallin", "2", "0", "0", "1", None, BinarySensorDeviceClass.RUNNING, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "PF30_I": [28,1, "Indikointi, poistopuhallin", "2", "0", "0", "1", None, BinarySensorDeviceClass.RUNNING, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "ME20_M": [29,1, "Kosteusmittaus, kostea tila", "2", "0", "-1", "100", "%", SensorDeviceClass.MOISTURE, "mdi:water-percent", READ_ONLY],
    "QE20_M": [30,1, "Hiilidioksidimittaus, sisäilma", "2", "0", "-1", "2000", "ppm", SensorDeviceClass.CO2, "mdi:molecule-co2", READ_ONLY],
    "EXTERNAL_M": [31,10, "Ulkoinen ohjaussignaali (0-10V)", "2", "0.0", "-1.0", "100.0", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_ONLY],
    "EXTERNAL_BOOST_M": [35,10, "Ulkoinen tehostussignaali (1-10V)", "2", "0.0", "-1.0", "100.0", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_ONLY],
    "TE10_DEFLECTION_M": [36,10, "Tulolämpötilan poikkeutus (+/- 3 astetta), (-9.9=EI käytössä)", "2", "0.0", "-9.9", "3.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_ONLY],
    "TF10_Y": [40,10, "Säätö, tulopuhallin", "3", "0.0", "0.0", "100.0", "%", SensorDeviceClass.SPEED, "mdi:fan", READ_ONLY],
    "PF30_Y": [42,10, "Säätö, poistopuhallin", "3", "0.0", "0.0", "100.0", "%", SensorDeviceClass.SPEED, "mdi:fan", READ_ONLY],
    "TV45_Y": [44,10, "Säätö, jälkilämmityspatteri", "3", "0.0", "0.0", "100.0", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_ONLY],
    "FG50_Y": [46,10, "Säätö, LTO", "3", "0.0", "0.0", "100.0", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_ONLY],
    "EC05_Y": [48,10, "Säätö, esilämmityspatteri", "3", "0.0", "0.0", "100.0", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_ONLY],
    "HP_RAD_O": [50,1, "Ohjaus, maalämpömoduli", "3", "0", "0", "1", None, None, "mdi:information-outline", READ_ONLY],
    "HOME_SPEED_S": [60,1, "Asetusarvo, Ilmanvaihtoasetus kotona-tilassa", "4", "3", "1", "5", None, None, "mdi:information-outline", READ_WRITE, Platform.NUMBER],
    "TE10_MIN_HOME_S": [61,10, "Asetusarvo, Tulolämpötilan minimiarvo kotona-tilassa", "4", "17.0", "10.0", "28.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "TE10_CONTROL_MODE_S": [62,1, "Asetusarvo, lämpötilan säätö (ECO, Vakio)", "4", "0", "0", "1", None, None, "mdi:information-outline", READ_WRITE, Platform.SELECT,["ECO","Vakio"]],
    "AWAY_SPEED_S": [63,1, "Asetusarvo, Ilmanvaihtoasetus poissa-tilassa", "4", "1", "1", "5", None, None, "mdi:information-outline", READ_WRITE, Platform.NUMBER],
    "TE10_MIN_AWAY_S": [64,10, "Asetusarvo, Tulolämpötilan minimiarvo poissa-tilassa", "4", "15.0", "10.0", "28.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "BOOST_SETTING_S": [65,1, "Asetusarvo, Tehostuksen nopeusasetus (nopeus 3-5)", "4", "4", "3", "5", None, NumberDeviceClass.SPEED, "mdi:information-outline", READ_WRITE, Platform.NUMBER],
    "OVERP_AMOUNT_S": [68,1, "Asetusarvo, Puhaltimien ylipainetilanteen ylipaineen määrä", "4", "20", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "TP_ENABLE_S": [70,1, "Asetusarvo, Aikaohjelmakäyttö (0=ei käytössä, 1=käytössä)", "4", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Käytössä"]],
    "AUTO_SUMMER_COOL_S": [71,1, "Asetus, Kesäviilennystoiminto (0=ei käytössä, 1=on, 2=automaatti)", "4", "2", "0", "2", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Käytössä","Automaatti"]],
    "AUTO_SUMMER_POWER_S": [72,1, "Asetus, Kesäkäytön tehomuutokset (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Automaatti"]],
    "TE30_S": [73,10, "Asetusarvo, Poistolämpötila (Tavoiteltava huonelämpötila kesäkaudella)", "4", "18.0", "15.0", "25.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "AUTO_HEATER_ENABLE_S": [74,1, "Asetus, Jälkilämmitysvastus (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Automaatti"]],
    "AUTO_COLD_LOWSPEED_S": [75,1, "Asetus, Automaattinen tehonpudotus kylmissä olosuhteissa (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Automaatti"]],
    "COLD_LOWSPEED_S": [76,10, "Asetus, Tehonpudostus pakkasella, pakkasraja", "4", "-15.0", "-25.0", "10.0", "°C", NumberDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "AUTO_HUMIDITY_BOOST_S": [77,1, "Asetus, Automaattinen kosteustehostus (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Automaatti"]],
    "ME05_BOOST_SENSITIVITY": [78,1, "Asetusarvo, kosteustehostuksen herkkyys", "4", "1", "0", "2", None, None, "mdi:information-outline", READ_WRITE, Platform.NUMBER],
    "ME_BST_TE01_LIMIT": [79,10, "Asetusarvo, Kosteustehostuksen ulkolämpötilaraja", "4", "-10.0", "-15.0", "15.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "AUTO_CO2_BOOST_S": [80,1, "Asetus, Automaattinen hiilidioksiditehostus (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Automaatti"]],
    "AUTO_HOMEAWAY_S": [81,1, "Asetus, Automaattinen kotona/poissa (CO2) (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei käytössä","Automaatti"]],
    "QE_HOME_S": [82,1, "Asetusarvo, CO2 kotona-raja", "4", "500", "100", "2000", "ppm", SensorDeviceClass.CO2, "mdi:molecule-co2", READ_WRITE, Platform.NUMBER],
    "QE_BOOST_S": [83,1, "Asetusarvo, CO2 tehostusraja (tehostuksen aloitus)", "4", "800", "100", "2000", "ppm", SensorDeviceClass.CO2, "mdi:molecule-co2", READ_WRITE, Platform.NUMBER],
    "FILTER_INTERVAL_S": [90,1, "Asetusarvo, Suodattimien vaihtoväli (0=3kk, 1=4kk, 2=6kk)", "4", "0", "0", "2", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["3kk","4kk","6kk"]],
    "HP_RAD_MODE": [91,1, "Asetusarvo, maalämpömoduulin toiminta (0=Off, 1=On, 2=Auto)", "4", "2", "0", "2", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Off","On","Auto"]],
    "HP_RAD_WINTER": [92,10, "Asetusarvo, maalämpömoduulin käyttöraja talvi", "4", "0.0", "-30.0", "15.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "HP_RAD_SUMMER": [93,10, "Asetusarvo, maalämpömoduulin käyttöraja kesä", "4", "15.0", "0.0", "40.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "HEATING_SEASON_AVERAGE": [94,10, "Asetusarvo, Lämmityskausi (24h raitis lämpötila)", "4", "14.0", "6.0", "50.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "HEATING_SEASON_MOMENT": [95,10, "Asetusarvo, Lämmityskausi (hetkellinen raitis lämpötila)", "4", "8.0", "-5.0", "50.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "TE10_MIN_SUMMER_S": [96,10, "Asetusarvo, Tulolämpötilan kesä-tilassa", "4", "12.0", "10.0", "25.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "TE10_MAX_S": [97,10, "Asetusarvo, Tulolämpötilan maksimiarvo", "4", "25.0", "10.0", "35.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "BST_TE01_LIMIT": [98,10, "Asetusarvo, Tehostuksen ulkolämpötilaraja / CO2, 0-10V", "4", "-10.0", "-15.0", "0.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "M10_TYPE": [105,1, "Mittauspaikan 10 tyyppi. 0=Ei käytössä.", "10", "0", "0", "27", None, None, "mdi:information-outline", READ_WRITE, Platform.NUMBER],
    "M11_TYPE": [106,1, "Mittauspaikan 11 tyyppi. 0=Ei käytössä.", "10", "0", "0", "27", None, None, "mdi:information-outline", READ_WRITE, Platform.NUMBER],
    "M12_TYPE": [107,1, "Mittauspaikan 12 tyyppi. 0=Ei käytössä.", "10", "0", "0", "27", None, None, "mdi:information-outline", READ_WRITE, Platform.NUMBER],
    "SF_SPEED1_S": [108,1, "Asetusarvo, Tulopuhaltimen nopeusasetus 1", "10", "20", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "SF_SPEED2_S": [109,1, "Asetusarvo, Tulopuhaltimen nopeusasetus 2", "10", "35", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "SF_SPEED3_S": [110,1, "Asetusarvo, Tulopuhaltimen nopeusasetus 3", "10", "60", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "SF_SPEED4_S": [111,1, "Asetusarvo, Tulopuhaltimen nopeusasetus 4", "10", "75", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "SF_SPEED5_S": [112,1, "Asetusarvo, Tulopuhaltimen nopeusasetus 5", "10", "90", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "EF_SPEED1_S": [113,1, "Asetusarvo, Poistopuhaltimen nopeusasetus 1", "10", "20", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "EF_SPEED2_S": [114,1, "Asetusarvo, Poistopuhaltimen nopeusasetus 2", "10", "35", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "EF_SPEED3_S": [115,1, "Asetusarvo, Poistopuhaltimen nopeusasetus 3", "10", "60", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "EF_SPEED4_S": [116,1, "Asetusarvo, Poistopuhaltimen nopeusasetus 4", "10", "75", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "EF_SPEED5_S": [117,1, "Asetusarvo, Poistopuhaltimen nopeusasetus 5", "10", "90", "0", "100", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_WRITE, Platform.NUMBER],
    "SENSOR_TE_COR": [120,10, "Lämpötilan korjaus", "10", "0.0", "-5.0", "5.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "SENSOR_ME_COR": [121,1, "Kosteuden korjaus", "10", "0", "-20", "20", "%", SensorDeviceClass.MOISTURE, "mdi:water-percent", READ_WRITE, Platform.NUMBER],
    "SENSOR_CO2_COR": [122,1, "Hiilidioksidin korjaus", "10", "0", "-500", "500", "ppm", SensorDeviceClass.CO2, "mdi:molecule-co2", READ_WRITE, Platform.NUMBER],
    "HEATPUMP_RADIATOR_ENABLE": [124,1, "Maalämpöpatteri (0=Ei asennettu, 1=Asennettu)", "10", "0", "0", "1", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Ei asennettu","Asennettu"]],
    "VENT_MACHINE": [125,1, "IV-koneen tyyppikoodi", "10", "1", "-1000", "1000", None, None, "mdi:information-outline", READ_ONLY, Platform.NUMBER],
    "TE10_MIN_S": [129,10, "Asetusarvo, Tulolämpötilan minimiarvo jonka käyttäjä voi asettaa", "10", "10.0", "10.0", "25.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "TE10_BASE_S": [137,10, "Asetusarvo, Tulolämpötilan perusasetusarvo, josta voidaan potikalla poikkeuttaa.", "10", "17.0", "15.0", "25.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_WRITE, Platform.NUMBER],
    "BST_MINTIME": [140,1, "Asetusarvo, Tehostuksen minimiaika (min) / LTO, CO2, 0-10V", "10", "5", "1", "60", "min", "SensorStateClass.DURATION", "mdi:clock-time-nine-outline", READ_WRITE, Platform.NUMBER],
    "CO2_MINTIME": [141,1, "Asetusarvo, Automaattinen kotona-poissa minimiaika", "10", "15", "1", "600", "min", "SensorStateClass.DURATION", "mdi:clock-time-nine-outline", READ_WRITE, Platform.NUMBER],
    "BST_TIME_LIMIT": [144,1, "Asetusarvo, Kosteus ja CO2-tehostusten maksimiaika", "10", "1440", "15", "1440", "min", "SensorStateClass.DURATION", "mdi:clock-time-nine-outline", READ_WRITE, Platform.NUMBER],
    CONF_UNIT_CONTROL_FO: [180,1, "IV-koneen ohjaus (0=Off, 1=On)", "10", "1", "0", "1", SwitchDeviceClass.SWITCH, None, "mdi:information-outline", READ_WRITE,Platform.SWITCH],
    "USERSTATECONTROL_FO": [181,1, "MAC 2 User state control from screen. 0=Off, 1=Away, 2=Home, 3=Boost, 4=Sauna, 5=Fireplace", "6", "1", "0", "5", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Off","Away","Home","Boost","Sauna","Fireplace"]],
    "DFRST_FI": [182,1, "Fiktiivinen indikointi, LTO:n sulatus päällä/pois", "6", "0", "0", "1", None, BinarySensorDeviceClass.RUNNING, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "FG50_EA_M": [183,10, "Fiktiivinen mittaus, LTO:n hyötysuhde", "6", "0.0", "0.0", "100.0", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_ONLY],
    "FILTER_STATE_FI": [184,1, "Fiktiivinen asetus, Suodattimen kunto (0=Idle, 1=Kuittaa vaihto, 2=Muistutushälytys)", "6", "0", "0", "2", None, None, "mdi:information-outline", READ_WRITE,Platform.SELECT,["Idle","Kuittaa vaihto","Muistutushälytys"]],
    "SENSOR_STATUS": [185,1, "Yhdistelmäanturin tila (1=Ok, 0=Initoimatta, -1=Modbuskommunikaatiovirhe, -2=Data puuttuu)", "6", "0", "-2", "1", None, None, "mdi:information-outline", READ_ONLY],
    "SUMMER_MODE_I": [189,1, "Tilatieto, Kausi. 0=Talvi, 1=Väli, 2=Kesä", "6", "0", "0", "2", None, None, "mdi:information-outline", READ_ONLY],
    "SUMMER_POWER_CHANGE_FM": [190,1, "Kesätilanteen tehonsäätö", "6", "0", "-1", "1", None, None, "mdi:information-outline", READ_ONLY],
    "HUMIDITY_FM": [191,100, "Laskettu kosteus", "6", "0.00", "0.00", "100.00", "g/kg", SensorDeviceClass.MOISTURE, "mdi:water-percent", READ_ONLY],
    "ME05_AVG_FM": [192,10, "Fiktiivinen mittaus, LTO:n kosteusmittauksen 24h keskiarvo", "6", "0.0", "0.0", "100.0", "%", SensorDeviceClass.MOISTURE, "mdi:water-percent", READ_ONLY],
    "PWR_LIMIT_FY": [199,10, "Fiktiivinen säätö, puhaltimien tehonrajoitus", "6", "0.0", "0.0", "100.0", "%", SensorDeviceClass.POWER_FACTOR, "mdi:percent-circle", READ_ONLY],
    "TE01_AVG_FM": [213,10, "Ulkolämpötilan vrk keskiarvo", "6", "0.0", "-50.0", "50.0", "°C", SensorDeviceClass.TEMPERATURE, "mdi:temperature-celsius", READ_ONLY],
    "TE01_FA": [220,1, "Vikahälytys, raitisilman lämpötila / anturivika", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TE10_FA": [221,1, "Vikahälytys, tulolämpötila / anturivika", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TE05_FA": [222,1, "Vikahälytys, tulolämpötila LTO:n jälkeen / anturivika", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TE30_FA": [223,1, "Vikahälytys, poistolämpötila / anturivika", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TE31_FA": [224,1, "Vikahälytys, jäteilman lämpötila / anturivika", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "ME05_FA": [225,1, "Vikahälytys, LTO:n kosteus / anturivika", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TF10_CA": [226,1, "Ristiriitahälytys, tulopuhallin", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "PF30_CA": [227,1, "Ristiriitahälytys, poistopuhallin", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TE10_HA": [228,1, "Ylärajahälytys, tulolämpötila", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TE30_HA": [229,1, "Ylärajahälytys, poistolämpötila", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "TE10_LA": [230,1, "Alarajahälytys, tulolämpötila", "7", "0", "0", "11", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR],
    "FILTER_FA": [240,1, "Suodattimen hälytys", "7", "0", "0", "1", None, BinarySensorDeviceClass.PROBLEM, "mdi:information-outline", READ_ONLY, Platform.BINARY_SENSOR]
}

SENSOR_DICT = {key: SensorSpec(*values) for key, values in SENSOR_DEFS.items()}

#SENSOR_ID_TO_NAME = {values[0]: key for key, values in SENSOR_DEFS.items()}

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

