import httpx

from services.core.code.core.config import settings


class AuthClient:
    def __init__(self, base_url: str = settings.AUTH_SERVICE_URL):
        self.base_url = base_url

    async def is_manager(self, user_id: int) -> bool:
        url = f"{self.base_url}/user/{user_id}/is_manager"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data.get("is_manager", False)

    async def are_students(self, user_ids: list[int]) -> bool:
        url = f"{self.base_url}/user/are_students"
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=[*user_ids])
        resp.raise_for_status()
        data = resp.json()
        return data.get("are_students", False)


auth_client = AuthClient()
