"""Adds config flow for fressnapf_tracker."""

import logging
from typing import TYPE_CHECKING, Any

from .client import (
    InvalidAuthToken,
    InvalidDeviceToken,
    InvalidSerialNumber,
    get_fressnapf_response,
)
import voluptuous as vol
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    CONN_CLASS_CLOUD_POLL,
)
from homeassistant.helpers.httpx_client import get_async_client

from .const import DOMAIN, CONF_SERIALNUMBER, CONF_DEVICE_TOKEN, CONF_AUTH_TOKEN

_LOGGER: logging.Logger = logging.getLogger(__package__)


class FressnapfTrackerFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for fressnapf_tracker."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            for entry in self._async_current_entries():
                if entry.data[CONF_SERIALNUMBER] == user_input[CONF_SERIALNUMBER]:
                    return self.async_abort(reason="already_configured")  # type: ignore[no-any-return]

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

            return self.async_create_entry(  # type: ignore[no-any-return]
                title=user_input[CONF_SERIALNUMBER],
                data=user_input,
            )
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input) -> ConfigFlowResult:
        """Show the configuration form."""
        return self.async_show_form(  # type: ignore[no-any-return]
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

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle reconfiguration."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if TYPE_CHECKING:
            assert entry

        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await get_fressnapf_response(
                    get_async_client(self.hass),
                    entry.data[CONF_SERIALNUMBER],
                    user_input[CONF_DEVICE_TOKEN],
                    user_input[CONF_AUTH_TOKEN],
                )
            except InvalidDeviceToken:
                self._errors["base"] = "invalid_device_token"
            except InvalidAuthToken:
                self._errors["base"] = "invalid_auth_token"
            except InvalidSerialNumber:
                self._errors["base"] = "invalid_serial_number"
            else:
                user_input[CONF_SERIALNUMBER] = entry.data[CONF_SERIALNUMBER]
                return self.async_update_reload_and_abort(  # type: ignore[no-any-return]
                    entry,
                    data=user_input,
                    reason="reconfigure_successful",
                )

        return self.async_show_form(  # type: ignore[no-any-return]
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                vol.Schema(
                    {
                        vol.Required(CONF_DEVICE_TOKEN): str,
                        vol.Required(CONF_AUTH_TOKEN): str,
                    }
                ),
                user_input,
            ),
            errors=errors,
        )
