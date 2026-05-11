from models.servicios.reserva_sala import ReservaSala
from models.cliente import Cliente
from models.reserva import Reserva

sala = ReservaSala('S01', 'Sala Principal', 50000, 8)
cliente = Cliente('CC123456', 'Angela Fajardo', 'angela@softwarefj.com', '3001234567')
r = Reserva('R001', cliente, sala, 2)
r.confirmar()
costo = r.procesar()
print(f'Costo: {costo}')