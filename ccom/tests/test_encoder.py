import os
import json

import pytest

from ccom import encoder, decoder, validator
import utils


TEST_CCOM_JSON_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "test_ccom_measurements.json"
)


@pytest.fixture(scope="session")
def ccom_parsed():
    with open(TEST_CCOM_JSON_FILE) as ccom_json:
        ccom_object = json.load(ccom_json)
    return decoder.ccom(ccom_object)


# Test CCOM message encoding


@pytest.fixture(scope="session")
def ccom_encoded_dict(ccom_parsed):
    return encoder.ccom(ccom_parsed)


@pytest.fixture(scope="session")
def ccom_encoded_json(ccom_encoded_dict):
    return json.dumps(ccom_encoded_dict)


def test_ccom_validate_encoded(ccom_encoded_dict):
    assert validator.validate(ccom_encoded_dict) is None


def test_ccom_base_encoded(ccom_encoded_dict):
    assert isinstance(ccom_encoded_dict["CCOMData"], dict)
    assert isinstance(ccom_encoded_dict["CCOMData"]["@ccomVersion"], str)
    assert isinstance(ccom_encoded_dict["CCOMData"]["entities"], list)


def test_ccom_entities_encoded(ccom_encoded_dict):
    assert len(ccom_encoded_dict["CCOMData"]["entities"]) > 0


def test_ccom_number_of_entities(ccom_parsed, ccom_encoded_dict):
    assert len(ccom_parsed) == len(ccom_encoded_dict["CCOMData"]["entities"])


def test_ccom_type_of_entities(ccom_parsed, ccom_encoded_dict):
    encoded_entities = ccom_encoded_dict["CCOMData"]["entities"]

    for original, encoded in zip(ccom_parsed, encoded_entities):
        assert original.__class__.__name__ == encoded["@@type"]


# Test IoT-Ticket message encoding


@pytest.fixture(scope="session")
def iot_encoded_json(ccom_parsed):
    single_measurements = ccom_parsed
    measurement_location = single_measurements[0].measurementLocation
    measurement_location.measurements = single_measurements
    return json.dumps(encoder.iot_ticket(measurement_location))


@pytest.fixture(scope="session")
def iot_encoded_dict(iot_encoded_json):
    print(json.loads(iot_encoded_json))
    return json.loads(iot_encoded_json)


def test_iot_entities_encoded(iot_encoded_dict):
    assert len(iot_encoded_dict) > 0


def test_iot_number_of_entities(ccom_parsed, iot_encoded_dict):
    assert len(ccom_parsed) == len(iot_encoded_dict)


def test_iot_type_of_entities(ccom_parsed, iot_encoded_dict):
    for original, encoded in zip(ccom_parsed, iot_encoded_dict):
        value = (original.data.measure or original.data.binaryObject).value
        assert value == encoded["v"]
        assert original.recorded.dateTime == utils.unix_to_utc_rfc3339(encoded["ts"])
