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
    respx_mock.get(
        "https://itsmybike.cloud/api/pet_tracker/v2/devices/test_serialnumber?devicetoken=test_device_token"
    ).mock(
        return_value=Response(
            200,
            json=json.loads(load_fixture("get_response.json")),
        )
    )
