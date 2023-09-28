from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.logger import Logger


class LoggerHandler(BaseHTTPMiddleware):
    """Middleware to log requests from clients"""

    NAME = "endpoint"

    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        response = await call_next(request)

        # Get client metadata
        client_addr = request.client.host if request.client else "-"
        method = request.method
        url = request.url.path

        # Get status code
        status_code = response.status_code

        # Get content length
        content_length = int(response.headers.get("content-length", "0"))

        # Get content length magnitude
        content_length_mag = "B"
        if content_length > 1000:
            content_length /= 1000
            content_length_mag = "KB"
        elif content_length > 1000000:
            content_length /= 1000000
            content_length_mag = "MB"

        # Create log line in format: 127.0.0.1 - GET /api/v1/path/to/ 200 - 1.5 KB
        line = f"{client_addr} - {method} {url} {status_code} - {content_length} {content_length_mag}"

        # Log line
        if status_code >= 500:
            Logger.error(line, caller_name=self.NAME)
        elif status_code >= 400:
            Logger.warn(line, caller_name=self.NAME)
        else:
            Logger.info(line, caller_name=self.NAME)

        return response
