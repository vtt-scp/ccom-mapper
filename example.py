import json

from ccom import decoder
from ccom import encoder

# ccom_object = json.load(ccom_json, object_hook=decoder.decode_ccom)

with open("./mapper/tests/test_ccom_measurements.json") as ccom_file:
    ccom_dict = json.load(ccom_file)
ccom_object = decoder.ccom(ccom_dict)
# print(ccom_object)

ccom_json = json.dumps(encoder.ccom(ccom_object), indent=4)
# print(ccom_json)
# partner_json = encoder.encode_iot(ccom_object)
#
# ccom_json = encoder.encode(encoder.Encoder.CCOM, ccom_object)

iot_message = {
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

ccom_from_iot_object = decoder.iot_ticket(iot_message)
# print(ccom_from_iot_object)
ccom_json = json.dumps(encoder.ccom(ccom_from_iot_object), indent=4)
print(ccom_json)
iot_json = json.dumps(encoder.iot_ticket(ccom_from_iot_object[0]), indent=4)
print(iot_json)
iot_json = json.dumps(encoder.iot_ticket(ccom_from_iot_object[-1]), indent=4)
print(iot_json)
