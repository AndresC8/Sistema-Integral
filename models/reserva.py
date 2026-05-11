

from exceptions.excepciones import (
    ErrorReserva, ErrorServicio, ErrorOperacionNoPermitida
)
from utils.logger import registrar_info, registrar_error, registrar_advertencia


# Estados posibles de una reserva
ESTADO_CREADA = "creada"
ESTADO_CONFIRMADA = "confirmada"
ESTADO_CANCELADA = "cancelada"
ESTADO_PROCESADA = "procesada"


class Reserva:
    """
    Clase que representa una reserva en el sistema Software FJ.
    Integra un cliente, un servicio, duración y estado.
    Implementa confirmación, cancelación y procesamiento
    con manejo robusto de excepciones.
    """

    def __init__(self, id_reserva, cliente, servicio, duracion):
        """
        Crea una nueva reserva.
        - id_reserva: identificador único
        - cliente: objeto Cliente válido
        - servicio: objeto Servicio disponible
        - duracion: duración en horas (debe ser mayor que cero)
        """
        self._id_reserva = id_reserva
        self._estado = ESTADO_CREADA

        # Validar cliente
        if cliente is None:
            raise ErrorReserva("El cliente no puede ser nulo.")
        self._cliente = cliente

        # Validar servicio
        if servicio is None:
            raise ErrorReserva("El servicio no puede ser nulo.")
        if not servicio.disponible:
            raise ErrorServicio(
                f"El servicio '{servicio.nombre}' no está disponible."
            )
        self._servicio = servicio

        # Validar duración
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorReserva("La duración debe ser un número mayor que cero.")
        self._duracion = duracion

        registrar_info(
            f"Reserva creada: id={self._id_reserva}, "
            f"cliente={self._cliente.nombre}, "
            f"servicio={self._servicio.nombre}, "
            f"duracion={self._duracion}h"
        )


    @property
    def id_reserva(self):
        return self._id_reserva

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion


    def confirmar(self):
        """Confirma la reserva si está en estado 'creada'."""
        if self._estado == ESTADO_CANCELADA:
            raise ErrorOperacionNoPermitida(
                "No se puede confirmar una reserva cancelada."
            )
        if self._estado == ESTADO_CONFIRMADA:
            raise ErrorOperacionNoPermitida(
                "La reserva ya está confirmada."
            )
        self._estado = ESTADO_CONFIRMADA
        registrar_info(f"Reserva {self._id_reserva} confirmada.")

    def cancelar(self):
        """Cancela la reserva si no ha sido procesada."""
        if self._estado == ESTADO_PROCESADA:
            raise ErrorOperacionNoPermitida(
                "No se puede cancelar una reserva ya procesada."
            )
        if self._estado == ESTADO_CANCELADA:
            raise ErrorOperacionNoPermitida(
                "La reserva ya está cancelada."
            )
        self._estado = ESTADO_CANCELADA
        registrar_advertencia(f"Reserva {self._id_reserva} cancelada.")

    def procesar(self, con_descuento=False, con_impuesto=False):
        """
        Procesa la reserva calculando el costo final.
        Solo se puede procesar una reserva confirmada.
        Usa try/except/else/finally para manejo robusto.
        """
        try:
            if self._estado != ESTADO_CONFIRMADA:
                raise ErrorOperacionNoPermitida(
                    f"Solo se pueden procesar reservas confirmadas. "
                    f"Estado actual: {self._estado}"
                )
            costo = self._servicio.calcular_costo(
                self._duracion,
                con_descuento=con_descuento,
                con_impuesto=con_impuesto
            )

        except ErrorOperacionNoPermitida as e:
            registrar_error(f"Reserva {self._id_reserva}: {e}")
            raise

        except Exception as e:
            registrar_error(
                f"Error inesperado al procesar reserva {self._id_reserva}: {e}"
            )
            raise ErrorReserva(
                "Fallo interno al calcular el costo de la reserva."
            ) from e

        else:
            self._estado = ESTADO_PROCESADA
            registrar_info(
                f"Reserva {self._id_reserva} procesada. "
                f"Costo total: ${costo:.2f}"
            )
            return costo

        finally:
            registrar_info(
                f"Intento de procesamiento finalizado para reserva {self._id_reserva}."
            )

    def describir(self):
        """Retorna un resumen de la reserva."""
        return (
            f"Reserva {self._id_reserva} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion}h | "
            f"Estado: {self._estado}"
        )