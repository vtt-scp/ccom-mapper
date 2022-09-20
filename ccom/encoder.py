from typing import Iterable

from ccom import types
import utils


def ccom(ccom_objects: Iterable[types.Entity]) -> dict:
    """Encode CCOM entities to a CCOM message"""

    entities = [ccom_object.to_dict() for ccom_object in ccom_objects]
    return {"CCOMData": {"@ccomVersion": types.CCOM_VERSION, "entities": entities}}


def iot_ticket(
    measurement_location: types.MeasurementLocation,
) -> list[dict]:
    """Encode CCOM MeasurementLocation to IoT-Ticket REST API message"""

    name = utils.require_attribute(measurement_location, "shortNames")[0].text
    unit = None
    if uom := getattr(measurement_location, "defaultUnitOfMeasure"):
        unit = uom.shortNames[0].text
    measurements: list = utils.require_attribute(measurement_location, "measurements")

    entities = []
    for measurement in measurements:
        measure = measurement.data.measure or measurement.data.binaryObject
        entity = {
            "name": name,
            "ts": utils.utc_rfc3339_to_unix(measurement.recorded.dateTime),
            "v": measure.value,
        }
        if unit:
            entity["unit"] = unit
        entities.append(entity)

    return entities
