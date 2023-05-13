# how data will look like in influxdb
influxdb_record = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",  # don't store time
        "fields": {
            "Float_value": 0.64,
            "Int_value": 3,
            "String_value": "Text",
            "Bool_value": True
        }
    }
]


def format_data(rabbit_message: dict) -> dict:
    """
    Format the data to be stored in the database
    Returns a dictionary containing 4 objects: temperature, humidity, pressure and gas_resistance
    Each of them represents a measurement of the specified type in the database
    data: {
      "sensor_type": "Bme680Bosh",
      "location_name": "HackTM2023 - Craft",
      "timestamp": 1683977102438,   # discard this
      "temperature": 22.68,
      "humidity": 54.114,
      "pressure": 1011.23,
      "gas_resistance": 274224.4536061566
    }
    """
    pass
    tags = {
        "sensor_type": rabbit_message["sensor_type"],
        "location_name": rabbit_message["location_name"]
    }
    fields_temperature = {
        "value": rabbit_message["temperature"],
    }
    fields_humidity = {
        "value": rabbit_message["humidity"],
    }
    fields_pressure = {
        "value": rabbit_message["pressure"],
    }
    fields_gas_resistance = {
        "value": rabbit_message["gas_resistance"],
    }
    # db measurements
    temp_measurement = {
        "measurement": "temperature",
        "tags": tags,
        "fields": fields_temperature
    }
    humidity_measurement = {
        "measurement": "humidity",
        "tags": tags,
        "fields": fields_humidity
    }
    pressure_measurement = {
        "measurement": "pressure",
        "tags": tags,
        "fields": fields_pressure
    }
    gas_resistance_measurement = {
        "measurement": "gas_resistance",
        "tags": tags,
        "fields": fields_gas_resistance
    }
    return {
        "temperature": temp_measurement,
        "humidity": humidity_measurement,
        "pressure": pressure_measurement,
        "gas_resistance": gas_resistance_measurement
    }
