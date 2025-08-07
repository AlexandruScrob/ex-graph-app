import json
from typing import Any, Iterable
from urllib.parse import ParseResult, parse_qsl, urlparse

from core.settings import get_settings


def redact_sensitive_info(
    object_with_sensitive_info: Any,
    keys_to_redact: Iterable[str],
    redacted_value: str | None = None,
) -> Any:
    """
    Redacts sensitive info from any object. Configurable by specifying which values of which keys to
    redact as well as what value to use when redacting.
    """
    redacted_value = redacted_value or get_settings().redacted_value

    redactors = {
        list: redact_list_sensitive_info,
        dict: redact_dict_sensitive_info,
        str: redact_string_sensitive_info,
    }

    for kls in type(object_with_sensitive_info).__mro__:
        if redactor := redactors.get(kls):
            object_with_sensitive_info = redactor(
                object_with_sensitive_info,
                keys_to_redact,
                redacted_value=redacted_value,
            )
    return object_with_sensitive_info


def redact_list_sensitive_info(
    list_data: dict, keys_to_redact: Iterable[str], redacted_value: str | None = None
) -> list:
    redacted_value = redacted_value or get_settings().redacted_value
    redacted_data = []

    for obj in list_data:
        redacted_data.append(redact_sensitive_info(obj, keys_to_redact, redacted_value=redacted_value))
    return redacted_data


def redact_dict_sensitive_info(
    dict_data: dict, keys_to_redact: Iterable[str], redacted_value: str | None = None
) -> dict:
    redacted_value = redacted_value or get_settings().redacted_value
    redacted_dict = {}

    for key, value in dict_data.items():
        if isinstance(key, str) and key.lower() in map(str.lower, keys_to_redact):
            redacted_dict[key] = redacted_value
        else:
            redacted_dict[key] = redact_sensitive_info(value, keys_to_redact, redacted_value=redacted_value)
    return redacted_dict


def redact_string_sensitive_info(
    string_data: str, keys_to_redact: Iterable[str], redacted_value: str | None = None
) -> str:
    """Redact sensitive info from string. Checking if string is url and has query part and if string is json otherwise
    leave it unchanged.
    """
    redacted_value = redacted_value or get_settings().redacted_value

    # Check if it is json
    try:
        json_data = json.loads(string_data)
        redacted_json_data = redact_sensitive_info(json_data, keys_to_redact, redacted_value=redacted_value)
        return json.dumps(redacted_json_data, indent=2)
    except json.decoder.JSONDecodeError:
        pass

    # Check if it contains query string
    parsed_url = urlparse(string_data)
    if parsed_url.query:
        redacted_query = redact_query_string_sensitive_info(
            parsed_url.query, keys_to_redact, redacted_value=redacted_value
        )
        string_data = ParseResult(**{**parsed_url._asdict(), "query": redacted_query}).geturl()

    return string_data


def redact_query_string_sensitive_info(
    query_string: str, keys_to_redact: Iterable[str], redacted_value: str | None = None
) -> str:
    """Redacts sensitive info from a URL encoded string in the format 'key1=value1&key2=value2'."""
    redacted_value = redacted_value or get_settings().redacted_value
    query_strings = parse_qsl(query_string)
    if not query_strings:
        return query_string

    redacted_query_strings = []
    for tup in query_strings:
        if tup[0].lower() in map(str.lower, keys_to_redact):
            redacted_query_strings.append((tup[0], redacted_value))
        else:
            redacted_query_strings.append(tup)

    object_with_sensitive_info = "&".join(f"{qs[0]}={qs[1]}" for qs in redacted_query_strings)
    return object_with_sensitive_info
