from exceptions.excepciones import ErrorSistema
from models.cliente import Cliente
from utils.logger import registrar_error, registrar_info


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

    # Valida la longitud minima del nombre (caso de prueba: "Lu")
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


if __name__ == "__main__":
    registrar_info("Inicio de simulacion de clientes Software FJ")
    simular_clientes()
    registrar_info("Fin de simulacion de clientes Software FJ")
