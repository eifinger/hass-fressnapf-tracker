"""Constants for fressnapf_tracker."""
from __future__ import annotations

from homeassistant.const import Platform

# Base component constants
NAME = "fressnapf_tracker"
DOMAIN = "fressnapf_tracker"
VERSION = "0.1.0"
ISSUE_URL = "https://github.com/eifinger/hass-fressnapf-tracker/issues"

PLATFORMS = [
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
]

# Configuration and options
CONF_USERNAME = "username"
CONF_PASSWORD = "password"  # nosec
CONF_SERIALNUMBER = "serialnumber"
CONF_DEVICE_TOKEN = "device_token"
CONF_AUTH_TOKEN = "auth_token"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
