"""Light platform for fressnapf_tracker."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
    LightEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.httpx_client import get_async_client

from .const import CONF_AUTH_TOKEN, CONF_DEVICE_TOKEN, DOMAIN, CONF_SERIALNUMBER
from .entity import FressnapfTrackerEntity


@dataclass
class FressnapfTrackerLightEntityDescription(LightEntityDescription):
    """Describes fressnapf_tracker light entity."""

    url_path: str | None = None


LIGHT_ENTITY_DESCRIPTIONS: tuple[FressnapfTrackerLightEntityDescription, ...] = (
    FressnapfTrackerLightEntityDescription(
        name="LED",
        key="led_brightness_value",
        url_path="change_led_brightness",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fressnapf_tracker binary_sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list = []
    for description in LIGHT_ENTITY_DESCRIPTIONS:
        entities.append(
            FressnapfTrackerLight(
                coordinator, entry.data.get(CONF_SERIALNUMBER), description
            )
        )

    async_add_entities(entities, True)


class FressnapfTrackerLight(FressnapfTrackerEntity, LightEntity):
    """fressnapf_tracker light."""

    _attr_color_mode: ColorMode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes: set[ColorMode] = {ColorMode.BRIGHTNESS}

    async def _send_request(self, url_path: str, brightness: int) -> None:
        """Send request to change device state."""
        serialnumber = self.coordinator.config_entry.data.get(CONF_SERIALNUMBER)
        device_token = self.coordinator.config_entry.data.get(CONF_DEVICE_TOKEN)
        auth_token = self.coordinator.config_entry.data.get(CONF_AUTH_TOKEN)
        url = f"https://itsmybike.cloud/api/pet_tracker/v2/devices/{serialnumber}/{url_path}?devicetoken={device_token}"
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip",
            "authorization": f"Token token={auth_token}",
            "Connection": "keep-alive",
            "Host": "itsmybike.cloud",
            "User-Agent": "okhttp/4.9.2",
            "Content-Type": "application/json",
        }
        body = {"value": brightness}
        client = get_async_client(self.hass)
        await client.put(url, headers=headers, json=body)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and bool(
            self.coordinator.data.get("led_activatable_overall", False)
        )

    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        if self.entity_description.key in self.coordinator.data:
            return int(
                round((self.coordinator.data[self.entity_description.key] / 100) * 255)
            )
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the device."""
        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        brightness = int((brightness / 255) * 100)
        await self._send_request(self.entity_description.url_path, brightness)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self) -> None:
        """Turn off the device."""
        await self._send_request(self.entity_description.url_path, 0)
        await self.coordinator.async_request_refresh()

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        if self.entity_description.key in self.coordinator.data:
            return bool(self.coordinator.data[self.entity_description.key])
        return False
