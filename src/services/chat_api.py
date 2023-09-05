from datetime import datetime
from enum import Enum
from typing import Optional, cast

from src.db import DbConnection


class QueriesOpts(Enum):
    """QueriesOpts class to handle the queries options."""

    GET_CI_BY_PHONE = "GET_CI_BY_PHONE"
    GET_ESTADO_USUARIO = "GET_ESTADO_USUARIO"
    INSERT_ESTADO_USUARIO = "INSERT_ESTADO_USUARIO"
    UPDATE_ESTADO_USUARIO = "UPDATE_ESTADO_USUARIO"


_QUERIES: dict[QueriesOpts, str] = {
    QueriesOpts.GET_CI_BY_PHONE: "SELECT cedula FROM saraguros_net WHERE celular = %s ORDER BY id DESC LIMIT 1",
    QueriesOpts.GET_ESTADO_USUARIO: "SELECT bot_estado, actualizado, usuario_id FROM saraguros_net WHERE celular = %s ORDER BY id DESC LIMIT 1",
    QueriesOpts.INSERT_ESTADO_USUARIO: "INSERT INTO saraguros_net (cedula, celular, bot_estado, observaciones, actualizado, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)",
    QueriesOpts.UPDATE_ESTADO_USUARIO: "UPDATE saraguros_net SET cedula = %s, bot_estado = %s, observaciones = %s, actualizado = %s WHERE celular = %s AND id = (SELECT max(id) FROM saraguros_net WHERE celular = %s)"
}


class ChatApiService(object):
    """ChatApiService class to handle the chat api service."""

    def __init__(self, conn: DbConnection) -> None:
        self._conn = conn

    def get_cedula_by_celular(self, phone: str) -> Optional[str]:
        """Get the cedula of a user by the celular.

        Parameters:
        celular (str): The celular of the user to get the cedula

        Returns:
        str | None: The cedula of the user
        """

        self._conn.connect()

        res = self._conn.execute_query(
            query=_QUERIES[QueriesOpts.GET_CI_BY_PHONE],
            params=(phone,),
            single=True
        )

        self._conn.close()

        if res:
            return cast(str, res[0])

        return None

    def get_estado_usuario(self, phone: str) -> tuple[str, int, str]:
        """Get the status of a user by the phone.

        Parameters:
        phone (str): The phone of the user to get the status

        Returns:
        tuple[str, int, str]: The status of the user, the hours difference and the user id
        """

        self._conn.connect()

        res = self._conn.execute_query(
            query=_QUERIES[QueriesOpts.GET_ESTADO_USUARIO],
            params=(phone,),
            single=True
        )

        self._conn.close()

        # timestamp in db 2023-04-03 17:52:42.041338
        if res:
            bot_status, updated_at, user_id = cast(
                tuple[str, datetime, str], res)
            hours_diff = int(
                (datetime.now() - updated_at).seconds / 3600)

            return bot_status, hours_diff, user_id

        return "", 0, ""

    def update_estado_usuario(self, ci: str, phone: str, bot_status: str, observations: str, updated_at: str, user_id: str) -> bool:
        """Update the status of a user.

        Parameters:
        ci (str): The cedula of the user
        phone (str): The phone of the user
        bot_status (str): The status of the user
        observations (str): The observations of the user
        updated_at (str): The updated_at of the user
        user_id (str): The user_id of the user

        Returns:
        bool: If the status was updated or not
        """

        info_msg = "[WARN] Status not in the options permitted."
        status_updated = False

        if bot_status in ["0.0_cliente_visita_primera_vez", "0.1_visita_recurrente", "1.0_nuevo_cliente"]:
            self._conn.connect()

            res = self._conn.execute_mutation(
                query=_QUERIES[QueriesOpts.INSERT_ESTADO_USUARIO],
                params=(ci, phone, bot_status,
                        observations, updated_at, user_id)
            )

            self._conn.close()

            info_msg = "[INFO] User status inserted." if res else "[ERROR] User status not inserted."
            status_updated = res

        elif bot_status in ["2.0_interesado_pagar_servicio", "2.1_no_valor_pendiente", "1.3_hablar_con_asesor", "1.4_ticket_generado_nousuario", "1.5_vio_promociones", "2.3_servicio_activado_con_evidencia"]:
            self._conn.connect()

            res = self._conn.execute_mutation(
                query=_QUERIES[QueriesOpts.UPDATE_ESTADO_USUARIO],
                params=(ci, bot_status, observations, updated_at, phone, phone)
            )

            self._conn.close()

            info_msg = "[INFO] User status updated." if res else "[ERROR] User status not updated."
            status_updated = res

        print(info_msg)

        return status_updated
