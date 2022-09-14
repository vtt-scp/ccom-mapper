# Core component types

from dataclasses import dataclass, field

from dataclasses_json import config

from mapper.types.helpers import ExcludeNone


@dataclass
class UTCDateTime(ExcludeNone):
    dateTime: str
    _format: str = field(metadata=config(field_name="@format"))


@dataclass
class TextType(ExcludeNone):
    text: str
