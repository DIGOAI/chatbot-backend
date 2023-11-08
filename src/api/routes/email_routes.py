from fastapi import APIRouter

router = APIRouter(prefix="/emails", tags=["Emails"])


@router.post("/")
def send_email_to_certain_users():
    return {}


@router.post("/massive")
def send_email_to_all_users():
    return "Massive"


@router.get("/templates")
def get_email_templates(limit: int = 30, offset: int = 0):
    return []


@router.get("/templates/{template_id}")
def get_email_template(template_id: int):
    return ""


@router.put("/templates/{template_id}")
def update_email_template(template_id: int):
    return ""


@router.post("/templates/{template_id}")
def create_email_template(template_id: int):
    return []


@router.delete("/templates/{template_id}")
def delete_email_template(template_id: int):
    return {}
