from abc import ABC, abstractmethod

from exceptions.excepciones import ErrorDatosInvalidos
from utils.logger import registrar_error, registrar_info


class Entidad(ABC):
    """Clase base abstracta para las entidades principales del sistema."""

    def __init__(self, id_entidad, nombre, activo=True):
        self._id = None
        self._nombre = None
        self._activo = None

        self.id = id_entidad
        self.nombre = nombre
        self.activo = activo

        registrar_info(
            f"Entidad creada: tipo={self.__class__.__name__}, "
            f"id={self.id}, nombre={self.nombre}, activo={self.activo}"
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if valor is None:
            self._registrar_error_validacion("El id de la entidad es obligatorio.")

        if isinstance(valor, bool):
            self._registrar_error_validacion(
                "El id de la entidad debe ser texto o numero entero."
            )

        if isinstance(valor, str):
            valor = valor.strip()
            if not valor:
                self._registrar_error_validacion("El id de la entidad no puede estar vacio.")
        elif isinstance(valor, int):
            if valor <= 0:
                self._registrar_error_validacion("El id numerico de la entidad debe ser mayor que cero.")
        else:
            self._registrar_error_validacion(
                "El id de la entidad debe ser texto o numero entero."
            )

        self._id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            self._registrar_error_validacion("El nombre de la entidad debe ser texto.")

        valor = valor.strip()
        if not valor:
            self._registrar_error_validacion("El nombre de la entidad es obligatorio.")

        self._nombre = valor

    @property
    def activo(self):
        return self._activo

    @activo.setter
    def activo(self, valor):
        if not isinstance(valor, bool):
            self._registrar_error_validacion("El estado activo debe ser booleano.")

        self._activo = valor

    def activar(self):
        self.activo = True
        registrar_info(f"Entidad activada: tipo={self.__class__.__name__}, id={self.id}")

    def desactivar(self):
        self.activo = False
        registrar_info(f"Entidad desactivada: tipo={self.__class__.__name__}, id={self.id}")

    @abstractmethod
    def describir(self):
        """Devuelve una descripcion legible de la entidad."""
        pass

    @abstractmethod
    def validar(self):
        """Valida las reglas especificas de la entidad derivada."""
        pass

    def _registrar_error_validacion(self, mensaje, tipo_error=ErrorDatosInvalidos):
        registrar_error(f"{self.__class__.__name__}: {mensaje}")
        raise tipo_error(
            mensaje,
            contexto={"entidad": self.__class__.__name__},
        )
