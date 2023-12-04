TICKET_TYPE_PROMPT = """El siguiente es un mensaje de un cliente en un canal de sorpote:

{message}.

A partir del mensaje del cliente determina a cuál de las siguientes categorías de atención pertenece el mensaje:

- Disponibilidad del servicio por falla técnica.
- Lentitud o baja velocidad del servicio.
- Problemas con la antena o baja señal de equipo CPE.
- Problemas del servicio por ausencia o falla en potencia óptica.
- Problemas con el router o señal WIFI.
- Cambio de clave WIFI.
- Bloqueo de servicios o accesos a internet.
- Falla masiva.
- Congelamiento temporal del servicio.
- Traslado del servicio.
- Cambio de condiciones del servicio.
- Suspensión Injustificada.
- Cesión de contrato.
- Servicios adicionales.
- Contratación de servicios.
- Equipos en comodato.
- Terminación de contrato.
- Certificaciones y paz y salvo.
- Fidelización.
- Reclamo sobre reporte a centrales de riesgos.
- Cambio de periodos de facturación.
- Reclamo sobre facturación.
- Descuento o compensación.
- Recurso de reposición.
- Recurso de reposición y en subsidio de apelación.
- Cumplimiento de una orden de la SIC.
- Sugerencias.
- Otras PQ.

Selecciona además qué departamento debería atender al usuario:

- Soporte técnico
- Ventas
- Quejas y Sugerencias.

El output debe ser estrictamente: "categoría sugerida, departamento sugerido"
"""


OCR_DATA_PROMPT = """
        Below I will show you a set of tokens extracted from an OCR process to a bank payment receipt:
        
        {text_data}

        Based on the tokens, I need you to extract the following information, the bank or financial institution that issues the receipt, the person or client who makes this payment, the date of the transaction, the time of the transaction, the type of currency, ( e.g. USD, EUR), and the amount or value of the payment.
        
        Returns a Json with the following structure:
        {{
            "bank": "bank from text, put null if not found",
            "customer": "name of the customer from" or null,
            "date": "date from text on format YYYY-MM-DD" or null,
            "hour": "hour from text on format HH:MM" or null,
            "currency": "currency from text (USD, EUR)" or null,
            "total": <numeric value> or null
        }}
    """
