"""Tests for the config flow."""

import pytest
from homeassistant.core import HomeAssistant
from homeassistant import config_entries
from custom_components.fressnapf_tracker.const import DOMAIN
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.fressnapf_tracker.const import (
    CONF_AUTH_TOKEN,
    CONF_DEVICE_TOKEN,
    CONF_SERIALNUMBER,
)

from .const import MOCK_CONFIG, RECONFIGURE_CONFIG


@pytest.mark.usefixtures("get_response")
async def test_step_user(hass: HomeAssistant) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    create_result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        MOCK_CONFIG,
    )
    assert create_result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()

    entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert entry.title == "test_serialnumber"
    assert entry.data == {
        CONF_AUTH_TOKEN: "test_auth_token",
        CONF_DEVICE_TOKEN: "test_device_token",
        CONF_SERIALNUMBER: "test_serialnumber",
    }


@pytest.mark.usefixtures("get_response_no_led")
async def test_step_user_no_led(hass: HomeAssistant) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    create_result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        MOCK_CONFIG,
    )
    assert create_result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()

    entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert entry.title == "test_serialnumber"
    assert entry.data == {
        CONF_AUTH_TOKEN: "test_auth_token",
        CONF_DEVICE_TOKEN: "test_device_token",
        CONF_SERIALNUMBER: "test_serialnumber",
    }


@pytest.mark.usefixtures("reconfigure_get_response")
async def test_reconfigure(hass: HomeAssistant) -> None:
    """Test reconfigure flow."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    reconfigure_result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": config_entry.entry_id,
        },
    )
    assert reconfigure_result["type"] is FlowResultType.FORM
    assert reconfigure_result["step_id"] == "reconfigure"

    reconfigure_successful_result = await hass.config_entries.flow.async_configure(
        reconfigure_result["flow_id"],
        RECONFIGURE_CONFIG,
    )
    assert reconfigure_successful_result["type"] is FlowResultType.ABORT
    assert reconfigure_successful_result["reason"] == "reconfigure_successful"
    await hass.async_block_till_done()

    entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert entry.data == {
        CONF_AUTH_TOKEN: "test_auth_token_reconfigure",
        CONF_DEVICE_TOKEN: "test_device_token_reconfigure",
        CONF_SERIALNUMBER: "test_serialnumber",
    }
