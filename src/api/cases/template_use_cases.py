from datetime import datetime
from uuid import UUID

from src.common.cases import UseCaseBase
from src.common.models import (
    MassiveTemplate,
    MassiveTemplateInsert,
    MassiveTemplateResume,
    MassiveTemplateType,
)
from src.db.models import MassiveTemplate as MassiveTemplateModel
from src.db.repositories import BaseRepository


class MassiveTemplateUseCases(UseCaseBase):

    def get_templates_by_type(self, type: MassiveTemplateType):
        with self._session() as session:
            template_repo = BaseRepository(MassiveTemplateModel, MassiveTemplateResume, session)

            if type == MassiveTemplateType.EMAIL:
                templates = template_repo.filter(MassiveTemplateModel.type == MassiveTemplateType.EMAIL)
            elif type == MassiveTemplateType.WHATSAPP:
                templates = template_repo.filter(MassiveTemplateModel.type == MassiveTemplateType.WHATSAPP)
            else:
                raise ValueError(f"Invalid template type: {type}")

        return templates

    def get_template_by_id(self, template_id: UUID):
        with self._session() as session:
            template_repo = BaseRepository(MassiveTemplateModel, MassiveTemplate, session)
            template = template_repo.get(template_id)

        return template

    def add_new_template(self, data: MassiveTemplateInsert):
        with self._session() as session:
            template_repo = BaseRepository(MassiveTemplateModel, MassiveTemplate, session)
            template = template_repo.add(data.model_dump())

        return template

    def update_template(self, data: MassiveTemplate):
        with self._session() as session:
            template_repo = BaseRepository(MassiveTemplateModel, MassiveTemplate, session)
            template = template_repo.update(
                data.id,
                name=data.name,
                description=data.description,
                data=data.data,
                template=data.template,
                updated_at=datetime.utcnow()
            )

        return template

    def delete_template(self, template_id: UUID):
        with self._session() as session:
            template_repo = BaseRepository(MassiveTemplateModel, MassiveTemplate, session)
            template = template_repo.delete(template_id)

        return template
