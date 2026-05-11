

from exceptions.excepciones import ErrorServicio, ErrorValidacion
from models.servicio import Servicio
from utils.logger import registrar_error, registrar_info


class AlquilerEquipo(Servicio):
    """
    Servicio para alquilar equipos tecnológicos en Software FJ.
    El costo se calcula por hora según la cantidad de equipos.
    """

    RECARGO_MULTIPLE = 0.15  # 15% extra si se alquilan más de 3 equipos

    def __init__(self, codigo, nombre, precio_base, tipo_equipo, disponible=True):
        """
        - codigo: identificador único
        - nombre: nombre del equipo
        - precio_base: precio por hora
        - tipo_equipo: descripción del tipo (ej: 'laptop', 'proyector')
        - disponible: si el equipo está disponible
        """
        self._tipo_equipo = None

        super().__init__(codigo, nombre, precio_base, disponible)

        self.tipo_equipo = tipo_equipo

        registrar_info(
            f"AlquilerEquipo configurado: tipo={tipo_equipo}"
        )

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            registrar_error("AlquilerEquipo: el tipo de equipo debe ser texto no vacío.")
            raise ErrorServicio("El tipo de equipo debe ser texto no vacío.")
        self._tipo_equipo = valor.strip()

    def validar_parametros(self, duracion, cantidad=1):
        """Valida duración y cantidad de equipos."""
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
            raise ErrorValidacion("La duración debe ser un número.")
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise ErrorValidacion("La cantidad de equipos debe ser un número entero.")
        if cantidad <= 0:
            raise ErrorValidacion("La cantidad de equipos debe ser mayor que cero.")
        return True

    def calcular_costo(self, duracion, cantidad=1, con_descuento=False, con_impuesto=False):
        """
        Calcula el costo del alquiler.
        Si se alquilan más de 3 equipos aplica recargo del 15%.
        Acepta parámetros opcionales de descuento e impuesto.
        """
        self._verificar_disponibilidad()
        self.validar_parametros(duracion, cantidad)

        costo_base = self._precio_base * duracion * cantidad

        # Recargo por múltiples equipos
        if cantidad > 3:
            costo_base = costo_base * (1 + self.RECARGO_MULTIPLE)

        costo_final = self._calcular_con_opciones(
            costo_base,
            con_descuento=con_descuento,
            con_impuesto=con_impuesto
        )

        registrar_info(
            f"AlquilerEquipo costo calculado: equipo={self.nombre}, "
            f"cantidad={cantidad}, duracion={duracion}h, costo=${costo_final:.2f}"
        )

        return costo_final

    def describir(self):
        """Retorna descripción del equipo."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Equipo] {self.nombre} | "
            f"Tipo: {self._tipo_equipo} | "
            f"Precio/hora: ${self._precio_base:.2f} | "
            f"Estado: {estado}"
        )

    def validar(self):
        super().validar()
        if not self._tipo_equipo:
            raise ErrorServicio("El tipo de equipo no es válido.")
        return True