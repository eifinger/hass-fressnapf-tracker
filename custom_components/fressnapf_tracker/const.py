"""Constants for fressnapf_tracker."""

from __future__ import annotations

from homeassistant.const import Platform

# Base component constants
NAME = "fressnapf_tracker"
DOMAIN = "fressnapf_tracker"

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.SWITCH,
]

# Configuration and options
CONF_USERNAME = "username"
CONF_PASSWORD = "password"  # nosec
CONF_SERIALNUMBER = "serialnumber"
CONF_DEVICE_TOKEN = "device_token"
CONF_AUTH_TOKEN = "auth_token"
