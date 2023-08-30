from datetime import datetime
from typing import Optional, TypedDict, cast

from src.db import DbConnection

QueriesType = TypedDict("QueriesType", {
    "GET_CI_BY_PHONE": str,
    "GET_ESTADO_USUARIO": str,
    "INSERT_ESTADO_USUARIO": str,
    "UPDATE_ESTADO_USUARIO": str,
})

QUERIES: QueriesType = {
    "GET_CI_BY_PHONE": "SELECT cedula FROM saraguros_net WHERE celular = %s ORDER BY id DESC LIMIT 1",
    "GET_ESTADO_USUARIO": "SELECT bot_estado, actualizado, usuario_id FROM saraguros_net WHERE celular = %s ORDER BY id DESC LIMIT 1",
    "INSERT_ESTADO_USUARIO": "INSERT INTO saraguros_net (cedula, celular, bot_estado, observaciones, actualizado, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)",
    "UPDATE_ESTADO_USUARIO": "UPDATE saraguros_net SET cedula = %s, bot_estado = %s, observaciones = %s, actualizado = %s WHERE celular = %s AND id = (SELECT max(id) FROM saraguros_net WHERE celular = %s)"
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
            query=QUERIES["GET_CI_BY_PHONE"],
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
            query=QUERIES["GET_ESTADO_USUARIO"],
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
                query=QUERIES["INSERT_ESTADO_USUARIO"],
                params=(ci, phone, bot_status,
                        observations, updated_at, user_id)
            )

            self._conn.close()

            info_msg = "[INFO] User status inserted." if res else "[ERROR] User status not inserted."
            status_updated = res

        elif bot_status in ["2.0_interesado_pagar_servicio", "2.1_no_valor_pendiente", "1.3_hablar_con_asesor", "1.4_ticket_generado_nousuario", "1.5_vio_promociones", "2.3_servicio_activado_con_evidencia"]:
            self._conn.connect()

            res = self._conn.execute_mutation(
                query=QUERIES["UPDATE_ESTADO_USUARIO"],
                params=(ci, bot_status, observations, updated_at, phone, phone)
            )

            self._conn.close()

            info_msg = "[INFO] User status updated." if res else "[ERROR] User status not updated."
            status_updated = res

        print(info_msg)

        return status_updated
