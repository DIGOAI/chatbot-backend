from uuid import UUID

from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import MassiveTemplate as Template
from src.common.services import SMTPService
from src.db.models import MassiveTemplate as TemplateModel
from src.db.repositories import BaseRepository


class EmailUseCases(UseCaseBase):

    def send_email(self, template_id: UUID, emails: list[str]):
        with self._session() as session:
            template_repo = BaseRepository(TemplateModel, Template, session)
            template = template_repo.get(template_id)

        smtp_service = SMTPService()
        subject: str = template.data.get("subject", template.name)
        smtp_service.send_email(receivers=emails, subject=subject, body=template.template)

        return True
