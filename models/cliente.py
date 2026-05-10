import re

from exceptions.excepciones import ErrorCliente, ErrorValidacion
from models.entidad import Entidad
from utils.logger import registrar_error, registrar_info


class Cliente(Entidad):
    """Representa un cliente de Software FJ con datos personales validados."""

    _PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _PATRON_DOCUMENTO = re.compile(r"^[A-Za-z0-9-]+$")

    def __init__(self, documento, nombre, correo, telefono, activo=True):
        self._documento = None
        self._correo = None
        self._telefono = None

        try:
            super().__init__(documento, nombre, activo)
            self.documento = documento
            self.correo = correo
            self.telefono = telefono
            self.validar()
        except ErrorValidacion:
            raise
        except Exception as error:
            registrar_error(f"No fue posible registrar el cliente: {error}")
            raise ErrorCliente(
                "No fue posible registrar el cliente.",
                contexto={"documento": documento},
            ) from error
        else:
            registrar_info(
                f"Cliente registrado correctamente: documento={self.documento}, "
                f"nombre={self.nombre}"
            )

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor = self._normalizar_texto(valor, "documento")

        if not self._PATRON_DOCUMENTO.match(valor):
            self._registrar_error_cliente(
                "El documento solo puede contener letras, numeros o guiones."
            )

        self._documento = valor
        self.id = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        valor = self._normalizar_texto(valor, "correo").lower()

        if not self._PATRON_CORREO.match(valor):
            self._registrar_error_cliente("El correo electronico no tiene un formato valido.")

        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._normalizar_texto(valor, "telefono")

        if not valor.isdigit():
            self._registrar_error_cliente("El telefono debe contener solo numeros.")

        if len(valor) < 7 or len(valor) > 15:
            self._registrar_error_cliente("El telefono debe tener entre 7 y 15 digitos.")

        self._telefono = valor

    def actualizar_contacto(self, correo=None, telefono=None):
        if correo is not None:
            self.correo = correo

        if telefono is not None:
            self.telefono = telefono

        registrar_info(f"Contacto actualizado para cliente documento={self.documento}")

    def describir(self):
        return (
            f"Cliente {self.nombre} identificado con documento {self.documento}, "
            f"correo {self.correo} y telefono {self.telefono}."
        )

    def validar(self):
        if not self.documento:
            self._registrar_error_cliente("El documento del cliente es obligatorio.")

        if not self.nombre:
            self._registrar_error_cliente("El nombre del cliente es obligatorio.")

        if not self.correo:
            self._registrar_error_cliente("El correo del cliente es obligatorio.")

        if not self.telefono:
            self._registrar_error_cliente("El telefono del cliente es obligatorio.")

        return True

    def _normalizar_texto(self, valor, campo):
        if valor is None:
            self._registrar_error_cliente(f"El campo {campo} es obligatorio.")

        if isinstance(valor, bool):
            self._registrar_error_cliente(f"El campo {campo} debe ser texto.")

        if isinstance(valor, int):
            valor = str(valor)
        elif not isinstance(valor, str):
            self._registrar_error_cliente(f"El campo {campo} debe ser texto.")

        valor = valor.strip()
        if not valor:
            self._registrar_error_cliente(f"El campo {campo} no puede estar vacio.")

        return valor

    def _registrar_error_cliente(self, mensaje):
        registrar_error(f"Cliente: {mensaje}")
        raise ErrorValidacion(
            mensaje,
            contexto={"entidad": "Cliente", "documento": self._documento},
        )
