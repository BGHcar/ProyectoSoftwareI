# domain/entities/transaction.py
from uuid import UUID
from datetime import datetime
from domain.entities.transaction_type import TransactionType
from enum import Enum
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TransactionState(Enum):
    PENDIENTE = "PENDIENTE"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"

    @classmethod
    def from_string(cls, value: str) -> 'TransactionState':
        """Convierte un string a TransactionState de manera segura"""
        try:
            return cls(value.upper())
        except ValueError:
            estados_validos = [e.value for e in cls]
            raise ValueError(f"Estado inválido '{value}'. Estados válidos: {estados_validos}")

    def __str__(self):
        return self.value

class Transaction:
    def __init__(
        self,
        id: UUID,
        cuenta_id: UUID,
        monto: Decimal,
        tipo: TransactionType,
        estado: str | TransactionState,
        fecha: datetime = None
    ):
        logger.debug(f"Creando nueva transacción - ID: {id}, Tipo: {tipo}, Estado: {estado}")
        self.id = id
        self.cuenta_id = cuenta_id
        self.monto = monto
        logger.debug(f"Procesando tipo de transacción: {tipo}, Tipo de dato: {type(tipo)}")
        self.tipo = tipo if isinstance(tipo, TransactionType) else TransactionType.from_string(tipo)
        logger.debug(f"Procesando estado de transacción: {estado}")
        self.estado = estado if isinstance(estado, TransactionState) else TransactionState.from_string(estado)
        self.fecha = fecha or datetime.now()  # Si no se proporciona, asigna la fecha actual.
        logger.debug(f"Transacción creada exitosamente con estado: {self.estado}")
        
    def validar(self):  # Valida que los atributos de la transacción sean válidos
        logger.debug(f"Validando transacción {self.id}")
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