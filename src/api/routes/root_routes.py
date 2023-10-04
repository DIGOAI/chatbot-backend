from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="DIGO | Chatbot-API",
        swagger_favicon_url="/static/favicon.png"
    )


@router.get("/", tags=["Default"], include_in_schema=True)
def index():
    return RedirectResponse(url="/api/v1")


@router.get("/api/v1", tags=["Default"], include_in_schema=True)
def index_v1():
    return {
        "message": "Welcome to the DIGO Chatbot-API",
        "documentation": "/docs"
    }
