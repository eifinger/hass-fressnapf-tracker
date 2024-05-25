"""Custom integration to integrate fressnapf_tracker with Home Assistant.

For more details about this integration, please refer to
https://github.com/eifinger/hass-fressnapf-tracker
"""
# pyright: reportGeneralTypeIssues=false
import logging
from datetime import timedelta
from typing import Any

from .client import get_fressnapf_response
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.httpx_client import get_async_client
from .const import (
    CONF_SERIALNUMBER,
    CONF_DEVICE_TOKEN,
    CONF_AUTH_TOKEN,
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

DEFAULT_UPDATE_RATE = 30


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    coordinator = FressnapfTrackerDataUpdateCoordinator(hass, config_entry=entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


class FressnapfTrackerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_RATE),
        )
        self.config_entry = config_entry
        self.data: dict[str, Any] = {}

    async def _async_update_data(self) -> dict[int, Any]:
        """Update data via library."""
        try:
            serial_number = self.config_entry.data.get(CONF_SERIALNUMBER)
            device_token = self.config_entry.data.get(CONF_DEVICE_TOKEN)
            auth_token = self.config_entry.data.get(CONF_AUTH_TOKEN)
            httpx_client = get_async_client(self.hass)
            return await get_fressnapf_response(  # type: ignore
                httpx_client, serial_number, device_token, auth_token
            )
        except Exception as exception:
            _LOGGER.debug(
                "Failed to update fressnapf_tracker data: %s",
                exception,
                exc_info=True,
                stack_info=True,
            )
            raise UpdateFailed(exception) from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
