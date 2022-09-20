from ccom import types


def sort_measurements_by_locations(
    measurements: list[types.SingleDataMeasurement],
) -> list[types.MeasurementLocation]:

    i: int = 0
    locations: dict[str, types.MeasurementLocation] = {}
    for measurement in measurements:
        if not measurement.measurementLocation:
            raise ValueError(
                f"Measurement '{measurement.UUID}' missing measurementLocation."
            )

        location = measurement.measurementLocation
        measurement.measurementLocation = None
        location = locations.get(location.UUID) or location

        if not location.measurements:
            location.measurements = []
        location.measurements.append(measurement)
        locations[location.UUID] = location

    return list(locations.values())
