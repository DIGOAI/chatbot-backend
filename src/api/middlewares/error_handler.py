from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.common.logger import Logger


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            Logger.error(f"Error {e.__class__.__name__}: {str(e)}", "error-handler")

            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "type": e.__class__.__name__,
                    "message": str(e),
                    "traceback": e.__traceback__ if hasattr(e, "__traceback__") else None
                }
            )
