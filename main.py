from exceptions.excepciones import ErrorSistema
from models.cliente import Cliente
from utils.logger import registrar_error, registrar_info


def ejecutar_operacion(nombre_operacion, operacion):
    print(f"\n--- {nombre_operacion} ---")

    try:
        resultado = operacion()
    except ErrorSistema as error:
        mensaje = f"Operacion controlada con error: {error}"
        print(mensaje)
        registrar_error(f"{nombre_operacion}: {error}")
        return None
    except Exception as error:
        mensaje = f"Error inesperado controlado: {error}"
        print(mensaje)
        registrar_error(f"{nombre_operacion}: {error}")
        return None
    else:
        print("Operacion exitosa.")
        registrar_info(f"{nombre_operacion}: operacion exitosa")
        return resultado
    finally:
        print("La aplicacion continua en ejecucion.")


def simular_clientes():
    clientes = []

    cliente_valido = ejecutar_operacion(
        "Registrar cliente valido",
        lambda: Cliente(
            documento="CC123456",
            nombre="Angela Fajardo",
            correo="angela.fajardo@softwarefj.com",
            telefono="3001234567",
        ),
    )
    if cliente_valido is not None:
        clientes.append(cliente_valido)

    ejecutar_operacion(
        "Rechazar cliente con documento vacio",
        lambda: Cliente(
            documento="",
            nombre="Carlos Perez",
            correo="carlos.perez@softwarefj.com",
            telefono="3109876543",
        ),
    )

    ejecutar_operacion(
        "Rechazar cliente con documento muy corto",
        lambda: Cliente(
            documento="A1",
            nombre="Laura Gomez",
            correo="laura.gomez@softwarefj.com",
            telefono="3112223344",
        ),
    )

    ejecutar_operacion(
        "Rechazar cliente con nombre muy corto",
        lambda: Cliente(
            documento="CC445566",
            nombre="Lu",
            correo="lu.gomez@softwarefj.com",
            telefono="3112223344",
        ),
    )

    ejecutar_operacion(
        "Rechazar cliente con correo invalido",
        lambda: Cliente(
            documento="CC778899",
            nombre="Mariana Torres",
            correo="mariana.torres",
            telefono="3205556677",
        ),
    )

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
