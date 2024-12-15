<<<<<<< HEAD
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
=======
# domain/entities/transaction_type.py

from enum import Enum

class TransactionType(Enum):
    DEPOSITO = "deposito"
    RETIRO = "retiro"

    @property
    def descripcion(self) -> str:
        descripciones = {
            "deposito": "Agrega dinero a la cuenta HSA del usuario.",
            "retiro": "Reduce el saldo de la cuenta HSA del usuario dentro de los límites establecidos."
        }
        return descripciones[self.value]

    @property
    def nombre(self) -> str:
        return self.value

>>>>>>> origin/bryan
