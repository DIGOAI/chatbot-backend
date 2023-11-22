from uuid import UUID

from fastapi import APIRouter, status

from src.common.cases import MassiveTemplateUseCases
from src.common.models import (
    GenericResponse,
    MassiveTemplate,
    MassiveTemplateInsert,
    MassiveTemplateType,
    create_response,
)

router = APIRouter(prefix="/templates", tags=["Massive templates"])


@router.get("/", response_model=GenericResponse[list[MassiveTemplate]])
def get_templates(type: MassiveTemplateType):
    templates = MassiveTemplateUseCases().get_templates_by_type(type)
    return create_response(templates, "Templates retrieved")


@router.post("/", response_model=GenericResponse[MassiveTemplate], status_code=status.HTTP_201_CREATED)
def create_template(template_data: MassiveTemplateInsert):
    template = MassiveTemplateUseCases().add_new_template(template_data)
    return create_response(template, "Template created", status.HTTP_201_CREATED)


@router.get("/{template_id}", response_model=GenericResponse[MassiveTemplate])
def get_template(template_id: UUID):
    template = MassiveTemplateUseCases().get_template_by_id(template_id)
    return create_response(template, "Template retrieved")


@router.put("/", response_model=GenericResponse[MassiveTemplate])
def update_template(template: MassiveTemplate):
    template_updated = MassiveTemplateUseCases().update_template(template)
    return create_response(template_updated, "Template updated")


@router.delete("/{template_id}", response_model=GenericResponse[MassiveTemplate])
def delete_template(template_id: UUID):
    template_deleted = MassiveTemplateUseCases().delete_template(template_id)
    return create_response(template_deleted, "Template deleted")
