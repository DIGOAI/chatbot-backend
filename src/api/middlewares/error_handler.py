import traceback

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.common.logger import Logger
from src.config import Config


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            err_name = e.__class__.__name__
            err_msg = str(e)

            Logger.error(err=e, caller_name="error-handler")

            content = {
                "status": "error",
                "type": err_name,
                "message": err_msg
            }

            if Config.ENVIRONMENT == "development":
                traceback_str = traceback.format_exc() if hasattr(e, "__traceback__") else None
                content["traceback"] = traceback_str  # type: ignore

            return JSONResponse(
                status_code=500,
                content=content
            )
