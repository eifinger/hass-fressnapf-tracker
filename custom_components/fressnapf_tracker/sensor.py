"""Sensor platform for fressnapf_tracker."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .entity import FressnapfTrackerEntity
from . import FressnapfTrackerConfigEntry


SENSOR_ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        name="Battery",
        key="battery",
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FressnapfTrackerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the fressnapf_tracker sensors."""

    coordinator = entry.runtime_data
    sensors: list = []
    for sensor_description in SENSOR_ENTITY_DESCRIPTIONS:
        sensors.append(FressnapfTrackerSensor(coordinator, sensor_description))

    async_add_entities(sensors, True)


class FressnapfTrackerSensor(FressnapfTrackerEntity, SensorEntity):
    """fressnapf_tracker sensor for general information."""

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and bool(self.coordinator.data)

    @property
    def native_value(self) -> StateType | datetime:
        """Return the state of the resources if it has been received yet."""
        if self.entity_description.key in self.coordinator.data:
            return int(self.coordinator.data[self.entity_description.key])
        return None
