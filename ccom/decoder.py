from typing import Any, Iterable

from ccom import types
import utils


def ccom(data: dict[str, Any]) -> list[types.Entity]:

    try:
        entities: list[dict[str, Any]] = data["CCOMData"]["entities"]
        return [
            types.CCOM_TYPES[entity["@@type"]].from_dict(entity) for entity in entities
        ]
    except KeyError as error:
        raise ValueError("Invalid CCOM structure") from error


def iot_ticket_values(data: Iterable[dict]) -> list[types.SingleDataMeasurement]:
    """Decode IoT-Ticket values to CCOM SingleDataMeasurements"""

    return [
        types.SingleDataMeasurement.from_dict(
            {
                "@@type": "SingleDataMeasurement",
                "UUID": utils.new_uuid(),
                "recorded": {
                    "@format": "RFC3339",
                    "dateTime": utils.unix_to_utc_rfc3339(point["ts"]),
                },
                "data": {"measure": {"value": point["v"]}},
            }
        )
        for point in data
    ]


def iot_ticket(data: dict[str, Any]) -> list[types.MeasurementLocation]:
    """Decode IoT-Ticket REST API response data to CCOM MeasurementLocations"""

    nodes = data.get("datanodeReads", [])
    decoded = []
    for node in nodes:

        meas_loc: dict = {
            "@@type": "MeasurementLocation",
            "UUID": "TBD",
            "shortNames": [{"text": node["name"]}],
            "measurements": iot_ticket_values(node.get("values")),
        }

        if unit := node.get("unit"):
            meas_loc["defaultUnitOfMeasure"] = {
                "UUID": "TBD",
                "shortNames": [{"text": unit}],
            }

        decoded.append(types.MeasurementLocation.from_dict(meas_loc))

    return decoded
