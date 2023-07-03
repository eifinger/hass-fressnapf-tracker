"""Device tracker platform for fressnapf_tracker."""
from typing import List

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_SERIALNUMBER,
)
from .entity import FressnapfTrackerBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fressnapf_tracker device_trackers."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            FressnapfTrackerDeviceTracker(
                coordinator,
                entry.data.get(CONF_SERIALNUMBER),
            )
        ],
        True,
    )


class FressnapfTrackerDeviceTracker(FressnapfTrackerBaseEntity, TrackerEntity):
    """fressnapf_tracker device tracker."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        tracker_id: int,
    ):
        super().__init__(coordinator, tracker_id)
        self._attr_icon = "mdi:paw"
        self._attr_unique_id = tracker_id
        self._attr_name = self.coordinator.data["name"]

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and bool(self.coordinator.data["position"])

    @property
    def latitude(self):
        """Return latitude value of the device."""
        if "position" in self.coordinator.data:
            return float(self.coordinator.data["position"]["lat"])

    @property
    def longitude(self):
        """Return longitude value of the device."""
        if "position" in self.coordinator.data:
            return float(self.coordinator.data["position"]["lng"])

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS

    @property
    def location_accuracy(self):
        """Return the location accuracy of the device.

        Value in meters.
        """
        if "position" in self.coordinator.data:
            return int(self.coordinator.data["position"]["accuracy"])
