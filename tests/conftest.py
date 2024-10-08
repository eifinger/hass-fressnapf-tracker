"""Global fixtures for fressnapf_tracker integration."""

import pytest
import json
from httpx import Response
from pytest_homeassistant_custom_component.common import load_fixture

pytest_plugins = "pytest_homeassistant_custom_component"  # pylint: disable=invalid-name


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):  # noqa: F841
    """Enable custom integration loading."""
    yield


@pytest.fixture(autouse=True)
def expected_lingering_timers() -> bool:
    """Temporary ability to bypass test failures.

    Parametrize to True to bypass the pytest failure.
    @pytest.mark.parametrize("expected_lingering_timers", [True])
    This should be removed when all lingering timers have been cleaned up.
    """
    return True


@pytest.fixture(name="get_response")
async def get_response_fixture(respx_mock):
    """Mock the get response."""
    mocked = respx_mock.get(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber?devicetoken=test_device_token"
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("get_response.json")),
        )
    )
    yield mocked


@pytest.fixture(name="get_response_no_led")
async def get_response_no_led_fixture(respx_mock):
    """Mock the get response."""
    mocked = respx_mock.get(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber?devicetoken=test_device_token"
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("get_response_no_led_no_sleep_mode.json")),
        )
    )
    yield mocked


@pytest.fixture(name="get_response_no_deep_sleep")
async def get_response_no_deep_sleep_fixture(respx_mock):
    """Mock the get response."""
    mocked = respx_mock.get(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber?devicetoken=test_device_token"
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("get_response_no_led_no_sleep_mode.json")),
        )
    )
    yield mocked


@pytest.fixture(name="reconfigure_get_response")
async def reconfigure_get_response_fixture(respx_mock):
    """Mock the get response."""
    mocked = respx_mock.get(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber?devicetoken=test_device_token_reconfigure"
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("get_response.json")),
        )
    )
    yield mocked


@pytest.fixture(name="get_response_light_on")
async def get_response_light_on_fixture(respx_mock):
    """Mock the get response."""
    mocked = respx_mock.get(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber?devicetoken=test_device_token"
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("get_response_light_on.json")),
        )
    )
    yield mocked


@pytest.fixture(name="change_deep_sleep")
async def change_deep_sleep_fixture(respx_mock):
    """Mock the put response."""
    mocked = respx_mock.put(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber/change_deep_sleep?devicetoken=test_device_token"
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("put_success_response.json")),
        )
    )
    yield mocked


@pytest.fixture(name="change_led_brightness_100")
async def change_led_brightness_100_fixture(respx_mock):
    """Mock the put response."""
    mocked = respx_mock.put(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber/change_led_brightness?devicetoken=test_device_token",
        json={"value": 100},
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("put_success_response.json")),
        )
    )
    yield mocked


@pytest.fixture(name="change_led_brightness_0")
async def change_led_brightness_0_fixture(respx_mock):
    """Mock the put response."""
    mocked = respx_mock.put(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber/change_led_brightness?devicetoken=test_device_token",
        json={"value": 0},
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("put_success_response.json")),
        )
    )
    yield mocked
