"""Excepciones personalizadas centralizadas para Software FJ.

Estas clases representan errores controlados del dominio. Cuando el error
provenga de una excepcion interna de Python, deben usarse con encadenamiento:

    raise ErrorDatosInvalidos("Dato invalido recibido") from error_original
"""


class ErrorSistema(Exception):
    """Error base para cualquier fallo controlado del sistema.

    Debe usarse como clase padre de todas las excepciones propias del proyecto.
    El parametro contexto permite agregar datos utiles sin exponer detalles
    internos sensibles.
    """

    def __init__(self, mensaje, contexto=None):
        self.mensaje = mensaje
        self.contexto = contexto or {}
        super().__init__(self._construir_mensaje())

    def _construir_mensaje(self):
        if not self.contexto:
            return self.mensaje

        detalles = ", ".join(
            f"{clave}={valor}" for clave, valor in sorted(self.contexto.items())
        )
        return f"{self.mensaje} | contexto: {detalles}"


class ErrorCliente(ErrorSistema):
    """Debe usarse cuando falle una operacion propia de clientes."""


class ErrorServicio(ErrorSistema):
    """Debe usarse cuando falle la creacion, validacion o uso de un servicio."""


class ErrorReserva(ErrorSistema):
    """Debe usarse cuando falle una operacion general de reservas."""


class ErrorValidacion(ErrorSistema):
    """Debe usarse cuando un dato no cumpla las reglas de validacion."""


class ErrorDatosInvalidos(ErrorValidacion):
    """Debe usarse cuando se reciban datos vacios, incompletos o mal formados."""


class ErrorServicioNoDisponible(ErrorServicio):
    """Debe usarse cuando se intente reservar o procesar un servicio inactivo."""


class ErrorReservaInvalida(ErrorReserva):
    """Debe usarse cuando una reserva tenga cliente, servicio, duracion o estado invalido."""


class ErrorCalculoInconsistente(ErrorSistema):
    """Debe usarse cuando un costo, descuento, impuesto o total sea incoherente."""


class ErrorOperacionNoPermitida(ErrorSistema):
    """Debe usarse cuando el estado actual no permita ejecutar una operacion."""


