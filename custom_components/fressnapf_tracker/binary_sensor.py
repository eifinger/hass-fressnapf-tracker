"""Binary Sensor platform for fressnapf_tracker."""

from __future__ import annotations

from . import FressnapfTrackerConfigEntry
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import FressnapfTrackerEntity


BINARY_SENSOR_ENTITY_DESCRIPTIONS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        name="Charging",
        key="charging",
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    BinarySensorEntityDescription(
        name="Deep Sleep",
        key="deep_sleep_value",
        device_class=BinarySensorDeviceClass.POWER,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FressnapfTrackerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fressnapf_tracker binary_sensors."""

    coordinator = entry.runtime_data
    binary_sensors: list = []
    for sensor_description in BINARY_SENSOR_ENTITY_DESCRIPTIONS:
        binary_sensors.append(FressnapfTrackerBinarySensor(coordinator, sensor_description))

    async_add_entities(binary_sensors, True)


class FressnapfTrackerBinarySensor(FressnapfTrackerEntity, BinarySensorEntity):
    """fressnapf_tracker binary_sensor for general information."""

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and bool(self.coordinator.data)

    @property
    def is_on(self) -> bool:
        """Return True if the binary sensor is on."""
        if self.entity_description.key in self.coordinator.data:
            return bool(self.coordinator.data[self.entity_description.key])
        return False
