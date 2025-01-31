from unittest.mock import patch

import pytest

pytestmark = pytest.mark.asyncio


@patch("services.auth_service.verify_token")
@patch("services.auth_service.calc_diff")
async def test_verify_token_success(
    mock_calc_diff, mock_verify_token, auth_service, mock_cacher
):
    """Тестирует успешную проверку токена."""
    token = "valid_token"
    mock_cacher.get.return_value = None
    mock_verify_token.return_value = None
    mock_calc_diff.return_value = 10

    await auth_service.verify(token)

    mock_cacher.get.assert_called_once_with("def verify: valid_token")
    mock_verify_token.assert_called_once_with(token)
    mock_cacher.set.assert_called_once_with(
        "def verify: valid_token", True, expire=10
    )
