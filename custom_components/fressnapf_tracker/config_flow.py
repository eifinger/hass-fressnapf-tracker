"""Adds config flow for fressnapf_tracker."""

import logging

from .client import (
    InvalidAuthToken,
    InvalidDeviceToken,
    InvalidSerialNumber,
    get_fressnapf_response,
)
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.httpx_client import get_async_client

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

        if user_input is not None:
            for entry in self._async_current_entries():
                if entry.data[CONF_SERIALNUMBER] == user_input[CONF_SERIALNUMBER]:
                    return self.async_abort(reason="already_configured")

            try:
                await get_fressnapf_response(
                    get_async_client(self.hass),
                    user_input[CONF_SERIALNUMBER],
                    user_input[CONF_DEVICE_TOKEN],
                    user_input[CONF_AUTH_TOKEN],
                )
            except InvalidDeviceToken:
                self._errors["base"] = "invalid_device_token"
                return await self._show_config_form(user_input)
            except InvalidAuthToken:
                self._errors["base"] = "invalid_auth_token"
                return await self._show_config_form(user_input)
            except InvalidSerialNumber:
                self._errors["base"] = "invalid_serial_number"
                return await self._show_config_form(user_input)

            return self.async_create_entry(
                title=user_input[CONF_SERIALNUMBER],
                data=user_input,
            )
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input) -> FlowResult:
        """Show the configuration form."""
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(
                    {
                        vol.Required(CONF_SERIALNUMBER): str,
                        vol.Required(CONF_DEVICE_TOKEN): str,
                        vol.Required(CONF_AUTH_TOKEN): str,
                    }
                ),
                user_input,
            ),
            errors=self._errors,
        )
