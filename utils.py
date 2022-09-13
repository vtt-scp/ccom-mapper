import uuid
from datetime import datetime, timezone
from typing import Any, NoReturn


def utc_rfc3339_to_datetime(date: str) -> datetime:
    """Convert UTC RFC 3339 datetime string to datetime object"""
    return datetime.fromisoformat(date.replace("Z", "")).replace(tzinfo=timezone.utc)


def unix_to_datetime(timestamp: int) -> datetime:
    """Convert UTC unix timestamp (microseconds) to datetime object"""
    return datetime.utcfromtimestamp(timestamp / 1e6)


def utc_rfc3339_to_unix(date: str) -> int:
    """Convert UTC datetime string to unix timestamp in microseconds"""
    date_object = utc_rfc3339_to_datetime(date)
    # Convert to unix timestamp in microseconds
    return int(date_object.timestamp() * 1e6)


def unix_to_utc_rfc3339(timestamp: int) -> str:
    """Convert UTC unix timestamp to datetime string"""
    date_object = unix_to_datetime(timestamp)
    # Convert to RFC3339 while removing trailing zeroes
    return (
        date_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        .replace(".000000Z", "Z")
        .replace("000Z", "Z")
    )


def new_uuid() -> str:
    """Return a new uuid4 as string"""
    return str(uuid.uuid4())


def exclude_none_values(dct: list[tuple[str, Any]]) -> dict[str, Any]:
    """Drop keys with 'None' value from given dict"""
    return {key: value for (key, value) in dct if value is not None}


def require_attribute(object: Any, attribute_name: str) -> Any:
    """Return attribute or raise AttributeError"""
    attribute = getattr(object, attribute_name)
    if not attribute:
        raise AttributeError(
            f"'{type(object).__name__}' missing required attribute '{attribute_name}'."
        )
    return attribute


if __name__ == "__main__":
    rfc3339_string = "2022-06-09T14:38:31.945Z"
    print("RFC3339:", rfc3339_string)
    datetime_object = utc_rfc3339_to_datetime(rfc3339_string)
    print("Datetime:", datetime_object)
    unix_timestamp = utc_rfc3339_to_unix(rfc3339_string)
    print("Unix:", unix_timestamp)
    rfc3339_string = unix_to_utc_rfc3339(unix_timestamp)
    print("RFC3339:", rfc3339_string)
    datetime_object = utc_rfc3339_to_datetime(rfc3339_string)
    print("Datetime:", datetime_object)
