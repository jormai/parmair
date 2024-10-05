"""Constants for Parmair MAC v2."""
DOMAIN = "parmair"
import csv
from enum import Enum
import json
import re
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

from _ctypes import PyObj_FromPtr
import json
import re

class NoIndent(object):
    """ Value wrapper. """
    def __init__(self, value):
        self.value = value


class MyJSONEncoder(json.JSONEncoder):

  def iterencode(self, o, _one_shot=False):
    list_lvl = 0
    for s in super(MyJSONEncoder, self).iterencode(o, _one_shot=_one_shot):
      if s.startswith('['):
        list_lvl += 1
        s = s.replace('\n', '').rstrip()
      elif 0 < list_lvl:
        s = s.replace('\n', '').rstrip()
        if s and s[-1] == ',':
          s = s[:-1] + self.item_separator
        elif s and s[-1] == ':':
          s = s[:-1] + self.key_separator
      if s.endswith(']'):
        list_lvl -= 1
      yield s
    
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
DEFAULT_NAME = "Parmair"
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
    """Class to hold sensor specification"""
    @property
    def name(self) -> str:
        """Get the name."""
        return self._name
    
    def __init__(self, id: int, multiplier: int, name: str, group: str, factory_setting: str,  min_limit: str, max_limit: str, unit: str, sensor_device_class: SensorDeviceClass|BinarySensorDeviceClass|None, icon: str, writeable: bool, platform:Platform=Platform.SENSOR,options:list[str]=None):
        """Init the class."""
        self.id = id
        self._name = name
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
        """Print."""
        return f"DataRow({self.id}, {self.name}, {self.group}, {self.multiplier}, {self.min_limit}, {self.max_limit}, {self.unit}, {self.sensor_device_class}, {self.icon}, {self.writeable})"
