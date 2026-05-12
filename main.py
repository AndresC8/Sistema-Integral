from exceptions.excepciones import ErrorSistema
from models.cliente import Cliente
from models.servicios.reserva_sala import ReservaSala
from models.servicios.alquiler_equipo import AlquilerEquipo
from models.servicios.asesoria import Asesoria
from models.reserva import Reserva
from utils.logger import registrar_info, registrar_error


def ejecutar_operacion(nombre_operacion, operacion):
    """Ejecuta una funcion de forma segura, manejando errores de sistema y genericos."""
    print(f"\n--- {nombre_operacion} ---")

    try:
        # Intenta ejecutar la accion principal
        resultado = operacion()
    except ErrorSistema as error:
        # Maneja errores espesificos del negocio o sistema

        mensaje = f"Operacion controlada con error: {error}"
        print(mensaje)
        registrar_error(f"{nombre_operacion}: {error}")
        return None
    except Exception as error:
        # captura cualquier otro fallo inesperado
        mensaje = f"Error inesperado controlado: {error}"
        print(mensaje)
        registrar_error(f"{nombre_operacion}: {error}")
        return None
    else:
        # si no hubo errores, confirma el exito y retorna el dato
        print("Operacion exitosa.")
        registrar_info(f"{nombre_operacion}: operacion exitosa")
        return resultado
    finally:
        # Garantiza que este mensaje salga siempre
        print("La aplicacion continua en ejecucion.")


def simular_clientes():
    clientes = [] # base de datos temporal

    # caso 1: registro de cliente exitoso
    cliente_valido = ejecutar_operacion(
        "Registrar cliente valido",
        lambda: Cliente(
            documento="CC123456",
            nombre="Angela Fajardo",
            correo="angela.fajardo@softwarefj.com",
            telefono="3001234567",
        ),
    )
    # guarda el cliente si la operacion fue exitosa
    if cliente_valido is not None:
        clientes.append(cliente_valido)

    # caso 2: prueba de validacion de datos
    # Valida que el sistema bloquee registros sin numero de documento
    ejecutar_operacion(
        "Rechazar cliente con documento vacio",
        lambda: Cliente(
            documento="",
            nombre="Carlos Perez",
            correo="carlos.perez@softwarefj.com",
            telefono="3109876543",
        ),
    )

    # Valida la longitud minima del documento (caso de prueba: "A1")
    ejecutar_operacion(
        "Rechazar cliente con documento muy corto",
        lambda: Cliente(
            documento="A1",
            nombre="Laura Gomez",
            correo="laura.gomez@softwarefj.com",
            telefono="3112223344",
        ),
    )

    # Valida la longitud minima del nombre 
    ejecutar_operacion(
        "Rechazar cliente con nombre muy corto",
        lambda: Cliente(
            documento="CC445566",
            nombre="Lu",
            correo="lu.gomez@softwarefj.com",
            telefono="3112223344",
        ),
    )
 
    # Rechazar cliente con correo invalido
    ejecutar_operacion(
        "Rechazar cliente con correo invalido",
        lambda: Cliente(
            documento="CC778899",
            nombre="Mariana Torres",
            correo="mariana.torres",
            telefono="3205556677",
        ),
    )

    # Rechazar cliente con telefono no numerico
    ejecutar_operacion(
        "Rechazar cliente con telefono no numerico",
        lambda: Cliente(
            documento="CC998877",
            nombre="Pedro Ramirez",
            correo="pedro.ramirez@softwarefj.com",
            telefono="32055A6677",
        ),
    )

    ejecutar_operacion(
        "Rechazar cliente con telefono muy corto",
        lambda: Cliente(
            documento="CC112233",
            nombre="Sofia Mejia",
            correo="sofia.mejia@softwarefj.com",
            telefono="12345",
        ),
    )

    ejecutar_operacion(
        "Rechazar cliente con tipo incorrecto",
        lambda: Cliente(
            documento=True,
            nombre="Tipo Incorrecto",
            correo="tipo.incorrecto@softwarefj.com",
            telefono="3001112233",
        ),
    )

    if cliente_valido is not None:
        ejecutar_operacion(
            "Actualizar contacto valido",
            lambda: cliente_valido.actualizar_contacto(
                correo="angela.actualizada@softwarefj.com",
                telefono="3017654321",
            ),
        )

        ejecutar_operacion(
            "Rechazar actualizacion con telefono invalido",
            lambda: cliente_valido.actualizar_datos(telefono="telefono"),
        )

        print(f"\nClientes registrados correctamente: {len(clientes)}")
        for cliente in clientes:
            print(cliente.describir())
    return clientes

