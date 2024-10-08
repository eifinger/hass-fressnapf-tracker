"""Switch platform for fressnapf_tracker."""

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.httpx_client import get_async_client

from .const import CONF_AUTH_TOKEN, CONF_DEVICE_TOKEN, CONF_SERIALNUMBER
from .entity import FressnapfTrackerEntity
from . import FressnapfTrackerConfigEntry


@dataclass(frozen=True)
class FressnapfTrackerSwitchEntityDescription(SwitchEntityDescription):
    """Describes fressnapf_tracker switch entity."""

    url_path: str | None = None


SWITCH_ENTITY_DESCRIPTIONS: tuple[FressnapfTrackerSwitchEntityDescription, ...] = (
    FressnapfTrackerSwitchEntityDescription(
        name="Deep Sleep",
        key="deep_sleep_value",
        device_class=SwitchDeviceClass.SWITCH,
        url_path="change_deep_sleep",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FressnapfTrackerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fressnapf_tracker switches."""

    coordinator = entry.runtime_data
    if coordinator.data["tracker_settings"]["features"]["sleep_mode"]:
        entities: list = []
        for description in SWITCH_ENTITY_DESCRIPTIONS:
            entities.append(FressnapfTrackerSwitch(coordinator, description))

        async_add_entities(entities, True)


class FressnapfTrackerSwitch(FressnapfTrackerEntity, SwitchEntity):
    """fressnapf_tracker binary_sensor for general information."""

    entity_description: FressnapfTrackerSwitchEntityDescription

    async def _send_request(self, url_path: str, on: bool) -> None:
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
        body = {"value": int(on)}
        client = get_async_client(self.hass)
        await client.put(url, headers=headers, json=body)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and bool(self.coordinator.data)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the device."""
        if TYPE_CHECKING:
            assert self.entity_description.url_path
        await self._send_request(self.entity_description.url_path, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the device."""
        if TYPE_CHECKING:
            assert self.entity_description.url_path
        await self._send_request(self.entity_description.url_path, False)
        await self.coordinator.async_request_refresh()

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        if self.entity_description.key in self.coordinator.data:
            return bool(self.coordinator.data[self.entity_description.key])
        return False
