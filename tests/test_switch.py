"""Tests for the fressnapf_tracker switch."""

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
)
from .const import MOCK_CONFIG
from custom_components.fressnapf_tracker.const import DOMAIN


async def test_switch_deep_sleep(hass, get_response, change_deep_sleep):
    """Test that switch works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    await hass.services.async_call(
        "switch",
        "turn_on",
        {"entity_id": "switch.test_deep_sleep"},
        blocking=True,
    )
    await hass.async_block_till_done()
    assert change_deep_sleep.called
