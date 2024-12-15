from enum import Enum
from datetime import datetime

class EstadoTransaccion(Enum):
    VALIDADO = "validado"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"

class TipoTransaccion(Enum):
    DEPOSITO = "deposito"
    RETIRO = "retiro"

class Transaccion:
    def __init__(self, id_transaccion: int, tipo_transaccion: TipoTransaccion, monto: float, estado: EstadoTransaccion, fecha: datetime):
        self.id_transaccion = id_transaccion
        self.tipo_transaccion = tipo_transaccion
        self.monto = monto
        self.estado = estado
        self.fecha = fecha

    def validar(self):
        self.estado = EstadoTransaccion.VALIDADO

    def confirmar(self):
        self.estado = EstadoTransaccion.CONFIRMADO

    def cancelar(self):
        self.estado = EstadoTransaccion.CANCELADO
