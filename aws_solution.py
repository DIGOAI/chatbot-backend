import json
import os
import re
from datetime import datetime, timedelta

import openai
import psycopg2
import requests
from twilio.rest import Client

###########################################
## START - HELPER FUNCTIONS              ##
###########################################

# === COMPLETE ===


def ask_chatgpt(text: str) -> str:
    asunto = ''
    departamento = ''
    openai.api_key = os.environ['OPENAI_KEY']

    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'El siguiente es un mensaje de un cliente en un canal de sorpote: {text}. A partir del mensaje del cliente determina a cuál de las siguientes categorías de atención pertenece el mensaje: Disponibilidad del servicio por falla técnica, Lentitud o baja velocidad del servicio, Problemas con la antena o baja señal de equipo CPE, Problemas del servicio por ausencia o falla en potencia óptica, Problemas con el router o señal WIFI, Cambio de clave WIFI, Bloqueo de servicios o accesos a internet, Falla masiva, Congelamiento temporal del servicio, Traslado del servicio, Cambio de condiciones del servicio, Suspensión Injustificada, Cesión de contrato, Servicios adicionales, Contratación de servicios, Equipos en comodato, Terminación de contrato, Certificaciones y paz y salvo, Fidelización, Reclamo sobre reporte a centrales de riesgos, Cambio de periodos de facturación, Reclamo sobre facturación, Descuento o compensación, Recurso de reposición, Recurso de reposición y en subsidio de apelación, Cumplimiento de una orden de la SIC, Sugerencias, Otras PQ. Selecciona además qué departamento debería atender al usuario: Soporte técnico, Ventas, Quejas y Sugerencias. El output debe ser estrictamente: categoría sugerida,departamento sugerido',
        temperature=0.5,
        max_tokens=1024
    )

    r = completion.choices[0]['text']
    response = r.replace('[\s\.\n]+', '')

    return response
# === COMPLETE ===


# === COMPLETE ===


def activar_servicio(usuario_id):
    url = "https://mw.saraguros.info/api/v1/ActiveService"
    headers = {"Content-Type": "application/json"}

    data = {
        "token": "R3Z4SlNrWVZvZzFsV1pvTTQ3ci9wZz09",
        "idcliente": usuario_id
    }

    response = requests.post(
        url, headers=headers, data=json.dumps(data))
    return response.json()
# === COMPLETE ===

# === COMPLETE ===


def create_ticket(contenido, asunto, departamento, turno, usuario_id, fechavisita, agendado):
    url = "https://mw.saraguros.info/api/v1/NewTicket"
    headers = {"Content-Type": "application/json"}

    data = {
        "token": "R3Z4SlNrWVZvZzFsV1pvTTQ3ci9wZz09",
        "idcliente": usuario_id,
        "dp": departamento,
        "asunto": asunto,
        "fechavisita": fechavisita,
        "turno": turno,
        "agendado": agendado,
        "contenido": contenido
    }

    response = requests.post(
        url, headers=headers, data=json.dumps(data))
    return response.json()
# === COMPLETE ===

# === COMPLETE ===


def parse_transaccion(image_text):
    nombre_usuario = ""
    fecha = ""
    monto = ""
    oficina = ""
    lines = image_text.split('\n')

    match = re.search(
        r'COAC.*JARDIN AZUAYO', lines[0])
    if match:
        nombre_usuario = lines[4]
        fecha = lines[7]
        monto = lines[15]
        oficina = lines[16]
        return nombre_usuario, fecha, monto, oficina
# === COMPLETE ===

# === COMPLETE ===


def get_cedula_by_celular(celular):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            database="chatbots",
            user="postgres",
            password="ZvLk2aFM",
            host="ihub.cbok7gpaemrw.us-east-1.rds.amazonaws.com",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Define the SQL query to retrieve the cedula where celular matches
        sql = "SELECT cedula FROM saraguros_net WHERE celular = %s ORDER BY id DESC LIMIT 1"

        # Execute the query with the given celular value
        cur.execute(sql, (celular,))

        # Fetch the result
        result = cur.fetchone()

        if result:
            # Return the cedula value if found
            return result[0]
        else:
            # Return an empty string if no match is found
            return ""

    except (Exception, psycopg2.Error) as error:
        print(
            "Error while retrieving data from the table:", error)
        return ""

    finally:
        # Close the database connection and cursor
        if cur:
            cur.close()
        if conn:
            conn.close()
# === COMPLETE ===

# === COMPLETE ===


