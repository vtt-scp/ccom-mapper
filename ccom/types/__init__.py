import inspect

from ccom.types import types
from ccom.types.types import *

CCOM_VERSION = "4.1.0-draft"

# Provide a dict of supported CCOM classes (types) in a constant
CCOM_TYPES = {
    member[0]: member[1]
    for member in inspect.getmembers(types, inspect.isclass)
    if member[1].__module__ == types.__name__
}
