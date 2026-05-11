from abc import abstractmethod

from exceptions.excepciones import (
    ErrorServicio, ErrorServicioNoDisponible, ErrorCalculoInconsistente
)
from models.entidad import Entidad
from utils.logger import registrar_error, registrar_info

class Servicio(Entidad):
    """
    Clase abstracta que define el contrato común para todos
    los servicios ofrecidos por Software FJ.
    Las clases hijas deben implementar calcular_costo(),
    describir() y validar_parametros().
    """

    IMPUESTO = 0.19      # IVA 19%
    DESCUENTO = 0.10     # Descuento estándar 10%

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        """
        - codigo: identificador único del servicio
        - nombre: nombre del servicio
        - precio_base: precio por hora (debe ser mayor que cero)
        - disponible: indica si el servicio puede reservarse
        """
        self._precio_base = None
        self._disponible = None

        super().__init__(codigo, nombre, activo=disponible)

        self.precio_base = precio_base
        self._disponible = disponible

        registrar_info(
            f"Servicio creado: codigo={codigo}, nombre={nombre}, "
            f"precio_base={precio_base}, disponible={disponible}"
        )

    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            registrar_error(f"Servicio: el precio base debe ser un número.")
            raise ErrorServicio("El precio base debe ser un número.")
        if valor <= 0:
            registrar_error(f"Servicio: el precio base debe ser mayor que cero.")
            raise ErrorServicio("El precio base debe ser mayor que cero.")
        self._precio_base = float(valor)

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ErrorServicio("La disponibilidad debe ser un valor booleano.")
        self._disponible = valor
        self.activo = valor

    def activar_servicio(self):
        """Marca el servicio como disponible."""
        self.disponible = True
        registrar_info(f"Servicio activado: {self.nombre}")

    def desactivar_servicio(self):
        """Marca el servicio como no disponible."""
        self.disponible = False
        registrar_info(f"Servicio desactivado: {self.nombre}")

    def _verificar_disponibilidad(self):
        """Lanza excepción si el servicio no está disponible."""
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{self.nombre}' no está disponible.",
                contexto={"codigo": self.id}
            )

    def _calcular_con_opciones(self, costo_base, con_descuento=False, con_impuesto=False):
        """
        Aplica descuento e impuesto al costo base según los parámetros.
        Lanza ErrorCalculoInconsistente si el resultado es inválido.
        """
        try:
            costo = costo_base

            if con_descuento:
                costo = costo * (1 - self.DESCUENTO)

            if con_impuesto:
                costo = costo * (1 + self.IMPUESTO)

            if costo <= 0:
                raise ErrorCalculoInconsistente(
                    "El costo calculado no puede ser cero o negativo."
                )

            return round(costo, 2)

        except ErrorCalculoInconsistente:
            raise
        except Exception as e:
            raise ErrorCalculoInconsistente(
                "Error inesperado al calcular el costo."
            ) from e


    @abstractmethod
    def calcular_costo(self, duracion, con_descuento=False, con_impuesto=False):
        """Calcula el costo total del servicio según la duración."""
        pass

    @abstractmethod
    def describir(self):
        """Retorna una descripción legible del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida que los parámetros del servicio sean correctos."""
        pass

    def validar(self):
        """Valida las reglas básicas del servicio."""
        if self._precio_base is None or self._precio_base <= 0:
            raise ErrorServicio("El precio base del servicio no es válido.")
        return True