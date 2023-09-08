from datetime import datetime, timezone

from src.decisions_tree import DecisionsTree
from src.logger import Logger
from src.models import ContextType
from src.utils import get_phone_and_service

tree = DecisionsTree[ContextType]()


@tree.add_action('0.0', condition=lambda _: True, end=False)
def load_context(context: ContextType) -> None:
    Logger.info("Loading context")

    # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
    client_phone, _ = get_phone_and_service(context['EVENT_TWILIO'].from_phone)

    user = context['SERVICE_API'].get_user_by_phone(client_phone)

    if not user:
        Logger.warn(f"User doesn't exists: {client_phone} | Setting default values")

    user_ci = user.ci if user else None
    user_id = user.id if user else -1
    user_last_state = user.last_state or "" if user else ""
    last_update = user.updated_at if user else datetime.now(timezone.utc)

    hours_diff = int((datetime.now(timezone.utc) - last_update).seconds / 3600)

    Logger.info(f"Context loaded: [ ID: {user_id} | CI: {user_ci} | Status: {user_last_state} | Hours: {hours_diff}]")

    context['DATA_USER_CI'] = user.ci if user else None
    context['DATA_USER_ID'] = user.id if user else -1
    context['DATA_LAST_STATE'] = user.last_state or "" if user else ""


@tree.add_action('1.0', condition=lambda context: context["DATA_LAST_STATE"] == "" and context["DATA_USER_CI"] == "")
def say_welcome(context: ContextType) -> None:
    JASON_PHONE = "whatsapp:+593939893985"
    HUMBERTO_PHONE = "whatsapp:+593996739383"
    JUAN_PHONE = "whatsapp:+593959011576"
    context['SERVICE_TWILIO'](
        "¡Hola! 👋\nSoy *SaragurosNet*.\n\nPor favor ingresa tu número de *cédula/RUC* para continuar.", receiver=JUAN_PHONE)


# @tree.add_action('1.1', condition=lambda _: True)
def say_welcome_client(context: ContextType) -> None:
    pass


# @tree.add_action('1.2', condition=lambda context: context['DATA_LAST_STATE'] == "")
def say_welcome_unknown(context: ContextType) -> None:
    if not context['DATA_USER_CI']:
        Logger.error(f"ID: {context['DATA_USER_ID']} | User doesn't have a CI")
        return

    user_data = context['SERVICE_SARAGUROS'].getUsuarioData(
        context['DATA_USER_CI'])

    if not user_data:
        Logger.error(f"ID: {context['DATA_USER_ID']} | User data is empty")
        return

    res_status = user_data.get('estado')

    if not res_status:
        Logger.error(
            f"ID: {context['DATA_USER_ID']} | Response doesn't have a status")
        return

    user_name: str = "Usuario"
    user_id: str = ""
    msg = "Estimado {user_name} bienvenido a nuestra plataforma."
    observations = "Nuevo lead. ACCION: llamar a celular del lead para cerrar venta"
    ci = ""
    last_status = "1.2"  # Welcome unknown user

    if res_status == 'exito':
        user_name = user_data['datos'][0]['nombre']
        user_id = user_data['datos'][0]['id']
        msg = "Bienvenido {user_name}. ¿En qué puedo ayudarte hoy? Escoge una de las siguientes opciones:"
        observations = ""
        ci = context['DATA_USER_CI']
        last_status = "1.1"  # Welcome known user

    context['SERVICE_TWILIO'](msg.format(user_name=user_name))

    context['SERVICE_API'].update_estado_usuario(
        ci=ci,
        user_id=user_id,
        observations=observations,
        bot_status=last_status,
        phone=context['SERVICE_TWILIO'].receiver,
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
