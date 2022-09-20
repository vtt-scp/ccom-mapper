# Helper classes for other Types to inherit

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config


def if_none(x: str, *_) -> bool:
    """Check if given first argument is None"""
    # This function exists because lambda didn't work nicely with mypy in the case below
    return x is None


@dataclass
class ExcludeNone(DataClassJsonMixin):
    # Exclude "None" values from generated JSON and dict objects
    dataclass_json_config = config(exclude=if_none)[  # type: ignore[assignment]
        "dataclasses_json"
    ]


@dataclass
class Typed(ExcludeNone):
    # Add "@@type" key and value for classes inheriting this class
    _type: str = field(init=False, metadata=config(field_name="@@type"))

    def __post_init__(self):
        self._type = self.__class__.__name__
