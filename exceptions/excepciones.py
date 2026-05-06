class ErrorSistema(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class ErrorCliente(ErrorSistema):
    pass

class ErrorServicio(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass

class ErrorValidacio(ErrorSistema):
    pass

class ErrorOperacionNoPermitida(ErrorSistema):
    pass


