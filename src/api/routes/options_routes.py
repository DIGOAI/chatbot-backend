from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.middlewares import JWTBearer
from src.common.cases import OptionsUseCases
from src.common.models import GenericResponse, Options, OptionsUpdate, create_response

router = APIRouter(prefix="/options", tags=["Options"], dependencies=[Depends(JWTBearer())])


@router.get("/", response_model=GenericResponse[Options])
def get_options():
    options = OptionsUseCases().get_options()

    return create_response(options, message="Options founded.")


@router.put("/{options_id}", response_model=GenericResponse[Options])
def update_options(options_id: UUID, options_data: OptionsUpdate):
    options = OptionsUseCases().update_options(options_id, options_data)

    return create_response(options, message="Options updated.")
