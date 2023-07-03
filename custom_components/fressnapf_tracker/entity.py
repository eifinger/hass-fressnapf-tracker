"""fressnapf_tracker class."""
# pyright: reportGeneralTypeIssues=false
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN


class FressnapfTrackerBaseEntity(CoordinatorEntity):
    """Abstract base entity for fressnapf_tracker."""

    def __init__(self, coordinator: DataUpdateCoordinator, tracker_id: int):
        super().__init__(coordinator)
        self.id = tracker_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.id)},
            name=str(self.coordinator.data["name"]),
            model=str(self.coordinator.data["tracker_settings"]["generation"]),
            manufacturer="Fressnapf",
        )


class FressnapfTrackerEntity(FressnapfTrackerBaseEntity):
    """Entity for fressnapf_tracker."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        tracker_id: int,
        entity_description: EntityDescription,
    ) -> None:
        super().__init__(coordinator, tracker_id)
        self.entity_description = entity_description
        self._attr_name = (
            f"{self.coordinator.data['name']} {self.entity_description.name}"
        )
        self._attr_unique_id = f"{self.id}_{self.entity_description.key}"
