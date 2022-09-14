import os
import json

import jsonschema

CCOM_SCHEMA_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "schema/CCOM.json"
)
CCOM_CORE_TYPE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "schema/CoreComponentType_2p0.json"
)
CCOM_SCHEMA = json.load(open(CCOM_SCHEMA_PATH))
CCOM_CORE_TYPE = json.load(open(CCOM_CORE_TYPE_PATH))

resolver = jsonschema.RefResolver.from_schema(
    CCOM_SCHEMA,
    store={
        CCOM_SCHEMA.get("$id", "CCOM.json"): CCOM_SCHEMA,
        CCOM_CORE_TYPE.get("$id", "CoreComponentType_2p0.json"): CCOM_CORE_TYPE,
    },
)


def validate(ccom_object: dict) -> None:
    """Validate given CCOM object against CCOM schema"""

    jsonschema.validate(ccom_object, CCOM_SCHEMA, resolver=resolver)


if __name__ == "__main__":
    with open("ccom_example.json") as ccom_file:
        ccom_object = json.load(ccom_file)
    validate(ccom_object)
