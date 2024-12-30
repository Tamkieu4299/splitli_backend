from datetime import datetime
from typing import Any, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def to_str(value: Any, dateformat: str = "%Y-%m-%dT%H:%M:%S.%fZ") -> str:
    if value is None:
        return None
    elif type(value) == datetime:
        return value.strftime(dateformat)
    else:
        return str(value)


def escape_regex(text: str) -> str:
    special_chars = ".*+^|[]()?$\\"

    return text.translate(str.maketrans({c: f"\\{c}" for c in special_chars}))


def serialize_model(instance):
    """Helper function to serialize SQLAlchemy model instance."""
    serialized_data = {
        column.name: getattr(instance, column.name)
        for column in instance.__table__.columns
    }
    # Add polymorphic identity or other attributes if needed
    if hasattr(instance, "profile_type"):
        serialized_data["profile_type"] = instance.profile_type

    return serialized_data


def combine_data(es_data, sql_data, schema: Type[T]) -> T:
    """Merging data from ES and SQL"""
    sql_parsed_data = schema.from_orm(sql_data)
    sql_dict = sql_parsed_data.dict()
    combined_data = {
        **sql_dict,
        **{k: es_data.get(k, v) for k, v in sql_dict.items()},
    }
    return schema(**combined_data)
