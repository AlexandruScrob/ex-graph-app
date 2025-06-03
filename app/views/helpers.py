from datetime import datetime
from typing import Any

from neomodel import StructuredNode


def parse_entity(entity: StructuredNode | list[StructuredNode]) -> dict[str, Any] | list[dict[str, Any] | None] | None:
    if isinstance(entity, list):
        return [_parse_to_str(e) for e in entity]
    return _parse_to_str(entity)


def _parse_to_str(entity: StructuredNode) -> dict[str, Any] | None:
    # NOTE: neomodel OGM uses __properties__, cypher_query uses _properties
    properties: dict[str, Any] | None = getattr(entity, "__properties__", None) or getattr(entity, "_properties", None)

    if properties:
        for key, value in properties.items():
            if isinstance(value, datetime):
                properties[key] = f"{value:%Y-%m-%dT%H:%M:%S}"
        return properties
