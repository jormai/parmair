def add_sensor_defs(
    coordinator: ABBPowerOneFimerCoordinator,
    config_entry: ABBPowerOneFimerConfigEntry,
    sensor_list,
    sensor_definitions,
):
    """Class Initializitation."""

    for sensor_info in sensor_definitions.values():
        sensor_data = {
            "name": sensor_info[0],
            "key": sensor_info[1],
            "unit": sensor_info[2],
            "icon": sensor_info[3],
            "device_class": sensor_info[4],
            "state_class": sensor_info[5],
        }
        sensor_list.append(
            ABBPowerOneFimerSensor(coordinator, config_entry, sensor_data)
        )
