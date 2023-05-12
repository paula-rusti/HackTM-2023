Receives data from RabbitMQ and saves it to a MongoDB database.
Exposes Web api for retrieving the latest data from the sensors.

data format
```
{
    "temperature": 24.0,
    "pressure": 1000.0,
    "humidity": 50.0,
    "gas_resistance": 1000.0,
    "sensor_type": string,
    "timestamp": "3424423424"
}
```