"""Device tracker platform for fressnapf_tracker."""

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import FressnapfTrackerBaseEntity
from . import FressnapfTrackerConfigEntry, FressnapfTrackerDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FressnapfTrackerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fressnapf_tracker device_trackers."""
    coordinator = entry.runtime_data

    async_add_entities(
        [
            FressnapfTrackerDeviceTracker(
                coordinator,
            )
        ],
        True,
    )


class FressnapfTrackerDeviceTracker(FressnapfTrackerBaseEntity, TrackerEntity):
    """fressnapf_tracker device tracker."""

    def __init__(
        self,
        coordinator: FressnapfTrackerDataUpdateCoordinator,
    ):
        super().__init__(coordinator)
        self._attr_icon = "mdi:paw"
        self._attr_unique_id = str(coordinator.config.serial_number)
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
        return SourceType.GPS

    @property
    def location_accuracy(self):
        """Return the location accuracy of the device.

        Value in meters.
        """
        if "position" in self.coordinator.data:
            return int(self.coordinator.data["position"]["accuracy"])
