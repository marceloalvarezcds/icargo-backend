import inspect
from datetime import date, datetime
from typing import List, TypeVar

from app.audits.audit_mixin import AuditMixin

T = TypeVar("T", bound="AuditMixin")

circular_keys = ["ciudades", "localidades"]


def get_name_attributes(obj: T, ignore_keys: List[str]) -> List[str]:
    attributes = []
    all_attributes = inspect.getmembers(obj, lambda a: not (inspect.isroutine(a)))
    for (key, _) in all_attributes:
        if not (
            key == "metadata"
            or key == "registry"
            or key in ignore_keys
            or key in circular_keys
            or key.startswith("_")
            or (key.startswith("__") and key.endswith("__"))
        ):
            attributes.append(key)
    return attributes


def get_dict_instance(obj: T, ignore_keys: List[str], for_json: bool = True):
    d = {}
    for key in get_name_attributes(obj, ignore_keys):
        value = getattr(obj, key)
        d[key] = format_value_by_instance(value, [*ignore_keys, key], for_json)
    return d


def format_value_by_instance(value: T, ignore_keys: List[str], for_json: bool = True):
    if for_json and (isinstance(value, datetime) or isinstance(value, date)):
        return value.isoformat()
    elif isinstance(value, list):
        return [format_value_by_instance(val, ignore_keys, for_json) for val in value]
    elif isinstance(value, AuditMixin):
        return get_dict_instance(value, ignore_keys, for_json)
    else:
        return value


def get_dict(obj: T, ignore_keys: List[str], for_json: bool = True):
    return get_dict_instance(obj, ignore_keys, for_json)