def simular_servicios():
    registrar_info("INICIO SIMULACION SERVICIOS")
    servicios = []

    # Caso 1: Crear sala valida
    s1 = ejecutar_operacion(
        "Crear sala de reuniones valida",
        lambda: ReservaSala("S01", "Sala Principal", 50000, 8),
    )
    if s1:
        servicios.append(s1)

    # Caso 2: Crear equipo valido
    s2 = ejecutar_operacion(
        "Crear equipo valido",
        lambda: AlquilerEquipo("E01", "Laptop Dell", 25000, "laptop"),
    )
    if s2:
        servicios.append(s2)

    # Caso 3: Crear asesoria valida
    s3 = ejecutar_operacion(
        "Crear asesoria experto valida",
        lambda: Asesoria("A01", "Asesoria Cloud", 80000, "experto"),
    )
    if s3:
        servicios.append(s3)

    # Caso 4: Rechazar servicio con precio negativo
    ejecutar_operacion(
        "Rechazar servicio con precio negativo",
        lambda: ReservaSala("S02", "Sala Invalida", -1000, 5),
    )

    # Caso 5: Rechazar asesoria con nivel invalido
    ejecutar_operacion(
        "Rechazar asesoria con nivel invalido",
        lambda: Asesoria("A02", "Asesoria Invalida", 50000, "dios"),
    )

    registrar_info("FIN SIMULACION SERVICIOS")
    return servicios

def simular_reservas(clientes, servicios):
    registrar_info("INICIO SIMULACION RESERVAS")

    if not clientes or not servicios:
        registrar_error("No hay clientes o servicios para simular reservas.")
        return

    cliente = clientes[0]
    sala = servicios[0]
    equipo = servicios[1]
    asesoria = servicios[2]

    # Caso 1: Reserva de sala exitosa con impuesto
    r1 = ejecutar_operacion(
        "Crear reserva de sala",
        lambda: Reserva("R001", cliente, sala, 2),
    )
    if r1:
        ejecutar_operacion(
            "Confirmar reserva de sala",
            lambda: r1.confirmar(),
        )
        ejecutar_operacion(
            "Procesar reserva con impuesto",
            lambda: r1.procesar(con_impuesto=True),
        )

    # Caso 2: Reserva de equipo con descuento
    r2 = ejecutar_operacion(
        "Crear reserva de equipo",
        lambda: Reserva("R002", cliente, equipo, 3),
    )
    if r2:
        ejecutar_operacion(
            "Confirmar reserva de equipo",
            lambda: r2.confirmar(),
        )
        ejecutar_operacion(
            "Procesar equipo con descuento",
            lambda: r2.procesar(con_descuento=True),
        )

    # Caso 3: Intentar cancelar reserva ya procesada 
    if r1:
        ejecutar_operacion(
            "Intentar cancelar reserva ya procesada",
            lambda: r1.cancelar(),
        )

    # Caso 4: Reserva cancelada antes de confirmar
    r3 = ejecutar_operacion(
        "Crear reserva de asesoria",
        lambda: Reserva("R003", cliente, asesoria, 1),
    )
    if r3:
        ejecutar_operacion(
            "Cancelar reserva de asesoria",
            lambda: r3.cancelar(),
        )
        ejecutar_operacion(
            "Intentar confirmar reserva cancelada",
            lambda: r3.confirmar(),
        )

    # Caso 5: Reserva con duracion invalid
    ejecutar_operacion(
        "Rechazar reserva con duracion negativa",
        lambda: Reserva("R004", cliente, sala, -5),
    )

    registrar_info("=== FIN SIMULACION RESERVAS ===")

if __name__ == "__main__":
    from models.servicios.reserva_sala import ReservaSala
    from models.servicios.alquiler_equipo import AlquilerEquipo
    from models.servicios.asesoria import Asesoria
    from models.reserva import Reserva

    registrar_info("INICIO DEL SISTEMA SOFTWARE FJ")
    clientes = simular_clientes()
    servicios = simular_servicios()
    simular_reservas(clientes, servicios)
    registrar_info("FIN DEL SISTEMA SOFTWARE FJ")
    print("\n✓ Simulacion completa. Revisa logs/sistema.log para el detalle.")