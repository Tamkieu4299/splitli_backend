import aiohttp
import json
from sqlalchemy.orm import Session
from schemas.auth_schema import LoginSchema
from secret import UserRoleEnum
from routers.auth import login_for_access_token


class ExternalCall:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    async def get(self, path: str, params: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.endpoint}/{path}", params=params, headers=headers
            ) as response:
                return await response.json()

    async def post(self, path: str, data: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.endpoint}/{path}", json=data, headers=headers
            ) as response:
                return await response.json()

    async def put(self, path: str, data: dict = None, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.endpoint}/{path}", json=data, headers=headers
            ) as response:
                return await response.json()

    async def delete(self, path: str, headers: dict = None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.endpoint}/{path}", headers=headers
            ) as response:
                return await response.json()

    def authenticate_internal_user(
        self, username: str, password: str, db: Session
    ):
        form_data = LoginSchema(
            email=username,
            password=password,
            login_type=UserRoleEnum.INTERNAL.value,
        )

        try:
            response = login_for_access_token(form_data=form_data, db=db)
            jsonres = json.loads(response.__dict__.get("body"))
            token = jsonres.get("data", {}).get("token")
            return f"Bearer {token}"
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            raise
