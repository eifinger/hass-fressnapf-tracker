"""Test fressnapf_tracker setup process."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.fressnapf_tracker import (
    async_setup_entry,
    async_unload_entry,
)
from custom_components.fressnapf_tracker.const import DOMAIN

from .const import MOCK_CONFIG


async def test_setup_unload_and_reload_entry(hass, get_response):
    """Test entry setup and unload."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    assert await async_setup_entry(hass, config_entry)

    assert await async_unload_entry(hass, config_entry)
