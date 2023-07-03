"""Adds config flow for fressnapf_tracker."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_SERIALNUMBER, CONF_DEVICE_TOKEN, CONF_AUTH_TOKEN

_LOGGER: logging.Logger = logging.getLogger(__package__)


class FressnapfTrackerFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):  # type: ignore
    """Config flow for fressnapf_tracker."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        entries = self._async_current_entries()
        for entry in entries:
            if entry.data[CONF_SERIALNUMBER] == user_input[CONF_SERIALNUMBER]:
                return self.async_abort(reason="already_configured")

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_SERIALNUMBER],
                data=user_input,
            )
        self._errors["base"] = "auth"

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input) -> FlowResult:
        """Show the configuration form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SERIALNUMBER): str,
                    vol.Required(CONF_DEVICE_TOKEN): str,
                    vol.Required(CONF_AUTH_TOKEN): str,
                }
            ),
            errors=self._errors,
        )
