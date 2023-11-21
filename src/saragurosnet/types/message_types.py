from typing import Final


class MessageType():
    SAY_HELLO: Final[str] = "¡Hola! 👋\nSoy *SaragurosNet*.\n\nPor favor ingresa tu número de *cédula/RUC* para continuar."
    ERROR_INVALID_CI: Final[str] = "El número de cédula/RUC ingresado no es válido. Por favor intenta nuevamente."
    ERROR_CLIENT_NOT_FOUND: Final[str] = "Lo sentimos, hubo un error al procesar tu mensaje. Por favor intenta más tarde."
    WELCOME_UNKNOW: Final[str] = "Estimado {name} bienvenido a nuestra plataforma."
    WELCOME_CLIENT: Final[str] = "Bienvenido {name}. ¿En qué puedo ayudarte hoy? Escoge una de las siguientes opciones:"
    PROMOTIONS: Final[str] = "Conoce nuestros excelentes planes en promoción."
    COVERAGES: Final[str] = "Conoce la cobertura que ofrece nuestra empresa."
    HELLO_AGENTS: Final[str] = "Estimado {name}, soy tu agente de atención virtual en Saraguros Net. ¿En qué te puedo ayudar?\nEscríbeme en un mensaje tu requerimiento, gracias."
    CONNECT_AGENT: Final[str] = "Estimado {name},\nSe ha generado un ticket a uno de nuestros agentes de venta\nPor favor espere mientras nuestro agente se pone en contacto con usted."
    INVOICES_PENDING: Final[
        str] = "Estimado {name},\nTienes {num_invoices} factura(s) por pagar:\n{invoice_table}\nEl monto total a pagar es de {invoice_total}"
    PAYMENT_METHOD: Final[str] = "Selecciona el método de pago que más te convenga:\n*TRANSFERENCIA*: _Deberas subir una imagen del comprobante._\n*TARJETA*: _Pago mediante tarjeta de crédito o débito._\n*PUNTO DE PAGO*: _Pago en efectivo en nuestros puntos de pago._"
    END_CONVERSATION: Final[str] = "Estimado {name},\nAgradecemos su tiempo. Si desea continuar explorando nuestros servicios o tiene más preguntas, seleccione *TENGO MÁS DUDAS* y estaremos encantados de ayudarle. Caso contrario, seleccione *FINALIZAR CONSULTA*."
    SAY_GOODBAY: Final[str] = "Gracias por contactarnos. ¡Hasta pronto!"

    TELL_ME_YOUR_NAMES: Final[str] = "Estimado {name}, por favor ingresa tus nombres. _ejm: Juan Carlos_"
    TELL_ME_YOUR_LASTNAMES: Final[str] = "Estimado {name}, por favor ingresa tus apellidos. _ejm: Pérez López_"
    TELL_ME_YOUR_EMAIL: Final[str] = "Estimado {name}, por favor ingresa tu correo electrónico. _ejm: example@email.com_"

    ERROR_INVALID_NAMES: Final[str] = "Estimado {name}, el nombre ingresado no es válido. Por favor intenta nuevamente."
    ERROR_INVALID_LASTNAMES: Final[str] = "Estimado {name}, el apellido ingresado no es válido. Por favor intenta nuevamente."
    ERROR_INVALID_EMAIL: Final[str] = "Estimado {name}, el correo electrónico ingresado no es válido. Por favor intenta nuevamente."
