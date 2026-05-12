#--- Prueba Unitaria: GESTION DE RESERVAS ---
# Este script valida el flujo principal de creacion y procesamiento de una reserva 
from models.servicios.reserva_sala import ReservaSala
from models.cliente import Cliente
from models.reserva import Reserva

# 1. Definicion de datos de prueba
# Se crea una sala disponible con ID, Nombre, precio y capacidad
sala = ReservaSala('S01', 'Sala Principal', 50000, 8)
# Se registran los datos basicos del cliente
cliente = Cliente('CC123456', 'Angela Fajardo', 'angela@softwarefj.com','3001234567')
# 2. creacion de la reserva
# Se asocia el codigo R001 al cliente y la sala para 2 personas
r = Reserva('R001', cliente, sala, 2)
# 3. procesamiento y salida
r.confirmar()          # Cambia el estado de la reserva 
costo = r.procesar()   # calcula el valor total segun la logica de negocio
print(f'Costo: {costo}')