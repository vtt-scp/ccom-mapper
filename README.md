# CCOM-Mapper
Library for validating and converting CCOM messages to other formats, and vice versa.


## Requirements
- Python `^3.10`
- Access to Git repository
- [Poetry](https://python-poetry.org/) for creating development environment

## Quickstart
Install the python library from GitHub repository
```
pip install git+ssh://git@github.com:vtt-scp/ccom-mapper.git
```
Basic decoding and encoding are used as follows:
```python
import json
from ccom import decoder, encoder, validator

# Parse incoming CCOM JSON message to Python dictionary object
ccom_dict = json.loads(ccom_json_message)  

# Validator raises an error if message is not valid CCOM
validator.validate(ccom_dict)  

# Decode dictionary object to CCOM dataclass object
ccom_object = decoder.ccom(ccom_dict)

# ...

# Convert dataclass object back to Python dictionary
ccom_dict = encoder.ccom(ccom_object)

# Serialize object back to outgoing CCOM JSON message
ccom_json_message = json.dumps(ccom_dict)
```
More in-depth example can be found in [example.py](example.py).

## Development
Clone the repository, move to root folder and run:
```
poetry install
```
Run tests with:
```
pytest
```
Search for type errors with:
```
mypy ccom
```

### Decoder/encoder development
Create new decoders to  and encoders to:
- [ccom/decoder.py](ccom/decoder.py)
- [ccom/encoder.py](ccom/encoder.py)

Tests can be added to:
- [ccom/tests/test_decoder.py](ccom/tests/test_decoder.py)
- [ccom/tests/test_encoder.py](ccom/tests/test_encoder.py)

### Expand supported CCOM model
More of the CCOM data model can be supported by building the dataclasses found in:
- [ccom/types/types.py](ccom/types/types.py)
- [ccom/types/core_component.py](ccom/types/core_component.py).

#### Inheritable helpers
Classes from [ccom/types/helpers.py](ccom/types/helpers.py) are inherited in CCOM types for features such as:
- Exclude None values from encoded dicts/JSON.
- Add `@@type` field to specific types (Python variable names cannot start with an `@`). 

### Build Python package
Portable Python package can be built with:
```
poetry build
```
The package can then be found in a newly created `dist/` folder at root.
