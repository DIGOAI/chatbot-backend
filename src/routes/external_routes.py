from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile

from src.middlewares import APITokenAuth

router = APIRouter(prefix="/external", tags=["External"])


@router.post("/invoice/check", dependencies=[Depends(APITokenAuth())])
def check_invoice(invoice_img: UploadFile):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/ticket/create", dependencies=[Depends(APITokenAuth())])
def create_ticket(client_id: Annotated[str, Body(...)], department: Annotated[str, Body(...)], subject: Annotated[str, Body(...)], message: Annotated[str, Body(...)]):
    raise HTTPException(status_code=501, detail="Not implemented")
