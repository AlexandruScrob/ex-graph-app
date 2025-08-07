import json
from core.logging.redactors import redact_dict_sensitive_info, redact_string_sensitive_info
from core.settings import Settings


def test_redact_sensitive_info_dict(settings: Settings):
    to_redact = {
        "customerIdentifier": "SHOULD_BE_REDACTED",
        "anotherSecretCase": "SHOULD_BE_REDACTED",
        "sensitiveInfo": "SHOULD_BE_REDACTED",
        "notSecret": "should_NOT_be_redacted",
        "nested_test": [
            {
                "sensitiveInfo": "SHOULD_BE_REDACTED",
            }
        ],
    }
    redacted = redact_dict_sensitive_info(to_redact, {"customeridentifier", "Anothersecretcase", "sensitiveInfo"})

    assert redacted == {
        "customerIdentifier": settings.redacted_value,
        "anotherSecretCase": settings.redacted_value,
        "sensitiveInfo": settings.redacted_value,
        "notSecret": "should_NOT_be_redacted",
        "nested_test": [{"sensitiveInfo": settings.redacted_value}],
    }


def test_redact_sensitive_info_str(settings: Settings):
    to_redact = (
        "http://test.org/path?api_secret=SHOULD_BE_REDACTED&api_secret=SHOULD_ALSO_BE_REDACTED&"
        "random=should_NOT_be_redacted&another_one=should_NOT_be_redacted"
    )
    redacted = redact_string_sensitive_info(to_redact, {"api_secret"})

    assert redacted == (
        f"http://test.org/path?api_secret={settings.redacted_value}&api_secret={settings.redacted_value}"
        "&random=should_NOT_be_redacted&another_one=should_NOT_be_redacted"
    )

    to_redact = '{"api_secret":"SHOULD_BE_REDACTED", "notSecret": "should_NOT_be_redacted"}'
    redacted = redact_string_sensitive_info(to_redact, {"api_secret"})
    assert redacted == json.dumps(
        {"api_secret": settings.redacted_value, "notSecret": "should_NOT_be_redacted"},
        indent=2,
    )
