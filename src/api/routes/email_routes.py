from uuid import UUID

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/send")
def send_massive_email(template_id: UUID, emails: list[str]):
    raise HTTPException(status_code=501, detail="Not implemented")
