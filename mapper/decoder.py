from typing import Any

from mapper import types
import utils


def simple_decode_ccom(dct: dict[str, Any]) -> list[types.Entity] | None:

    try:
        entities: list[dict[str, Any]] = dct["CCOMData"]["entities"]
        return [
            types.CCOM_TYPES[entity.get("@@type")].from_dict(entity)
            for entity in entities
        ]
    except KeyError as error:
        raise ValueError("Invalid CCOM structure") from error


def decode_ccom(dct: dict) -> types.Entity | dict:
    """Decode CCOM dictionary object to CCOM types"""

    if ccom_type_name := dct.get("@@type"):
        return types.CCOM_TYPES[ccom_type_name].from_dict(dct)
    elif "CCOMData" in dct:
        return dct["CCOMData"]["entities"]
    return dct


def decode_iot(dct: dict) -> types.SingleDataMeasurement | dict:
    """Decode IoT-Ticket dictionary object to CCOM types"""

    if dct.keys() >= {"id", "v", "ts"}:
        return types.SingleDataMeasurement.from_dict(
            {
                "UUID": utils.new_uuid(),
                "recorded": {
                    "@format": "RFC3339",
                    "dateTime": utils.unix_to_date_string(dct["ts"]),
                },
                "data": {"measure": {"value": dct["v"]}},
                "measurementLocation": {"UUID": dct["id"]},
            }
        )

    return dct


def iot_ticket_value(dct: dict) -> types.SingleDataMeasurement:
    """Decode IoT-Ticket value to CCOM SingleDataMeasurement"""

    timestamp = utils.unix_to_date_string(dct["ts"])
    value = dct["v"]

    return types.SingleDataMeasurement.from_dict(
        {
            "@@type": "SingleDataMeasurement",
            "UUID": utils.new_uuid(),
            "recorded": {
                "@format": "RFC3339",
                "dateTime": timestamp,
            },
            "data": {"measure": {"value": value}},
        }
    )


def iot_ticket(dct: dict):
    """Decode IoT-Ticket REST API response data to CCOM MeasurementLocation"""

    decoded = []
    for node in dct.get("datanodeReads", []):

        meas_loc = {
            "@@type": "MeasurementLocation",
            "UUID": "TODO",
            "shortNames": [{"text": node["name"]}],
            "measurements": [
                iot_ticket_value(measurement) for measurement in node.get("values", [])
            ],
        }
        if unit := node.get("unit"):
            meas_loc["defaultUnitOfMeasure"] = {"UUID": "TODO", "name": unit}

        decoded.append(types.MeasurementLocation.from_dict(meas_loc))

    return decoded