CONF_POWER_SWITCH="UNIT_CONTROL_FO"
CONF_CURRENT_HUMIDITY="ME05_M"
CONF_CURRENT_AIRFLOW_INPUT="TE10_M"
CONF_CURRENT_FAN_SPEED="FAN_SPEED_I"
CONF_PRESET_MODE="USERSTATECONTROL_FO"
#Sensor device groups
GROUPS = {
    "1": "system_settings",
    "2": "physical_inputs",
    "3": "physical_outputs",
    "4": "settings",
    "10": "configuration_params",
    "7": "alarms",
    "11": "essentials"
}
"""
Perhaps this includes filter change date?
2024-10-05 14:40:45.965 DEBUG (SyncWorker_0) [custom_components.parmair.api] Skipping 195=2024
2024-10-05 14:40:45.965 DEBUG (SyncWorker_0) [custom_components.parmair.api] Skipping 196=5
2024-10-05 14:40:45.965 DEBUG (SyncWorker_0) [custom_components.parmair.api] Skipping 197=9
2024-10-05 14:40:45.965 DEBUG (SyncWorker_0) [custom_components.parmair.api] Skipping 198=2024
"""
"""Definition of all sensors except climate sensor."""
# note, id must be ascending    
SENSOR_DEFS = {
"ACK_ALARMS":[3,1,"ack_alarms","1","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["waiting_ack","ok_ack"]],
"ALARM_COUNT":[4,1,"alarm_count","1","0","0","100",None,None,"mdi:information-outline",READ_ONLY],
"TIME_YEAR":[9,1,"year","1","2023","2000","3000",None,None,"mdi:information-outline",READ_WRITE],
"TIME_MONTH":[10,1,"month","1","8","1","12",None,None,"mdi:information-outline",READ_WRITE],
"TIME_DAY":[11,1,"day","1","1","1","31",None,None,"mdi:information-outline",READ_WRITE],
"TIME_HOUR":[12,1,"hours","1","1","0","23",None,None,"mdi:information-outline",READ_WRITE],
"TIME_MIN":[13,1,"minutes","1","1","0","59",None,None,"mdi:information-outline",READ_WRITE],
"MULTI_FW_VER":[14,100,"multi_fw_ver","1","2.00","0.00","100.00",None,None,"mdi:information-outline",READ_ONLY],
"MULTI_SW_VER":[15,100,"multi_app_ver","1","2.00","0.00","100.00",None,None,"mdi:information-outline",READ_ONLY],
"MULTI_BL_VER":[16,100,"multi_boot_ver","1","2.00","0.00","100.00",None,None,"mdi:information-outline",READ_ONLY],
"TE01_M":[20,10,"temp_fresh_air","11","0.0","-50.0","120.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_ONLY],
"TE05_M":[21,10,"temp_hr_cold_point","2","0.0","-50.0","120.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_ONLY],
"TE10_M":[22,10,"temp_supply_air","11","0.0","-50.0","120.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_ONLY],
"TE31_M":[23,10,"temp_exhaust_air","2","0.0","-50.0","120.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_ONLY],
"TE30_M":[24,10,"temp_return_air","11","0.0","-50.0","120.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_ONLY],
"ME05_M":[25,1,"humidity_hrv_device","2","0","0","100","%",SensorDeviceClass.MOISTURE,"mdi:water-percent",READ_ONLY],
"QE05_M":[26,1,"co2_return_air","2","0","-1","2000","ppm",SensorDeviceClass.CO2,"mdi:molecule-co2",READ_ONLY],
"TF10_I":[27,1,"fan_ind_supply","2","0","0","1",None,BinarySensorDeviceClass.RUNNING,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"PF30_I":[28,1,"fan_ind_return","2","0","0","1",None,BinarySensorDeviceClass.RUNNING,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"ME20_M":[29,1,"humid_wet_room","2","0","-1","100","%",SensorDeviceClass.MOISTURE,"mdi:water-percent",READ_ONLY],
"QE20_M":[30,1,"co2_indoor_air","11","0","-1","2000","ppm",SensorDeviceClass.CO2,"mdi:molecule-co2",READ_ONLY],
"EXTERNAL_M":[31,10,"ext_ctrl_signal","2","0.0","-1.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_ONLY],
"EXTERNAL_BOOST_M":[35,10,"ext_boost_signal","2","0.0","-1.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_ONLY],
"TE10_DEFLECTION_M":[36,10,"supply_temp_adjust","2","0.0","-9.9","3.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_ONLY],
"TF10_Y":[40,10,"fan_ctrl_supply","3","0.0","0.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:fan",READ_ONLY],
"PF30_Y":[42,10,"fan_ctrl_return","3","0.0","0.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:fan",READ_ONLY],
"TV45_Y":[44,10,"ctrl_post_heater","3","0.0","0.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_ONLY],
"FG50_Y":[46,10,"ctrl_heat_recovery","3","0.0","0.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_ONLY],
"EC05_Y":[48,10,"ctrl_pre_heater","3","0.0","0.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_ONLY],
"HP_RAD_O":[50,1,"ctrl_geo_heat_module","3","0","0","1",None,None,"mdi:information-outline",READ_ONLY],
"HOME_SPEED_S":[60,1,"setpoint_vent_home","4","3","1","5",None,None,"mdi:information-outline",READ_WRITE,Platform.NUMBER],
"TE10_MIN_HOME_S":[61,10,"setpoint_min_temp_home","4","17.0","10.0","28.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"TE10_CONTROL_MODE_S":[62,1,"setpoint_temp_ctrl","4","0","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["eco","standard"]],
"AWAY_SPEED_S":[63,1,"setpoint_vent_away","4","1","1","5",None,None,"mdi:information-outline",READ_WRITE,Platform.NUMBER],
"TE10_MIN_AWAY_S":[64,10,"setpoint_min_temp_away","4","15.0","10.0","28.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"BOOST_SETTING_S":[65,1,"setpoint_boost_speed","4","4","3","5",None,SensorDeviceClass.SPEED,"mdi:information-outline",READ_WRITE,Platform.NUMBER],
"OVERP_AMOUNT_S":[68,1,"setpoint_over_press","4","20","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"TP_ENABLE_S":[70,1,"setpoint_time_prog","4","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","in_use"]],
"AUTO_SUMMER_COOL_S":[71,1,"setting_summer_cool","4","2","0","2",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","in_use","automatic"]],
"AUTO_SUMMER_POWER_S":[72,1,"setting_summer_perf","4","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","automatic"]],
"TE30_S":[73,10,"setpoint_exh_temp","4","18.0","15.0","25.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"AUTO_HEATER_ENABLE_S":[74,1,"setting_post_heater","4","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","automatic"]],
"AUTO_COLD_LOWSPEED_S":[75,1,"setting_auto_cold_cut","4","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","automatic"]],
"COLD_LOWSPEED_S":[76,10,"setting_cold_cut_temp","4","-15.0","-25.0","10.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"AUTO_HUMIDITY_BOOST_S":[77,1,"setting_auto_humid_boost","4","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","automatic"]],
"ME05_BOOST_SENSITIVITY":[78,1,"setpoint_humidity_sens","4","1","0","2",None,None,"mdi:information-outline",READ_WRITE,Platform.NUMBER],
"ME_BST_TE01_LIMIT":[79,10,"setting_humidity_temp_limit","4","-10.0","-15.0","15.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"AUTO_CO2_BOOST_S":[80,1,"setting_auto_co2_boost","4","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","automatic"]],
"AUTO_HOMEAWAY_S":[81,1,"setting_auto_home_away_co2","4","1","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_in_use","automatic"]],
"QE_HOME_S":[82,1,"setpoint_co2_home","4","500","100","2000","ppm",SensorDeviceClass.CO2,"mdi:molecule-co2",READ_WRITE,Platform.NUMBER],
"QE_BOOST_S":[83,1,"setpoint_co2_boost","4","800","100","2000","ppm",SensorDeviceClass.CO2,"mdi:molecule-co2",READ_WRITE,Platform.NUMBER],
"FILTER_INTERVAL_S":[90,1,"setpoint_filter_change","4","0","0","2",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["3m","4m","6m"]],
"HP_RAD_MODE":[91,1,"setting_geo_heat_op","4","2","0","2",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["off","on","automatic"]],
"HP_RAD_WINTER":[92,10,"setting_geo_heat_limit_winter","4","0.0","-30.0","15.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"HP_RAD_SUMMER":[93,10,"setting_geo_heat_limit_summer","4","15.0","0.0","40.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"HEATING_SEASON_AVERAGE":[94,10,"setpoint_heating_season_24h","4","14.0","6.0","50.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"HEATING_SEASON_MOMENT":[95,10,"setpoint_heating_season_now","4","8.0","-5.0","50.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"TE10_MIN_SUMMER_S":[96,10,"setpoint_supply_temp_summer","4","12.0","10.0","25.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"TE10_MAX_S":[97,10,"setpoint_supply_max_temp","4","25.0","10.0","35.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"BST_TE01_LIMIT":[98,10,"setpoint_boost_temp_limit","4","-10.0","-15.0","0.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"M10_TYPE":[105,1,"meas_point_type_10","10","0","0","27",None,None,"mdi:information-outline",READ_WRITE,Platform.NUMBER],
"M11_TYPE":[106,1,"meas_point_type_11","10","0","0","27",None,None,"mdi:information-outline",READ_WRITE,Platform.NUMBER],
"M12_TYPE":[107,1,"meas_point_type_12","10","0","0","27",None,None,"mdi:information-outline",READ_WRITE,Platform.NUMBER],
"SF_SPEED1_S":[108,1,"setting_supply_fan_speed_1","10","20","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"SF_SPEED2_S":[109,1,"setting_supply_fan_speed_2","10","35","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"SF_SPEED3_S":[110,1,"setting_supply_fan_speed_3","10","60","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"SF_SPEED4_S":[111,1,"setting_supply_fan_speed_4","10","75","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"SF_SPEED5_S":[112,1,"setting_supply_fan_speed_5","10","90","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"EF_SPEED1_S":[113,1,"setting_return_fan_speed_1","10","20","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"EF_SPEED2_S":[114,1,"setting_return_fan_speed_2","10","35","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"EF_SPEED3_S":[115,1,"setting_return_fan_speed_3","10","60","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"EF_SPEED4_S":[116,1,"setting_return_fan_speed_4","10","75","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"EF_SPEED5_S":[117,1,"setting_return_fan_speed_5","10","90","0","100","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_WRITE,Platform.NUMBER],
"SENSOR_TE_COR":[120,10,"temp_correction","10","0.0","-5.0","5.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"SENSOR_ME_COR":[121,1,"humidity_correction","10","0","-20","20","%",SensorDeviceClass.MOISTURE,"mdi:water-percent",READ_WRITE,Platform.NUMBER],
"SENSOR_CO2_COR":[122,1,"co2_correction","10","0","-500","500","ppm",SensorDeviceClass.CO2,"mdi:molecule-co2",READ_WRITE,Platform.NUMBER],
"HEATPUMP_RADIATOR_ENABLE":[124,1,"geo_heat_coil","10","0","0","1",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["not_installed","installed"]],
"VENT_MACHINE":[125,1,"hrv_type_code","10","1","-1000","1000",None,None,"mdi:information-outline",READ_ONLY],
"TE10_MIN_S":[129,10,"setpoint_min_supply_user","10","10.0","10.0","25.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"TE10_BASE_S":[137,10,"setpoint_base_supply_temp","10","17.0","15.0","25.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_WRITE,Platform.NUMBER],
"BST_MINTIME":[140,1,"setpoint_boost_min_time","10","5","1","60","min",SensorDeviceClass.DURATION,"mdi:clock-time-nine-outline",READ_WRITE,Platform.NUMBER],
"CO2_MINTIME":[141,1,"setpoint_auto_home_away_min","10","15","1","600","min",SensorDeviceClass.DURATION,"mdi:clock-time-nine-outline",READ_WRITE,Platform.NUMBER],
"BST_TIME_LIMIT":[144,1,"setpoint_boost_max_time","10","1440","15","1440","min",SensorDeviceClass.DURATION,"mdi:clock-time-nine-outline",READ_WRITE,Platform.NUMBER],
"UNIT_CONTROL_FO":[180,1,"hrv_control","11","1","0","1", SwitchDeviceClass.SWITCH,None,"mdi:information-outline",READ_WRITE,Platform.SWITCH],
"USERSTATECONTROL_FO":[181,1,"mac2_user_state","11","1","0","5",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["off","away","home","boost","sauna","fireplace"]],
"DFRST_FI":[182,1,"fake_ind_hrv","11","0","0","1",None,BinarySensorDeviceClass.RUNNING,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"FG50_EA_M":[183,10,"fake_meas_hrv_eff","11","0.0","0.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_ONLY],
"FILTER_STATE_FI":[184,1,"fake_setting_filter_cond","11","0","0","2",None,None,"mdi:information-outline",READ_WRITE,Platform.SELECT,["idle","ack_needed","reminder_alarm"]],
"SENSOR_STATUS":[185,1,"comb_sensor_state","1","0","-2","1",None,None,"mdi:information-outline",READ_ONLY],
"FAN_SPEED_I":[187,1,"status_fan_speed","11","0","1","4",None,None,"mdi:information-outline",READ_ONLY],
"SUMMER_MODE_I":[189,1,"status_season","1","0","0","2",None,None,"mdi:information-outline",READ_ONLY],
"SUMMER_POWER_CHANGE_FM":[190,1,"summer_power_ctrl","1","0","-1","1",None,None,"mdi:information-outline",READ_ONLY],
"HUMIDITY_FM":[191,100,"calc_humidity","1","0.00","0.00","100.00","g/kg",SensorDeviceClass.MOISTURE,"mdi:water-percent",READ_ONLY],
"ME05_AVG_FM":[192,10,"fake_meas_hrv_humid","11","0.0","0.0","100.0","%",SensorDeviceClass.MOISTURE,"mdi:water-percent",READ_ONLY],
"PWR_LIMIT_FY":[199,10,"fake_ctrl_fan_limit","1","0.0","0.0","100.0","%",SensorDeviceClass.POWER_FACTOR,"mdi:percent-circle",READ_ONLY],
"TE01_AVG_FM":[213,10,"ext_temp_daily_avg","1","0.0","-50.0","50.0","°C",SensorDeviceClass.TEMPERATURE,"mdi:temperature-celsius",READ_ONLY],
"TE01_FA":[220,1,"error_temp_fresh_air","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TE10_FA":[221,1,"error_temp_supply","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TE05_FA":[222,1,"error_temp_supply_hrv","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TE30_FA":[223,1,"error_temp_return","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TE31_FA":[224,1,"error_temp_exhaust","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"ME05_FA":[225,1,"error_humid_hrv","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TF10_CA":[226,1,"conf_alarm_supply_fan","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"PF30_CA":[227,1,"conf_alarm_return_fan","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TE10_HA":[228,1,"high_limit_temp_supply","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TE30_HA":[229,1,"high_limit_temp_return","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"TE10_LA":[230,1,"low_limit_temp_supply","7","0","0","11",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR],
"FILTER_FA":[240,1,"filter_alarm","7","0","0","1",None,BinarySensorDeviceClass.PROBLEM,"mdi:information-outline",READ_ONLY,Platform.BINARY_SENSOR]
}
#Create dictionary of sensors
SENSOR_DICT = {key: SensorSpec(*values) for key, values in SENSOR_DEFS.items()}


