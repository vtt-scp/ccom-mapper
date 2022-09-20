import json
from typing import cast

from ccom import decoder, encoder, manipulator
from ccom import types

with open("./ccom/tests/test_ccom_measurements.json") as ccom_file:
    ccom_dict = json.load(ccom_file)

# Decode to CCOM entites as Python dataclasses
ccom_entities = decoder.ccom(ccom_dict)

# Cast entities to the expected CCOM type
ccom_measurements = cast(list[types.SingleDataMeasurement], ccom_entities)
print("Decoded measurements:")
for measurement in ccom_measurements:
    print(measurement.recorded, measurement.data)
print("")

# Encode measurements back to CCOM and JSON
ccom_json = json.dumps(encoder.ccom(ccom_entities), indent=4)
print("CCOM JSON message:", ccom_json, sep="\n", end="\n\n")

# Sort the measurements by measurement locations
measurement_locations = manipulator.sort_measurements_by_locations(ccom_measurements)

# Convert the same measurement locations to another format supported by partner system
print("CCOM message encoded to partner messages:")
for location in measurement_locations:
    partner_json = json.dumps(encoder.iot_ticket(measurement_locations[0]), indent=4)
    print(location.UUID, partner_json, sep="\n")
print("")

# Example partner system message
partner_message = {
    "datanodeReads": [
        {
            "name": "Latitude",
            "dataType": "long",
            "values": [{"v": "60", "ts": 1417636260139}],
        },
        {
            "name": "Temperature",
            "path": "Engine/Core",
            "unit": "c",
            "dataType": "double",
            "values": [
                {"v": "65", "ts": 1417636260152},
                {"v": "63", "ts": 1417636260152},
                {"v": "73", "ts": 1417636260152},
            ],
        },
    ]
}
print(
    "Original partner message:",
    json.dumps(partner_message, indent=4),
    sep="\n",
    end="\n\n",
)

# Decode to CCOM measurement locations
ccom_measurement_locations = decoder.iot_ticket(partner_message)

# Encode to CCOM message and JSON
ccom_json = json.dumps(encoder.ccom(ccom_measurement_locations), indent=4)
print("Partner message encoded to a CCOM JSON message:", ccom_json, sep="\n")

# Encode measurement locations back to partner messages
original_message = {
    "datanodeReads": [
        json.dumps(encoder.iot_ticket(location))
        for location in ccom_measurement_locations
    ]
}
