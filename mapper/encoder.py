import json
from enum import Enum
from typing import Union, List

from mapper import types
import utils


def encode_ccom(ccom_objects: Union[types.Entity, List[types.Entity]]) -> str:

    if not isinstance(ccom_objects, list):
        ccom_objects = [ccom_objects]

    entities = [ccom_object.to_dict() for ccom_object in ccom_objects]
    return json.dumps(
        {"CCOMData": {"@ccomVersion": types.CCOM_VERSION, "entities": entities}}
    )


def encode_iot(ccom_objects: Union[types.Entity, List[types.Entity]]) -> str:

    if not isinstance(ccom_objects, list):
        ccom_objects = [ccom_objects]

    entities = [
        {
            "id": ccom_object.measurementLocation.UUID,
            "ts": utils.date_string_to_unix(ccom_object.recorded.dateTime),
            "v": (ccom_object.data.measure or ccom_object.data.binaryObject).value,
        }
        for ccom_object in ccom_objects
        if isinstance(ccom_object, types.SingleDataMeasurement)
    ]
    return json.dumps(entities)


class Encoder(Enum):
    CCOM = encode_ccom
    IOT_TICKET = encode_iot


def encode(encoder: Encoder, ccom_objects: Union[types.Entity, List[types.Entity]]):

    if not isinstance(ccom_objects, list):
        ccom_objects = [ccom_objects]

    return encoder(ccom_objects)
