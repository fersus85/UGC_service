from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from db.redis import RedisCache
from main import app
from services.auth_service import AuthService
from utils.token_helpers import get_user_id_from_access_token

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_cacher():
    """Создает мок для объекта Cache."""
    return MagicMock(spec=RedisCache)


@pytest.fixture
def auth_service(mock_cacher):
    """Создает экземпляр AuthService с замоканным cacher."""
    return AuthService(cacher=mock_cacher)


@pytest.fixture(scope="session")
def client():
    async def get_user_id_from_access_token_mocked():
        return "80e6ffa2-8c3e-4d1a-8433-8cca669888a5"

    app.dependency_overrides[get_user_id_from_access_token] = (
        get_user_id_from_access_token_mocked
    )

    test_client = TestClient(app)
    yield test_client

    app.dependency_overrides.pop(get_user_id_from_access_token, None)
