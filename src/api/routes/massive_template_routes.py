from uuid import UUID

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/templates", tags=["Massive templates"])


@router.get("/")
def get_email_templates(limit: int = 30, offset: int = 0):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/")
def create_email_template():
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{template_id}")
def get_email_template(template_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{template_id}")
def update_email_template(template_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{template_id}")
def delete_email_template(template_id: UUID):
    raise HTTPException(status_code=501, detail="Not implemented")
