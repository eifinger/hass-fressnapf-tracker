"""Custom integration to integrate fressnapf_tracker with Home Assistant.

For more details about this integration, please refer to
https://github.com/eifinger/hass-fressnapf-tracker
"""

from dataclasses import dataclass
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
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

DEFAULT_UPDATE_RATE = 30


@dataclass
class FressnapfTrackerDataUpdateCoordinatorConfig:
    """Config data for FressnapfTrackerDataUpdateCoordinator."""

    serial_number: int
    device_token: str
    auth_token: str


class FressnapfTrackerDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, config: FressnapfTrackerDataUpdateCoordinatorConfig) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_RATE),
        )
        self.config = config

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            httpx_client = get_async_client(self.hass)
            return await get_fressnapf_response(
                httpx_client, self.config.serial_number, self.config.device_token, self.config.auth_token
            )
        except Exception as exception:
            _LOGGER.debug(
                "Failed to update fressnapf_tracker data: %s",
                exception,
                exc_info=True,
                stack_info=True,
            )
            raise UpdateFailed(exception) from exception


type FressnapfTrackerConfigEntry = ConfigEntry[FressnapfTrackerDataUpdateCoordinator]  # type: ignore[valid-type]


async def async_setup_entry(hass: HomeAssistant, entry: FressnapfTrackerConfigEntry):
    """Set up this integration using UI."""

    config = FressnapfTrackerDataUpdateCoordinatorConfig(
        entry.data[CONF_SERIALNUMBER], entry.data[CONF_DEVICE_TOKEN], entry.data[CONF_AUTH_TOKEN]
    )

    coordinator = FressnapfTrackerDataUpdateCoordinator(hass, config)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
