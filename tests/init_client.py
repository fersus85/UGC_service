from fastapi.testclient import TestClient

from main import app
from utils.token_helpers import get_user_id_from_access_token

client = TestClient(app)


async def get_user_id_from_access_token_mocked():
    return "80e6ffa2-8c3e-4d1a-8433-8cca669888a5"


app.dependency_overrides[get_user_id_from_access_token] = (
    get_user_id_from_access_token_mocked
)
