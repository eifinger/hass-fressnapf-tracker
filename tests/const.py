"""Constants used for tests."""

from custom_components.fressnapf_tracker.const import (
    CONF_AUTH_TOKEN,
    CONF_DEVICE_TOKEN,
    CONF_SERIALNUMBER,
)

# Mock config data to be used across multiple tests
MOCK_CONFIG: dict[str, str] = {
    CONF_DEVICE_TOKEN: "test_device_token",
    CONF_AUTH_TOKEN: "test_auth_token",
    CONF_SERIALNUMBER: "test_serialnumber",
}

RECONFIGURE_CONFIG: dict[str, str] = {
    CONF_DEVICE_TOKEN: "test_device_token_reconfigure",
    CONF_AUTH_TOKEN: "test_auth_token_reconfigure",
}
