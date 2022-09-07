import json

from mapper import decoder
from mapper import encoder

# ccom_object = json.load(ccom_json, object_hook=decoder.decode_ccom)

with open("./ccom/tests/test_ccom_measurements.json") as ccom_file:
    ccom_dict = json.load(ccom_file)
ccom_object = decoder.simple_decode_ccom(ccom_dict)
print(ccom_object)

ccom_json = encoder.encode_ccom(ccom_object)
print(ccom_json)
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

ccom_object = decoder.iot_ticket(iot_message)
print(ccom_object)
ccom_json = encoder.encode_ccom(ccom_object)
print(ccom_json)
