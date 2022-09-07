import uuid
from datetime import datetime
from typing import List, Tuple, Any, Dict

import pytz


def utc_rfc3339_to_datetime(date: str) -> datetime:
    """Convert UTC RFC 3339 datetime string to Python datetime object"""

    return datetime.fromisoformat(date.replace("Z", "")).replace(tzinfo=pytz.UTC)


def date_string_to_unix(date: str) -> int:
    """Convert UTC datetime string to unix timestamp"""

    date_object = datetime.fromisoformat(date.replace("Z", "")).replace(tzinfo=pytz.UTC)
    # Convert to microseconds
    return int(date_object.timestamp() * 1e6)


def unix_to_date_string(timestamp: int) -> str:
    """Convert UTC unix timestamp to datetime string"""

    date_object = datetime.utcfromtimestamp(timestamp / 1e6)
    # Convert to RFC3339 while removing trailing zeroes
    return (
        date_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        .replace(".000000Z", "Z")
        .replace("000Z", "Z")
    )


def new_uuid() -> str:
    return str(uuid.uuid4())


def exclude_none_values(dct: List[Tuple[str, Any]]) -> Dict[str, Any]:
    """Drop 'None' values from given dict"""
    return {key: value for (key, value) in dct if value is not None}


if __name__ == "__main__":
    # now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    now = utc_rfc3339_to_datetime("2022-06-09T14:38:31.945Z")
    print(now)
    ux = date_string_to_unix("2022-06-09T14:38:31.945Z")
    print(ux)
    now = unix_to_date_string(ux)
    print(now)
    dt = utc_rfc3339_to_datetime(now)
    print(dt)
