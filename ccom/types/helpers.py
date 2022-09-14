from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config

# Helper classes for other Types to inherit


@dataclass
class ExcludeNone(DataClassJsonMixin):
    # Exclude "None" values from generated JSON and dict objects
    dataclass_json_config = config(exclude=lambda x: x is None)["dataclasses_json"]


@dataclass
class Typed(ExcludeNone):
    # Add "@@type" key and value for classes inheriting this class
    _type: str = field(init=False, metadata=config(field_name="@@type"))

    def __post_init__(self):
        self._type = self.__class__.__name__
