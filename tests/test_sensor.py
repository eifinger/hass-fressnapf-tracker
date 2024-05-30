"""Tests for the fressnapf_tracker sensor."""

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
)
from .const import MOCK_CONFIG
from custom_components.fressnapf_tracker.const import DOMAIN


async def test_sensor_battery(hass, get_response):
    """Test that sensor works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    sensor = hass.states.get("sensor.test_battery")
    assert sensor.state == "81"
