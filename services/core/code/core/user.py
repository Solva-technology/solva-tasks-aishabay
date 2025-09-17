from http import HTTPStatus

import httpx
from fastapi import Depends, Header, HTTPException

from services.core.code.core.config import settings


AUTH_URL = settings.AUTH_SERVICE_URL + "/user/me"


async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="No Bearer token",
        )

    token = authorization.split()[1]

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                AUTH_URL,
                headers={"Authorization": f"Bearer {token}"},
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail="Auth service unavailable",
            )

    if resp.status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token",
        )
    return resp.json()


def role_required(roles: list[str]):
    async def wrapper(user=Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return wrapper
