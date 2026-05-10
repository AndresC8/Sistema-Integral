import re

from exceptions.excepciones import ErrorCliente, ErrorValidacion
from models.entidad import Entidad
from utils.logger import registrar_error, registrar_info


class Cliente(Entidad):
    """Representa un cliente de Software FJ con datos personales validados."""

    _PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _PATRON_DOCUMENTO = re.compile(r"^[A-Za-z0-9-]+$")
    _MIN_DOCUMENTO = 5
    _MAX_DOCUMENTO = 20
    _MIN_NOMBRE = 3
    _MAX_NOMBRE = 80
    _MAX_CORREO = 120
    _MIN_TELEFONO = 7
    _MAX_TELEFONO = 15

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
        valor = self._normalizar_texto(valor, "documento", permitir_entero=True)
        self._validar_longitud(
            valor,
            "documento",
            self._MIN_DOCUMENTO,
            self._MAX_DOCUMENTO,
        )

        if not self._PATRON_DOCUMENTO.match(valor):
            self._registrar_error_cliente(
                "El documento solo puede contener letras, numeros o guiones."
            )

        self._documento = valor
        self.id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._normalizar_texto(valor, "nombre")
        self._validar_longitud(valor, "nombre", self._MIN_NOMBRE, self._MAX_NOMBRE)
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        valor = self._normalizar_texto(valor, "correo").lower()
        self._validar_longitud(valor, "correo", longitud_maxima=self._MAX_CORREO)

        if not self._PATRON_CORREO.match(valor):
            self._registrar_error_cliente("El correo electronico no tiene un formato valido.")

        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._normalizar_texto(valor, "telefono", permitir_entero=True)

        if not valor.isdigit():
            self._registrar_error_cliente("El telefono debe contener solo numeros.")

        self._validar_longitud(
            valor,
            "telefono",
            self._MIN_TELEFONO,
            self._MAX_TELEFONO,
        )

        self._telefono = valor

    def actualizar_contacto(self, correo=None, telefono=None):
        self.actualizar_datos(correo=correo, telefono=telefono)

    def actualizar_datos(self, nombre=None, correo=None, telefono=None, activo=None):
        try:
            cambios = []

            if nombre is not None:
                self.nombre = nombre
                cambios.append("nombre")

            if correo is not None:
                self.correo = correo
                cambios.append("correo")

            if telefono is not None:
                self.telefono = telefono
                cambios.append("telefono")

            if activo is not None:
                self.activo = activo
                cambios.append("activo")

            if not cambios:
                self._registrar_error_cliente("Debe indicar al menos un dato para actualizar.")

            self.validar()
        except ErrorValidacion:
            raise
        except Exception as error:
            registrar_error(f"No fue posible actualizar el cliente: {error}")
            raise ErrorCliente(
                "No fue posible actualizar el cliente.",
                contexto={"documento": self.documento},
            ) from error
        else:
            registrar_info(
                f"Cliente actualizado: documento={self.documento}, "
                f"campos={', '.join(cambios)}"
            )

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

    def _normalizar_texto(self, valor, campo, permitir_entero=False):
        if valor is None:
            self._registrar_error_cliente(f"El campo {campo} es obligatorio.")

        if isinstance(valor, bool):
            self._registrar_error_cliente(f"El campo {campo} debe ser texto.")

        if permitir_entero and isinstance(valor, int):
            valor = str(valor)
        elif not isinstance(valor, str):
            self._registrar_error_cliente(f"El campo {campo} debe ser texto.")

        valor = valor.strip()
        if not valor:
            self._registrar_error_cliente(f"El campo {campo} no puede estar vacio.")

        return valor

    def _validar_longitud(
        self,
        valor,
        campo,
        longitud_minima=None,
        longitud_maxima=None,
    ):
        longitud = len(valor)

        if longitud_minima is not None and longitud < longitud_minima:
            self._registrar_error_cliente(
                f"El campo {campo} debe tener al menos {longitud_minima} caracteres."
            )

        if longitud_maxima is not None and longitud > longitud_maxima:
            self._registrar_error_cliente(
                f"El campo {campo} no puede superar {longitud_maxima} caracteres."
            )

    def _registrar_error_cliente(self, mensaje):
        registrar_error(f"Cliente: {mensaje}")
        raise ErrorValidacion(
            mensaje,
            contexto={"entidad": "Cliente", "documento": self._documento},
        )
