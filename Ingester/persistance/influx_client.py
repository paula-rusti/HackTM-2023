INFLUXDB_TOKEN = "NY5_CGtuvzZvam-Gxps5yypjciOQrqM0fr12Hh0o6y0wQs-6NEWGGyztbBoT-FXdVLoN7z6svUYLPXpQewu80A=="

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

org = "Home"
url = "http://localhost:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=INFLUXDB_TOKEN, org=org)

bucket = "initial_bucket"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

# for value in range(1000):
#     point = (
#         Point("measurement1")
#         .tag("tagname1", "tagvalue1")
#         .field("field1", value)
#     )
#     write_api.write(bucket=bucket, org="Home", record=point)
#     time.sleep(0.01)  # separate points by 1 second
