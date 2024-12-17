# domain/entities/transaction.py
from uuid import UUID
from datetime import datetime
from gestion_transacciones_hsa.domain.entities.transaction_type import TransactionType
from enum import Enum
from decimal import Decimal

class TransactionState(Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"

class Transaction:
    def __init__(
        self,
        id: UUID,
        cuenta_id: UUID,
        monto: Decimal,
        tipo: TransactionType,
        estado: TransactionState = TransactionState.PENDIENTE,
        fecha: datetime = None
    ):
        self.id = id
        self.cuenta_id = cuenta_id
        self.monto = monto
        self.tipo = tipo
        self.estado = estado
        self.fecha = fecha or datetime.now()  # Si no se proporciona, asigna la fecha actual.
        
    def validar(self):  # Valida que los atributos de la transacción sean válidos
        if self.monto <= 0:
            raise ValueError("El monto de la transacción debe ser mayor a 0.")
        if self.estado not in TransactionState:
            raise ValueError(f"El estado de la transacción debe ser uno de {list(TransactionState)}.")
        if not isinstance(self.tipo, TransactionType):
            raise ValueError("El tipo de transacción no es válido.")
        
    def confirmar(self):  # Confirma la transacción
        if self.estado != TransactionState.PENDIENTE:
            raise ValueError("Solo puedes confirmar transacciones en estado pendiente.")
        self.estado = TransactionState.APROBADA
        
    def cancelar(self):  # Cancela la transacción
        if self.estado != TransactionState.PENDIENTE:
            raise ValueError("Solo puedes cancelar transacciones en estado pendiente.")
        self.estado = TransactionState.RECHAZADA
