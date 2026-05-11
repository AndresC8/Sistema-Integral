

from exceptions.excepciones import ErrorServicio, ErrorValidacion
from models.servicio import Servicio
from utils.logger import registrar_error, registrar_info


class Asesoria(Servicio):
    """
    Servicio de asesoría especializada en Software FJ.
    El costo varía según el nivel de especialización del asesor.
    """

    NIVELES_VALIDOS = ("junior", "senior", "experto")
    RECARGO_SENIOR = 0.25    # 25% extra para nivel senior
    RECARGO_EXPERTO = 0.50   # 50% extra para nivel experto

    def __init__(self, codigo, nombre, precio_base, nivel, disponible=True):
        """
        - codigo: identificador único
        - nombre: nombre de la asesoría
        - precio_base: precio base por hora
        - nivel: nivel del asesor ('junior', 'senior', 'experto')
        - disponible: si la asesoría está disponible
        """
        self._nivel = None

        super().__init__(codigo, nombre, precio_base, disponible)

        self.nivel = nivel

        registrar_info(
            f"Asesoria configurada: nivel={nivel}"
        )

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            registrar_error("Asesoria: el nivel debe ser texto no vacío.")
            raise ErrorServicio("El nivel de asesoría debe ser texto.")
        valor = valor.strip().lower()
        if valor not in self.NIVELES_VALIDOS:
            registrar_error(f"Asesoria: nivel '{valor}' no válido.")
            raise ErrorServicio(
                f"Nivel inválido. Los niveles válidos son: {', '.join(self.NIVELES_VALIDOS)}."
            )
        self._nivel = valor

    def validar_parametros(self, duracion):
        """Valida que la duración sea un número mayor que cero."""
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
            raise ErrorValidacion("La duracin debe ser un número")
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        return True

    def calcular_costo(self, duracion, con_descuento=False, con_impuesto=False):
        """
        Calcula el costo de la asesoría según el nivel del asesor.
        - Junior: precio base
        - Senior: +25%
        - Experto: +50%
        Acepta parámetros opcionales de descuento e impuesto.
        """
        self._verificar_disponibilidad()
        self.validar_parametros(duracion)

        costo_base = self._precio_base * duracion

        # Recargo según nivel
        if self._nivel == "senior":
            costo_base = costo_base * (1 + self.RECARGO_SENIOR)
        elif self._nivel == "experto":
            costo_base = costo_base * (1 + self.RECARGO_EXPERTO)

        costo_final = self._calcular_con_opciones(
            costo_base,
            con_descuento=con_descuento,
            con_impuesto=con_impuesto
        )

        registrar_info(
            f"Asesoria costo calculado: asesoria={self.nombre}, "
            f"nivel={self._nivel}, duracion={duracion}h, costo=${costo_final:.2f}"
        )

        return costo_final

    def describir(self):
        """Retorna descripción de la asesoría."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Asesoría] {self.nombre} | "
            f"Nivel: {self._nivel} | "
            f"Precio/hora: ${self._precio_base:.2f} | "
            f"Estado: {estado}"
        )

    def validar(self):
        super().validar()
        if self._nivel not in self.NIVELES_VALIDOS:
            raise ErrorServicio("El nivel de asesoría no es válido")
        return True