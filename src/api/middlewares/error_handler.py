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
            error_title = f"Error {id(e)} | {e.__class__.__name__}: {str(e)}"
            traceback_str = traceback.format_exc() if hasattr(e, "__traceback__") else None

            Logger.error(f"{error_title}", "error-handler", traceback_str)

            if Config.ENVIRONMENT == "development":
                return JSONResponse(
                    status_code=500,
                    content={
                        "status": "error",
                        "type": e.__class__.__name__,
                        "message": str(e),
                        "traceback": traceback.format_exc() if hasattr(e, "__traceback__") else None
                    }
                )
            else:
                return JSONResponse(
                    status_code=500,
                    content={
                        "status": "error",
                        "type": e.__class__.__name__,
                        "message": str(e)
                    }
                )
