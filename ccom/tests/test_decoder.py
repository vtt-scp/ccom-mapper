import os
import json

import pytest

from mapper import types, decoder, validator
import utils


# Test CCOM message decoding


TEST_CCOM_JSON_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "test_ccom_measurements.json"
)


@pytest.fixture(scope="session")
def ccom_dict():
    with open(TEST_CCOM_JSON_FILE) as ccom_json:
        ccom_dict = json.load(ccom_json)
    return ccom_dict


@pytest.fixture(scope="session")
def ccom_parsed():
    with open(TEST_CCOM_JSON_FILE) as ccom_json:
        ccom_object = json.load(ccom_json)
    ccom_parsed = decoder.ccom(ccom_object)
    print(ccom_parsed)
    return ccom_parsed


def test_ccom_validate_test_json(ccom_dict):
    assert validator.validate(ccom_dict) is None


def test_ccom_entities_parsed(ccom_parsed):
    assert isinstance(ccom_parsed, list)
    assert len(ccom_parsed) > 0


def test_ccom_number_of_entities(ccom_dict, ccom_parsed):
    assert len(ccom_dict["CCOMData"]["entities"]) == len(ccom_parsed)


def test_ccom_type_of_entities(ccom_dict, ccom_parsed):
    entities = ccom_dict["CCOMData"]["entities"]

    for original, parsed in zip(entities, ccom_parsed):
        assert original["@@type"] == parsed.__class__.__name__


def test_ccom_single_data_measurement_data(ccom_dict, ccom_parsed):
    entities = ccom_dict["CCOMData"]["entities"]

    for original, parsed in zip(entities, ccom_parsed):
        data = original["data"]
        # Test measure
        if data.get("measure") and parsed.data.measure:
            assert isinstance(parsed.data.measure, types.Measure)
            assert data["measure"]["value"] == parsed.data.measure.value
        # Test binaryObject
        elif data.get("binaryObject") and parsed.data.binaryObject:
            assert isinstance(parsed.data.binaryObject, types.BinaryObject)
            assert data["binaryObject"]["value"] == parsed.data.binaryObject.value


# Test IoT-Ticket message decoding


@pytest.fixture(scope="session")
def iot_dict():
    return {
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
                    {"ts": 1654699434123123, "v": 1.234},
                    {"ts": 1654699534123246, "v": 2.345},
                ],
            },
        ]
    }


@pytest.fixture(scope="session")
def iot_json(iot_dict):
    return json.dumps(iot_dict)


@pytest.fixture(scope="session")
def iot_parsed(iot_json):
    return decoder.iot_ticket(json.loads(iot_json))


def test_iot_number_of_entities(iot_dict, iot_parsed):
    assert len(iot_dict["datanodeReads"]) == len(iot_parsed)


def test_iot_number_of_measurements(iot_dict, iot_parsed):
    for original, parsed in zip(iot_dict["datanodeReads"], iot_parsed):
        assert len(original["values"]) == len(parsed.measurements)


def test_iot_type_of_entities(iot_parsed):
    for parsed in iot_parsed:
        assert isinstance(parsed, types.MeasurementLocation)


def test_iot_value_match(iot_dict, iot_parsed):
    for original, parsed in zip(iot_dict["datanodeReads"], iot_parsed):
        assert original["name"] == parsed.shortNames[0].text
        if original.get("unit"):
            assert original["unit"] == parsed.defaultUnitOfMeasure.shortNames[0].text
        for value, measurement in zip(original["values"], parsed.measurements):
            assert value["v"] == measurement.data.measure.value
            assert (
                utils.unix_to_utc_rfc3339(value["ts"]) == measurement.recorded.dateTime
            )
            assert measurement.UUID
