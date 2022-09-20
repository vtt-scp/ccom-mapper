# CCOM types

from dataclasses import dataclass

from ccom.types.helpers import ExcludeNone, Typed
from ccom.types.core_component import *


@dataclass(kw_only=True)
class Entity(ExcludeNone):
    UUID: str


@dataclass(kw_only=True)
class Nameable(ExcludeNone):
    shortNames: list[TextType] | None = None


@dataclass
class UnitOfMeasure(Entity, Nameable, Typed):
    pass


@dataclass(kw_only=True)
class Measure(ExcludeNone):
    value: int | float
    unitOfMeasure: UnitOfMeasure | None = None


@dataclass
class BinaryObject:
    value: str


@dataclass(kw_only=True)
class ValueContent(ExcludeNone):
    measure: Measure | None = None
    binaryObject: BinaryObject | None = None


@dataclass
class MeasurementLocation(Entity, Nameable, Typed, ExcludeNone):
    measurements: list["SingleDataMeasurement"] | None = None
    defaultUnitOfMeasure: UnitOfMeasure | None = None


@dataclass
class SingleDataMeasurement(Entity, Nameable, Typed, ExcludeNone):
    recorded: UTCDateTime
    data: ValueContent
    measurementLocation: MeasurementLocation | None = None
