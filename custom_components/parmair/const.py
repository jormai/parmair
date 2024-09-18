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

READ_ONLY = False
READ_WRITE = True
class SensorSpec:
    def __init__(self, id: int, comment: str, multiplier: str, min_limit: str, max_limit: str, unit: str, sensor_state_class: str, icon: str, writeable: bool):
        self.id = id
        self.comment = comment
        self.multiplier = multiplier
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.unit = unit
        self.sensor_state_class = sensor_state_class
        self.icon = icon
        self.writeable = writeable


    def __repr__(self):
        return f"DataRow({self.id}, {self.comment}, {self.multiplier}, {self.min_limit}, {self.max_limit}, {self.unit}, {self.sensor_state_class}, {self.icon}, {self.writeable})"
    
SENSOR_DEFS = {
    "ACK_ALARMS": [3, "Hälytysten kuittaus (0=ODOTETAAN KUITTAUSTA, 1=OK/KUITTAA)", "1", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "ALARM_COUNT": [4, "Aktiivisten hälytysten määrä", "1", "1", "0", "100", "", None, "mdi:information-outline", READ_ONLY],
    "TIME_YEAR": [9, "Vuosi", "1", "2023", "2000", "3000", "", None, "mdi:information-outline", READ_WRITE],
    "TIME_MONTH": [10, "Kuukausi", "1", "8", "1", "12", "", None, "mdi:information-outline", READ_WRITE],
    "TIME_DAY": [11, "Päivä", "1", "1", "1", "31", "", None, "mdi:information-outline", READ_WRITE],
    "TIME_HOUR": [12, "Tunnit", "1", "1", "0", "23", "", None, "mdi:information-outline", READ_WRITE],
    "TIME_MIN": [13, "Minuutit", "1", "1", "0", "59", "", None, "mdi:information-outline", READ_WRITE],
    "MULTI_FW_VER": [14, "Multi24 firmware versio", "1", "2.00", "0.00", "100.00", "", None, "mdi:information-outline", READ_ONLY],
    "MULTI_SW_VER": [15, "Multi24 sovelluksen ohjelmaversio", "1", "2.00", "0.00", "100.00", "", None, "mdi:information-outline", READ_ONLY],
    "MULTI_BL_VER": [16, "Multi24 bootloaderin ohjelmaversio", "1", "2.00", "0.00", "100.00", "", None, "mdi:information-outline", READ_ONLY],
    "TE01_M": [20, "Lämpötilamittaus, raitisilma", "2", "0.0", "-50.0", "120.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "TE05_M": [21, "Lämpötilamittaus, LTO kylmäpiste", "2", "0.0", "-50.0", "120.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_ONLY],
    "TE10_M": [22, "Lämpötilamittaus, tuloilma", "2", "0.0", "-50.0", "120.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_ONLY],
    "TE31_M": [23, "Lämpötilamittaus, jäteilma", "2", "0.0", "-50.0", "120.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_ONLY],
    "TE30_M": [24, "Lämpötilamittaus, poistoilma", "2", "0.0", "-50.0", "120.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_ONLY],
    "ME05_M": [25, "Kosteusmittaus, LTO-laite", "2", "0", "0", "100", "%", "SensorStateClass.MOISTURE", "mdi:water-percent", READ_ONLY],
    "QE05_M": [26, "Hiilidioksidimittaus, poistoilma", "2", "0", "-1", "2000", "ppm", "SensorStateClass.CARBON_DIOXIDE", "mdi:molecule-co2", READ_ONLY],
    "TF10_I": [27, "Indikointi, tulopuhallin", "2", "0", "0", "1", "", None, "mdi:information-outline", READ_ONLY],
    "PF30_I": [28, "Indikointi, poistopuhallin", "2", "0", "0", "1", "", None, "mdi:information-outline", READ_ONLY],
    "ME20_M": [29, "Kosteusmittaus, kostea tila", "2", "0", "-1", "100", "%", "SensorStateClass.MOISTURE", "mdi:water-percent", READ_ONLY],
    "QE20_M": [30, "Hiilidioksidimittaus, sisäilma", "2", "0", "-1", "2000", "ppm", "SensorStateClass.CARBON_DIOXIDE", "mdi:molecule-co2", READ_ONLY],
    "EXTERNAL_M": [31, "Ulkoinen ohjaussignaali (0-10V)", "2", "0.0", "-1.0", "100.0", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_ONLY],
    "EXTERNAL_BOOST_M": [35, "Ulkoinen tehostussignaali (1-10V)", "2", "0.0", "-1.0", "100.0", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_ONLY],
    "TE10_DEFLECTION_M": [36, "Tulolämpötilan poikkeutus (+/- 3 astetta), (-9.9=EI käytössä)", "2", "0.0", "-9.9", "3.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_ONLY],
    "TF10_Y": [40, "Säätö, tulopuhallin", "3", "0.0", "0.0", "100.0", "%", "SensorStateClass.SPEED", "mdi:fan", READ_ONLY],
    "PF30_Y": [42, "Säätö, poistopuhallin", "3", "0.0", "0.0", "100.0", "%", "SensorStateClass.SPEED", "mdi:fan", READ_ONLY],
    "TV45_Y": [44, "Säätö, jälkilämmityspatteri", "3", "0.0", "0.0", "100.0", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_ONLY],
    "FG50_Y": [46, "Säätö, LTO", "3", "0.0", "0.0", "100.0", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_ONLY],
    "EC05_Y": [48, "Säätö, esilämmityspatteri", "3", "0.0", "0.0", "100.0", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_ONLY],
    "HP_RAD_O": [50, "Ohjaus, maalämpömoduli", "3", "0", "0", "1", "", None, "mdi:information-outline", READ_ONLY],
    "HOME_SPEED_S": [60, "Asetusarvo, Ilmanvaihtoasetus kotona-tilassa", "4", "3", "1", "5", "", None, "mdi:information-outline", READ_WRITE],
    "TE10_MIN_HOME_S": [61, "Asetusarvo, Tulolämpötilan minimiarvo kotona-tilassa", "4", "17.0", "10.0", "28.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "TE10_CONTROL_MODE_S": [62, "Asetusarvo, lämpötilan säätö (ECO, Vakio)", "4", "0", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "AWAY_SPEED_S": [63, "Asetusarvo, Ilmanvaihtoasetus poissa-tilassa", "4", "1", "1", "5", "", None, "mdi:information-outline", READ_WRITE],
    "TE10_MIN_AWAY_S": [64, "Asetusarvo, Tulolämpötilan minimiarvo poissa-tilassa", "4", "15.0", "10.0", "28.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "BOOST_SETTING_S": [65, "Asetusarvo, Tehostuksen nopeusasetus (nopeus 3-5)", "4", "4", "3", "5", "", None, "mdi:information-outline", READ_WRITE],
    "OVERP_AMOUNT_S": [68, "Asetusarvo, Puhaltimien ylipainetilanteen ylipaineen määrä", "4", "20", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "TP_ENABLE_S": [70, "Asetusarvo, Aikaohjelmakäyttö (0=ei käytössä, 1=käytössä)", "4", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "AUTO_SUMMER_COOL_S": [71, "Asetus, Kesäviilennystoiminto (0=ei käytössä, 1=on, 2=automaatti)", "4", "2", "0", "2", "", None, "mdi:information-outline", READ_WRITE],
    "AUTO_SUMMER_POWER_S": [72, "Asetus, Kesäkäytön tehomuutokset (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "TE30_S": [73, "Asetusarvo, Poistolämpötila (Tavoiteltava huonelämpötila kesäkaudella)", "4", "18.0", "15.0", "25.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "AUTO_HEATER_ENABLE_S": [74, "Asetus, Jälkilämmitysvastus (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "AUTO_COLD_LOWSPEED_S": [75, "Asetus, Automaattinen tehonpudotus kylmissä olosuhteissa (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "COLD_LOWSPEED_S": [76, "Asetus, Tehonpudostus pakkasella, pakkasraja", "4", "-15.0", "-25.0", "10.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "AUTO_HUMIDITY_BOOST_S": [77, "Asetus, Automaattinen kosteustehostus (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "ME05_BOOST_SENSITIVITY": [78, "Asetusarvo, kosteustehostuksen herkkyys", "4", "1", "0", "2", "", None, "mdi:information-outline", READ_WRITE],
    "ME_BST_TE01_LIMIT": [79, "Asetusarvo, Kosteustehostuksen ulkolämpötilaraja", "4", "-10.0", "-15.0", "15.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "AUTO_CO2_BOOST_S": [80, "Asetus, Automaattinen hiilidioksiditehostus (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "AUTO_HOMEAWAY_S": [81, "Asetus, Automaattinen kotona/poissa (CO2) (0=ei käytössä, 1=automaatti)", "4", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "QE_HOME_S": [82, "Asetusarvo, CO2 kotona-raja", "4", "500", "100", "2000", "ppm", "SensorStateClass.CARBON_DIOXIDE", "mdi:molecule-co2", READ_WRITE],
    "QE_BOOST_S": [83, "Asetusarvo, CO2 tehostusraja (tehostuksen aloitus)", "4", "800", "100", "2000", "ppm", "SensorStateClass.CARBON_DIOXIDE", "mdi:molecule-co2", READ_WRITE],
    "FILTER_INTERVAL_S": [90, "Asetusarvo, Suodattimien vaihtoväli (0=3kk, 1=4kk, 2=6kk)", "4", "0", "0", "2", "", None, "mdi:information-outline", READ_WRITE],
    "HP_RAD_MODE": [91, "Asetusarvo, maalämpömoduulin toiminta (0=Off, 1=On, 2=Auto)", "4", "2", "0", "2", "", None, "mdi:information-outline", READ_WRITE],
    "HP_RAD_WINTER": [92, "Asetusarvo, maalämpömoduulin käyttöraja talvi", "4", "0.0", "-30.0", "15.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "HP_RAD_SUMMER": [93, "Asetusarvo, maalämpömoduulin käyttöraja kesä", "4", "15.0", "0.0", "40.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "HEATING_SEASON_AVERAGE": [94, "Asetusarvo, Lämmityskausi (24h raitis lämpötila)", "4", "14.0", "6.0", "50.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "HEATING_SEASON_MOMENT": [95, "Asetusarvo, Lämmityskausi (hetkellinen raitis lämpötila)", "4", "8.0", "-5.0", "50.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "TE10_MIN_SUMMER_S": [96, "Asetusarvo, Tulolämpötilan kesä-tilassa", "4", "12.0", "10.0", "25.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "TE10_MAX_S": [97, "Asetusarvo, Tulolämpötilan maksimiarvo", "4", "25.0", "10.0", "35.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "BST_TE01_LIMIT": [98, "Asetusarvo, Tehostuksen ulkolämpötilaraja / CO2, 0-10V", "4", "-10.0", "-15.0", "0.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "M10_TYPE": [105, "Mittauspaikan 10 tyyppi. 0=Ei käytössä.", "1", "0", "0", "27", "", None, "mdi:information-outline", READ_WRITE],
    "M11_TYPE": [106, "Mittauspaikan 11 tyyppi. 0=Ei käytössä.", "1", "0", "0", "27", "", None, "mdi:information-outline", READ_WRITE],
    "M12_TYPE": [107, "Mittauspaikan 12 tyyppi. 0=Ei käytössä.", "1", "0", "0", "27", "", None, "mdi:information-outline", READ_WRITE],
    "SF_SPEED1_S": [108, "Asetusarvo, Tulopuhaltimen nopeusasetus 1", "1", "20", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "SF_SPEED2_S": [109, "Asetusarvo, Tulopuhaltimen nopeusasetus 2", "1", "35", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "SF_SPEED3_S": [110, "Asetusarvo, Tulopuhaltimen nopeusasetus 3", "1", "60", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "SF_SPEED4_S": [111, "Asetusarvo, Tulopuhaltimen nopeusasetus 4", "1", "75", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "SF_SPEED5_S": [112, "Asetusarvo, Tulopuhaltimen nopeusasetus 5", "1", "90", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "EF_SPEED1_S": [113, "Asetusarvo, Poistopuhaltimen nopeusasetus 1", "1", "20", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "EF_SPEED2_S": [114, "Asetusarvo, Poistopuhaltimen nopeusasetus 2", "1", "35", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "EF_SPEED3_S": [115, "Asetusarvo, Poistopuhaltimen nopeusasetus 3", "1", "60", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "EF_SPEED4_S": [116, "Asetusarvo, Poistopuhaltimen nopeusasetus 4", "1", "75", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "EF_SPEED5_S": [117, "Asetusarvo, Poistopuhaltimen nopeusasetus 5", "1", "90", "0", "100", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_WRITE],
    "SENSOR_TE_COR": [120, "Lämpötilan korjaus", "10", "0.0", "-5.0", "5.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "SENSOR_ME_COR": [121, "Kosteuden korjaus", "1", "0", "-20", "20", "%", "SensorStateClass.MOISTURE", "mdi:water-percent", READ_WRITE],
    "SENSOR_CO2_COR": [122, "Hiilidioksidin korjaus", "1", "0", "-500", "500", "ppm", "SensorStateClass.CARBON_DIOXIDE", "mdi:molecule-co2", READ_WRITE],
    "HEATPUMP_RADIATOR_ENABLE": [124, "Maalämpöpatteri (0=Ei asennettu, 1=Asennettu)", "1", "0", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "VENT_MACHINE": [125, "IV-koneen tyyppikoodi", "1", "1", "-1000", "1000", "", None, "mdi:information-outline", READ_ONLY],
    "TE10_MIN_S": [129, "Asetusarvo, Tulolämpötilan minimiarvo jonka käyttäjä voi asettaa", "10", "10.0", "10.0", "25.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "TE10_BASE_S": [137, "Asetusarvo, Tulolämpötilan perusasetusarvo, josta voidaan potikalla poikkeuttaa.", "10", "17.0", "15.0", "25.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "BST_MINTIME": [140, "Asetusarvo, Tehostuksen minimiaika (min) / LTO, CO2, 0-10V", "1", "5", "1", "60", "min", "SensorStateClass.DURATION", "mdi:clock-time-nine-outline", READ_WRITE],
    "CO2_MINTIME": [141, "Asetusarvo, Automaattinen kotona-poissa minimiaika", "1", "15", "1", "600", "min", "SensorStateClass.DURATION", "mdi:clock-time-nine-outline", READ_WRITE],
    "BST_TIME_LIMIT": [144, "Asetusarvo, Kosteus ja CO2-tehostusten maksimiaika", "1", "1440", "15", "1440", "min", "SensorStateClass.DURATION", "mdi:clock-time-nine-outline", READ_WRITE],
    "UNIT_CONTROL_FO": [180, "IV-koneen ohjaus (0=Off, 1=On)", "1", "1", "0", "1", "", None, "mdi:information-outline", READ_WRITE],
    "USERSTATECONTROL_FO": [181, "MAC 2 User state control from screen. 0=Off, 1=Away, 2=Home, 3=Boost, 4=Sauna, 5=Fireplace", "2", "1", "0", "5", "", None, "mdi:information-outline", READ_WRITE],
    "DFRST_FI": [182, "Fiktiivinen indikointi, LTO:n sulatus päällä/pois", "1", "0", "0", "1", "", None, "mdi:information-outline", READ_ONLY],
    "FG50_EA_M": [183, "Fiktiivinen mittaus, LTO:n hyötysuhde", "1", "0.0", "0.0", "100.0", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_ONLY],
    "FILTER_STATE_FI": [184, "Fiktiivinen asetus, Suodattimen kunto (0=Idle, 1=Kuittaa vaihto, 2=Muistutushälytys)", "1", "0", "0", "2", "", None, "mdi:information-outline", READ_WRITE],
    "SENSOR_STATUS": [185, "Yhdistelmäanturin tila (1=Ok, 0=Initoimatta, -1=Modbuskommunikaatiovirhe, -2=Data puuttuu)", "1", "0", "-2", "1", "", None, "mdi:information-outline", READ_ONLY],
    "SUMMER_MODE_I": [189, "Tilatieto, Kausi. 0=Talvi, 1=Väli, 2=Kesä", "1", "0", "0", "2", "", None, "mdi:information-outline", READ_ONLY],
    "SUMMER_POWER_CHANGE_FM": [190, "Kesätilanteen tehonsäätö", "1", "0", "-1", "1", "", None, "mdi:information-outline", READ_ONLY],
    "HUMIDITY_FM": [191, "Laskettu kosteus", "100", "0.00", "0.00", "100.00", "g/kg", "SensorStateClass.MOISTURE", "mdi:water-percent", READ_ONLY],
    "ME05_AVG_FM": [192, "Fiktiivinen mittaus, LTO:n kosteusmittauksen 24h keskiarvo", "10", "0.0", "0.0", "100.0", "%", "SensorStateClass.MOISTURE", "mdi:water-percent", READ_ONLY],
    "PWR_LIMIT_FY": [199, "Fiktiivinen säätö, puhaltimien tehonrajoitus", "10", "0.0", "0.0", "100.0", "%", "SensorStateClass.POWER_FACTOR", "mdi:percent-circle", READ_ONLY],
    "TE01_AVG_FM": [213, "Ulkolämpötilan vrk keskiarvo", "10", "0.0", "-50.0", "50.0", "°C", "SensorStateClass.TEMPERATURE", "mdi:temperature-celsius", READ_WRITE],
    "TE01_FA": [220, "Vikahälytys, raitisilman lämpötila / anturivika", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TE10_FA": [221, "Vikahälytys, tulolämpötila / anturivika", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TE05_FA": [222, "Vikahälytys, tulolämpötila LTO:n jälkeen / anturivika", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TE30_FA": [223, "Vikahälytys, poistolämpötila / anturivika", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TE31_FA": [224, "Vikahälytys, jäteilman lämpötila / anturivika", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "ME05_FA": [225, "Vikahälytys, LTO:n kosteus / anturivika", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TF10_CA": [226, "Ristiriitahälytys, tulopuhallin", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "PF30_CA": [227, "Ristiriitahälytys, poistopuhallin", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TE10_HA": [228, "Ylärajahälytys, tulolämpötila", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TE30_HA": [229, "Ylärajahälytys, poistolämpötila", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "TE10_LA": [230, "Alarajahälytys, tulolämpötila", "1", "0", "0", "11", "", None, "mdi:information-outline", READ_ONLY],
    "FILTER_FA": [240, "Suodattimen hälytys", "1", "0", "0", "1", "", None, "mdi:information-outline", READ_ONLY]
}

SENSOR_DICT = {key: SensorSpec(*values) for key, values in SENSOR_DEFS.items()}

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
