"""
Custom integration to integrate fressnapf_tracker with Home Assistant.

For more details about this integration, please refer to
https://github.com/eifinger/hass-fressnapf-tracker
"""
# pyright: reportGeneralTypeIssues=false
import logging
import httpx
from datetime import timedelta
from typing import Any, Dict, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

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
        self.data: Dict[str, Any] = {}

    async def _async_update_data(self) -> Dict[int, Any]:
        """Update data via library."""
        try:
            serialnumber = self.config_entry.data.get(CONF_SERIALNUMBER)
            device_token = self.config_entry.data.get(CONF_DEVICE_TOKEN)
            auth_token = self.config_entry.data.get(CONF_AUTH_TOKEN)
            url = f"https://itsmybike.cloud/api/pet_tracker/v2/devices/{serialnumber}?devicetoken={device_token}"
            headers = {
                "accept": "application/json",
                "accept-encoding": "gzip",
                "authorization": f"Token token={auth_token}",
                "Connection": "keep-alive",
                "Host": "itsmybike.cloud",
                "User-Agent": "okhttp/4.9.2",
                "Content-Type": "application/json",
            }
            async with httpx.AsyncClient() as client:
                result = await client.get(url, headers=headers)
            return result.json()  # type: ignore
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
