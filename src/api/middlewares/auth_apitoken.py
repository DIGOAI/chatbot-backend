from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader

from src.config import Config


class APITokenAuth:
    async def __call__(self, request: Request, api_key: str = Depends(APIKeyHeader(name='X-API-KEY', auto_error=True))):
        if api_key != Config.X_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

        request.state.user = "SERVICE"
        request.state.role = "SUPPORT"
        return True