def getEstadoUsuario(celular):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            database="chatbots",
            user="postgres",
            password="ZvLk2aFM",
            host="ihub.cbok7gpaemrw.us-east-1.rds.amazonaws.com",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Define the SQL query to retrieve the bot_estado and actualizado where celular matches
        sql = "SELECT bot_estado, actualizado, usuario_id FROM saraguros_net WHERE celular = %s ORDER BY id DESC LIMIT 1"

        # Execute the query with the given celular value
        cur.execute(sql, (celular,))

        # Fetch the result
        result = cur.fetchone()

        if result:
            # Get the bot_estado and actualizado values from the result
            bot_estado = result[0]
            actualizado = result[1]
            usuario_id = result[2]

            # Get the current time and calculate the difference in hours
            current_time = datetime.now()
            # actualizado_time = datetime.strptime(actualizado, '%Y-%m-%d %H:%M:%S.%f')
            difference_hours = int(
                (current_time - actualizado).total_seconds() / 3600)

            # Return the bot_estado and difference in hours
            return bot_estado, difference_hours, usuario_id
        else:
            # Return an empty string and 0 hours difference if no match is found
            return "", 0, ""

    except (Exception, psycopg2.Error) as error:
        print(
            "Error while retrieving data from the table:", error)
        return "", 0, ""

    finally:
        # Close the database connection and cursor
        if cur:
            cur.close()
        if conn:
            conn.close()
# === COMPLETE ===

# === COMPLETE ===


def getUsuarioData(cedula):
    url = "https://mw.saraguros.info/api/v1/GetClientsDetails"
    headers = {"Content-Type": "application/json"}
    data = {
        "token": "R3Z4SlNrWVZvZzFsV1pvTTQ3ci9wZz09",
        "cedula": cedula
    }
    response = requests.post(
        url, headers=headers, data=json.dumps(data))
    return response.json()
# === COMPLETE ===

# === COMPLETE ===


def updateEstadoUsuario(cedula, celular, bot_estado, observaciones, actualizado, usuario_id):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            database="chatbots",
            user="postgres",
            password="ZvLk2aFM",
            host="ihub.cbok7gpaemrw.us-east-1.rds.amazonaws.com",
            port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        if bot_estado == "0.0_cliente_visita_primera_vez" or bot_estado == "0.1_visita_recurrente" or bot_estado == "1.0_nuevo_cliente":
            # Define the SQL query to insert data into the table
            sql = "INSERT INTO saraguros_net (cedula, celular, bot_estado, observaciones, actualizado, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"

            # Execute the query with the given arguments
            cur.execute(sql, (cedula, celular, bot_estado,
                        observaciones, actualizado, usuario_id))

        if bot_estado == '2.0_interesado_pagar_servicio' or bot_estado == '2.1_no_valor_pendiente' or bot_estado == '1.3_hablar_con_asesor' or bot_estado == '1.4_ticket_generado_nousuario' or bot_estado == '1.5_vio_promociones' or bot_estado == '2.3_servicio_activado_con_evidencia':
            # Define the SQL query for UPDATE
            sql = "UPDATE saraguros_net SET cedula = %s, bot_estado = %s, observaciones = %s, actualizado = %s WHERE celular = %s AND id = (SELECT max(id) FROM saraguros_net WHERE celular = %s)"

            # Execute the query with the given arguments
            cur.execute(sql, (cedula, bot_estado, observaciones,
                        actualizado, celular, celular))

        # Commit the transaction
        conn.commit()

        print(
            "Data inserted successfully into the table.")

    except (Exception, psycopg2.Error) as error:
        print(
            "Error while inserting data into the table:", error)

    finally:
        # Close the database connection and cursor
        if cur:
            cur.close()
        if conn:
            conn.close()
# === COMPLETE ===


###########################################
## END - HELPER FUNCTIONS                ##
###########################################


