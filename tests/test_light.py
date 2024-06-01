"""Tests for the fressnapf_tracker light."""

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
)
from .const import MOCK_CONFIG
from custom_components.fressnapf_tracker.const import DOMAIN


async def test_light_led_on(hass, get_response, change_led_brightness_100):
    """Test that led works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    assert hass.states.get("light.test_led").state == "off"

    await hass.services.async_call(
        "light",
        "turn_on",
        {"entity_id": "light.test_led"},
        blocking=True,
    )
    await hass.async_block_till_done()
    assert change_led_brightness_100.called


async def test_light_led_off(hass, get_response_light_on, change_led_brightness_0):
    """Test that led works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    assert hass.states.get("light.test_led").state == "on"

    await hass.services.async_call(
        "light",
        "turn_off",
        {"entity_id": "light.test_led"},
        blocking=True,
    )
    await hass.async_block_till_done()
    assert change_led_brightness_0.called


async def test_light_led_brightness(hass, get_response_light_on):
    """Test that led works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    assert hass.states.get("light.test_led").state == "on"
    assert hass.states.get("light.test_led").attributes["brightness"] == 255
