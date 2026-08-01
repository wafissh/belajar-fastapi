import pytest
from httpx import AsyncClient

from test.conftest import auth_header, create_test_user, login_user

@pytest.mark.anyio
async def test_get_post_empty(client: AsyncClient):
    response = await client.get("/api/posts")
    assert response.status_code == 200
    data = response.json()
    assert data["posts"] == []
    assert data["total"] == 0
    assert data["has_more"] == False

