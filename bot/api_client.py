import os
import httpx

class ApiClient:
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://api:8000/api/v1")
        self.bot_token = os.getenv("BOT_SECRET", "super_secret_bot_api_token")
        self.headers = {"X-Bot-Token": self.bot_token}

    async def get_user_token(self, telegram_id: int, username: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/auth/telegram",
                json={"telegram_id": telegram_id, "username": username},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()["access_token"]

    async def get_habits(self, user_token: str) -> list:
        headers = {**self.headers, "Authorization": f"Bearer {user_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/habits/", headers=headers)
            response.raise_for_status()
            return response.json()

    async def create_habit(self, user_token: str, title: str) -> dict:
        headers = {**self.headers, "Authorization": f"Bearer {user_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/habits/",
                json={"title": title},
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def log_habit(self, user_token: str, habit_id: int, is_completed: bool) -> dict:
        headers = {**self.headers, "Authorization": f"Bearer {user_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/habits/{habit_id}/log",
                params={"is_completed": str(is_completed).lower()},
                headers=headers
            )
            response.raise_for_status()
            return response.json()

api_client = ApiClient()
