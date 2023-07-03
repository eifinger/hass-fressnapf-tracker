"""Test fressnapf_tracker setup process."""
from httpx import Response
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.fressnapf_tracker import (
    FressnapfTrackerDataUpdateCoordinator,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.fressnapf_tracker.const import DOMAIN

from .const import MOCK_CONFIG


async def test_setup_unload_and_reload_entry(hass, respx_mock):
    """Test entry setup and unload."""
    respx_mock.get(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber?devicetoken=test_device_token"
    ).mock(
        return_value=Response(
            200,
            json={
                "name": "Test",
                "position": {"lat": 1, "lng": 1, "accuracy": 0},
                "tracker_settings": {"generation": "2.1"},
            },
        )
    )
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    assert await async_setup_entry(hass, config_entry)
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert isinstance(
        hass.data[DOMAIN][config_entry.entry_id], FressnapfTrackerDataUpdateCoordinator
    )

    assert await async_unload_entry(hass, config_entry)
    assert config_entry.entry_id not in hass.data[DOMAIN]
