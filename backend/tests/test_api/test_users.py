import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_update_user_full_name(async_client: AsyncClient, registered_user, auth_header):
    response = await async_client.put(
        f"/users/{registered_user['id']}",
        headers=auth_header,
        json={"full_name": "Updated Tester"}
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Tester"

@pytest.mark.asyncio
async def test_update_user_not_found(async_client: AsyncClient, auth_header):
    invalid_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.put(
        f"/users/{invalid_id}",
        headers=auth_header,
        json={"full_name": "Nobody"}
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient, registered_user, auth_header):
    response = await async_client.delete(
        f"/users/{registered_user['id']}",
        headers=auth_header
    )

    assert response.status_code == 200

    # Verify user is deleted
    get_response = await async_client.get(
        f"/users/{registered_user['id']}",
        headers=auth_header
    )
    assert get_response.status_code == 404