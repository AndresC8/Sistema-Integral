

from exceptions.excepciones import ErrorServicio, ErrorValidacion
from models.servicio import Servicio
from utils.logger import registrar_error, registrar_info


class ReservaSala(Servicio):
    """
    Servicio para reservar salas de trabajo en Software FJ.
    El costo se calcula por hora según la capacidad de la sala.
    """

    RECARGO_CAPACIDAD_ALTA = 0.20  # 20% extra si capacidad > 10 personas

    def __init__(self, codigo, nombre, precio_base, capacidad, disponible=True):
        """
        - codigo: identificador único
        - nombre: nombre de la sala
        - precio_base: precio por hora
        - capacidad: número máximo de personas
        - disponible: si la sala está disponible
        """
        self._capacidad = None

        super().__init__(codigo, nombre, precio_base, disponible)

        self.capacidad = capacidad

        registrar_info(
            f"ReservaSala configurada: capacidad={capacidad} personas"
        )

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            registrar_error("ReservaSala: la capacidad debe ser un número entero.")
            raise ErrorServicio("La capacidad debe ser un número entero.")
        if valor <= 0:
            registrar_error("ReservaSala: la capacidad debe ser mayor que cero.")
            raise ErrorServicio("La capacidad debe ser mayor que cero.")
        self._capacidad = valor

    def validar_parametros(self, duracion):
        """Valida que la duración sea un número mayor que cero."""
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
            raise ErrorValidacion("La duración debe ser un número.")
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        return True

    def calcular_costo(self, duracion, con_descuento=False, con_impuesto=False):
        """
        Calcula el costo de reservar la sala.
        Si la capacidad es mayor a 10, aplica un recargo del 20%.
        Acepta parámetros opcionales de descuento e impuesto.
        """
        self._verificar_disponibilidad()
        self.validar_parametros(duracion)

        costo_base = self._precio_base * duracion

        # Recargo por capacidad alta
        if self._capacidad > 10:
            costo_base = costo_base * (1 + self.RECARGO_CAPACIDAD_ALTA)

        costo_final = self._calcular_con_opciones(
            costo_base,
            con_descuento=con_descuento,
            con_impuesto=con_impuesto
        )

        registrar_info(
            f"ReservaSala costo calculado: sala={self.nombre}, "
            f"duracion={duracion}h, costo=${costo_final:.2f}"
        )

        return costo_final

    def describir(self):
        """Retorna descripción de la sala."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Sala] {self.nombre} | "
            f"Capacidad: {self._capacidad} personas | "
            f"Precio/hora: ${self._precio_base:.2f} | "
            f"Estado: {estado}"
        )

    def validar(self):
        super().validar()
        if self._capacidad is None or self._capacidad <= 0:
            raise ErrorServicio("La capacidad de la sala no es válida.")
        return True