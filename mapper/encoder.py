import json

from mapper import types
import utils


def ccom(ccom_objects: types.Entity | list[types.Entity]) -> str:

    if not isinstance(ccom_objects, list):
        ccom_objects = [ccom_objects]

    entities = [ccom_object.to_dict() for ccom_object in ccom_objects]
    return json.dumps(
        {"CCOMData": {"@ccomVersion": types.CCOM_VERSION, "entities": entities}}
    )


def iot_ticket(
    ccom_objects: types.SingleDataMeasurement | list[types.SingleDataMeasurement],
) -> str:

    if not isinstance(ccom_objects, list):
        ccom_objects = [ccom_objects]

    entities = [
        {
            "id": getattr(ccom_object.measurementLocation, "UUID"),
            "ts": utils.date_string_to_unix(ccom_object.recorded.dateTime),
            "v": getattr(
                (ccom_object.data.measure or ccom_object.data.binaryObject), "value"
            ),
        }
        for ccom_object in ccom_objects
    ]
    return json.dumps(entities)