def lambda_handler(event, context):
    # TODO implement
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    Body = event['Body']
    From = event['From']
    MediaUrl0 = event['MediaUrl0']

    ####################################################################
    # 1 - Obtener el estado del usuario a partir del número de cédula  #
    ####################################################################
    titular_celular = From.replace(
        "whatsapp:+593", "")
    titular_celular = "0" + titular_celular

    # 1.1. Obtener el último estado del cliente
    estado_usuario, edad_estado, usuario_id = getEstadoUsuario(
        titular_celular)
    print(estado_usuario + " : " +
          repr(edad_estado))

    ####################################################################
    # 1.2 - Onboarding para nuevo usuario y recurrentes                #
    ####################################################################
    if estado_usuario == "":  # El usuario nunca ha usado este canal
        match = re.search(r"\d{10}", Body)
        if match:
            print("Escribió la cédula")
            data = getUsuarioData(Body)
            # El usuario es cliente de SARAGUROS.NET
            if data['estado'] == "exito":
                for el in data['datos']:
                    usuario_nombre = el['nombre']
                    usuario_id = el['id']

                message = client.messages.create(
                    from_='whatsapp:+593993999510',
                    # <= OPCIONES CLIENTE TEMPLATE
                    body=f'Bienvenido {usuario_nombre}. ¿En qué puedo ayudarte hoy? Escoge una de las siguientes opciones:',
                    to=From)

                print(usuario_id)
                timestamp = datetime.now()
                updateEstadoUsuario(
                    Body, titular_celular, '0.0_cliente_visita_primera_vez', '', timestamp, usuario_id)

            # El usuario no es cliente de SARAGUROS.NET
            elif data['estado'] == "error":

                nombre = "Usuario"
                message = client.messages.create(
                    from_='whatsapp:+593993999510',
                    body=f'Estimado {nombre} bienvenido a nuestra plataforma.',
                    to=From)

                # Dejar huella del estado 1.0_nuevo_cliente
                timestamp = datetime.now()
                updateEstadoUsuario(Body, titular_celular, '1.0_nuevo_cliente',
                                    'Nuevo lead. ACCION: llamar a celular del lead para cerrar venta', timestamp, usuario_id)

        elif Body != 'Hablar con asesor':
            # Enviar el mensaje de inicio
            message = client.messages.create(
                from_='whatsapp:+593993999510',
                body='¡Hola! Soy Saraguros Net. Ingresa tu número de cédula para continuar.',
                to=From)
    # El usuario es recurrente en este canal y su último estado es un END STATE
    elif (estado_usuario != '1_interesado_contratar') and (estado_usuario == '2.3_servicio_activado_con_evidencia' or estado_usuario == '1.4_ticket_generado_nousuario'):
        cedula = get_cedula_by_celular(
            titular_celular)
        print("Cedula: " + cedula)
        data = getUsuarioData(cedula)
        # El usuario es cliente de SARAGUROS.NET
        if data['estado'] == "exito":
            for el in data['datos']:
                usuario_nombre = el['nombre']
                usuario_id = el['id']

            message = client.messages.create(
                from_='whatsapp:+593993999510',
                # <= OPCIONES CLIENTE TEMPLATE
                body=f'Bienvenido {usuario_nombre}. ¿En qué puedo ayudarte hoy? Escoge una de las siguientes opciones:',
                to=From)

            timestamp = datetime.now()
            print("Aquí")
            updateEstadoUsuario(
                cedula, titular_celular, '0.1_visita_recurrente', '', timestamp, usuario_id)
            print("Terminado")

        else:
            nombre = "Usuario"
            message = client.messages.create(
                from_='whatsapp:+593993999510',
                body=f'Estimado {nombre} bienvenido a nuestra plataforma.',
                to=From)

            # Dejar huella del estado 1.0_nuevo_cliente
            timestamp = datetime.now()
            updateEstadoUsuario(Body, titular_celular, '1.0_nuevo_cliente',
                                'Nuevo lead. ACCION: llamar a celular del lead para cerrar venta', timestamp, usuario_id)

    ####################################################################
    # 1.3 - Hablar con asesor  & 1.4                                   #
    ####################################################################
    if Body == 'Hablar con asesor' and estado_usuario == "1.0_nuevo_cliente":
        message = client.messages.create(
            from_='whatsapp:+593993999510',
            # <= OPCIONES CLIENTE TEMPLATE
            body='Soy tu agente de ventas virtual en Saraguros Net. ¿En qué te puedo ayudar? Escríbeme en un mensaje tu requerimiento. Gracias',
            to=From)

        cedula = get_cedula_by_celular(
            titular_celular)
        timestamp = datetime.now()
        updateEstadoUsuario(cedula, titular_celular,
                            '1.3_hablar_con_asesor', '', timestamp, usuario_id)

    if estado_usuario == "1.3_hablar_con_asesor":
        r = ask_chatgpt(Body)
        data = r.split(',')
        departamentos = {
            "Ventas": 2,
            "Soporte técnico": 1,
            "Quejas y Sugerencias": 3
        }

        # Campos para el ticket
        # DEBEMOS CREAR UN USUARIO PARA RECEPTAR LOS TICKES DE LOS AUN NO USUARIOS.
        usuario_id = 5591
        contenido = Body + \
            ". Llamar al usuario al: " + titular_celular
        turno = "TARDE"
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        fechavisita = tomorrow.strftime(
            '%Y-%m-%d')
        dep_str = data[1].lstrip()
        dep_str2 = dep_str.replace('.', '')
        departamento = departamentos[dep_str2]
        asunto_str = data[0]
        asunto = asunto_str.replace(' .', '')

        agendado = "RED SOCIAL"

        rt = create_ticket(contenido, asunto, departamento,
                           turno, usuario_id, fechavisita, agendado)
        idticket = " "
        estado_ticket = rt['estado']
        if estado_ticket == "exito":
            idticket = rt['idticket']

        message = client.messages.create(
            from_='whatsapp:+593993999510',
            # <= OPCIONES CLIENTE TEMPLATE
            body=f'Su turno ha sido creado con: *{estado_ticket}* y su número de ticket es: *{idticket}* el mismo que será atendido por el departamento de: *{data[1]}*. Ha sido un placer atenderle. Escriba *INICIO* para regresar a las opociones principales. Gracias.',
            to=From)

        cedula = get_cedula_by_celular(
            titular_celular)
        timestamp = datetime.now()
        updateEstadoUsuario(cedula, titular_celular,
                            '1.4_ticket_generado_nousuario', '', timestamp, usuario_id)

        message = client.messages.create(
            from_='whatsapp:+593993999510',
            # <= OPCIONES CLIENTE TEMPLATE
            body=f'MENSAJE DE CHATBOT: Se ha generado el ticket: *{idticket}* para el departamento *{data[1]}* con el asunto: {asunto}. Por favor asignar un asesor. Gracias.',
            to='whatsapp:+593939893985')

        # print(data[0])
        # print(data[1])
        # message = client.messages.create(
        #        from_ = 'whatsapp:+593993999510',
        #        body = r, # <= OPCIONES CLIENTE TEMPLATE
        #        to = From)

    if estado_usuario == "1.4_ticket_generado_nousuario" and Body == 'INICIO':
        nombre = "Usuario"
        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body=f'Estimado {nombre} bienvenido a nuestra plataforma.',
            to=From)

        timestamp = datetime.now()
        cedula = get_cedula_by_celular(
            titular_celular)
        updateEstadoUsuario(cedula, titular_celular, '1.0_nuevo_cliente',
                            'Nuevo lead. ACCION: llamar a celular del lead para cerrar venta', timestamp, usuario_id)

    ####################################################################
    # 1.5 - Promociones                                                #
    ####################################################################
    if Body == 'Promociones' and estado_usuario == "1.0_nuevo_cliente":
        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body='Conoce nuestros excelentes planes en promoción. Escribe *INICIO* para regresar a las opciones principales.',
            media_url='https://i.ibb.co/Nn3ZDG7/saraguros-net-planes1.jpg',
            to=From)

        timestamp = datetime.now()
        cedula = get_cedula_by_celular(
            titular_celular)
        updateEstadoUsuario(cedula, titular_celular, '1.5_vio_promociones',
                            'Nuevo lead. ACCION: llamar a celular del lead para cerrar venta', timestamp, usuario_id)

    if estado_usuario == "1.5_vio_promociones" and Body == 'INICIO':
        nombre = "Usuario"
        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body=f'Estimado {nombre} bienvenido a nuestra plataforma.',
            to=From)

        timestamp = datetime.now()
        cedula = get_cedula_by_celular(
            titular_celular)
        updateEstadoUsuario(cedula, titular_celular, '1.0_nuevo_cliente',
                            'Nuevo lead. ACCION: llamar a celular del lead para cerrar venta', timestamp, usuario_id)

    ####################################################################
    # 2 - PAGAR SERVICIO                                               #
    ####################################################################
    if Body == 'PAGA TU SERVICIO':
        cedula = get_cedula_by_celular(
            titular_celular)
        print(cedula)
        data = getUsuarioData(cedula)
        # El usuario es cliente de SARAGUROS.NET
        if data['estado'] == "exito":
            for el in data['datos']:
                facturacion = el['facturacion']
                facturas_nopagadas = facturacion['facturas_nopagadas']
                total_facturas = facturacion['total_facturas']

            if facturas_nopagadas > 0:
                message = client.messages.create(
                    from_='whatsapp:+593993999510',
                    body=f'Tienes {facturas_nopagadas} facturas por pagar por un monto total de {total_facturas} dólares.',
                    to=From)

                timestamp = datetime.now()
                updateEstadoUsuario(
                    cedula, titular_celular, '2.0_interesado_pagar_servicio', '', timestamp, usuario_id)

            else:
                message = client.messages.create(
                    from_='whatsapp:+593993999510',
                    body='No posees ningún valor pendiente. Gracias por ponerte en contacto con nosotros. Hasta pronto.',
                    to=From)

                timestamp = datetime.now()
                updateEstadoUsuario(
                    cedula, titular_celular, '2.1_no_valor_pendiente', '', timestamp, usuario_id)

    ####################################################################
    # 2.2 - PAGAR SERVICIO MEDIANTE EVIDENCIA DE TRANSFERENCIA  & 2.3. #
    ####################################################################
    if Body == 'Transferencia' and estado_usuario == '2.0_interesado_pagar_servicio':
        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body='Por favor compartenos una foto del comprobante de transferencia. Si lo que posees es un PDF, compartenos una captura del mismo. Gracias.',
            to=From)

    if MediaUrl0.startswith('https://') and estado_usuario == '2.0_interesado_pagar_servicio':
        url = "https://flr88xbq98.execute-api.us-east-1.amazonaws.com/beta/ocr-helper"
        headers = {
            "Content-Type": "application/json"}
        data = {
            "image_url": MediaUrl0
        }
        response = requests.post(
            url, headers=headers, data=json.dumps(data))
        image_text = response.json()['image_text']

        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body=MediaUrl0,
            to=From)

        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body=image_text,
            to=From)

        nombre_usuario, fecha, monto, oficina = parse_transaccion(
            image_text)

        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body=f'Hemos confirmado la transacción realizada {fecha}. Procederemos a activar su servicio.',
            to=From)

        r = activar_servicio(usuario_id)
        if r['estado'] == 'exito':
            message = client.messages.create(
                from_='whatsapp:+593993999510',
                body=r['mensaje'],
                to=From)
        else:
            message = client.messages.create(
                from_='whatsapp:+593993999510',
                body='Lamentablemente no pudimos activar su servicio. Por favor comuníquese al 0000000000. Gracias',
                to=From)

        cedula = get_cedula_by_celular(
            titular_celular)
        timestamp = datetime.now()
        updateEstadoUsuario(cedula, titular_celular,
                            '2.3_servicio_activado_con_evidencia', '', timestamp, usuario_id)

        # lines = image_text.split('\n')
        # nro_transaccion = lines[len(lines) - 1]
        # valor_transferido = lines[len(lines) - 4]
        # message = client.messages.create(
        #            from_ = 'whatsapp:+593993999510',
        #            body = f'Hemos encontrado la transacción número: {nro_transaccion} por un valor de: {valor_transferido} dólares.',
        #            to = From)

    ####################################################################
    # 3 - ESTADO DEL SERVICIO & 3.1                                    #
    ####################################################################
    if Body == 'ESTADO DEL SERVICIO':
        # Consultar estado del servicio y plan del usuario.

        cedula = get_cedula_by_celular(
            titular_celular)
        data = getUsuarioData(cedula)
        estado_servicio = ""
        tiposervicio = ""

        # El usuario es cliente de SARAGUROS.NET
        if data['estado'] == "exito":
            for el in data['datos']:
                estado_servicio = el['estado']
                for servicio in el['servicios']:
                    tiposervicio = servicio['tiposervicio']

            message = client.messages.create(
                from_='whatsapp:+593993999510',
                body=f'El estado de su servicio de *{tiposervicio}* es *{estado_servicio}*. Ahora pudes continuar presionando los otros botones de opciones.',
                to=From)

        else:
            message = client.messages.create(
                from_='whatsapp:+593993999510',
                body='Lo sentimos, no fue posible consultar el estado de su servicio. Puede comunicarse al 0000000000.Gracias.',
                to=From)

        # Cambiar el estado a 3.1.Estado_consultado
        # Poner un botón de regresar al inicio

    ####################################################################
    # 4 - MESA DE AYUDA                                                #
    ####################################################################
    # Preguntar las categorias de los tickets. ChatGPT las categorizará
    if Body == 'MESA DE AYUDA':
        message = client.messages.create(
            from_='whatsapp:+593993999510',
            body='¿Cómo podemos ayudarte? Descríbenos el inconveniente que se presentó.',
            to=From)

        updateEstadoUsuario(cedula, titular_celular,
                            '4.0_esperando_texto_ticket', '', timestamp, usuario_id)

    if Body != 'MESA DE AYUDA' and estado_usuario == '4.0_esperando_texto_ticket':
        asunto, departamento = ask_chatgtp(Body)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
