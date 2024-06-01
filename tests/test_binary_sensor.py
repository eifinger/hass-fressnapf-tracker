"""Tests for the fressnapf_tracker binary_sensor."""

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
)
from .const import MOCK_CONFIG
from custom_components.fressnapf_tracker.const import DOMAIN


async def test_binary_sensor_charging(hass, get_response):
    """Test that binary_sensor works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    battery_sensor = hass.states.get("binary_sensor.test_charging")
    assert battery_sensor.state == "on"


async def test_binary_sensor_deep_sleep(hass, get_response):
    """Test that binary_sensor works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    battery_sensor = hass.states.get("binary_sensor.test_deep_sleep")
    assert battery_sensor.state == "off"
