from uuid import UUID
from datetime import datetime
from decimal import Decimal
from domain.entities.transaction_type import TransactionType
from domain.entities.transaction import Transaction, TransactionState
import logging

logger = logging.getLogger(__name__)

class TransactionDTO:
    def __init__(self, id: UUID, cuenta_id: UUID, monto: Decimal, tipo: TransactionType, estado: TransactionState, fecha: datetime):
        self.id = id
        self.cuenta_id = cuenta_id
        self.monto = monto
        self.tipo = tipo
        self.estado = str(estado)  # Convertir TransactionState a string
        self.fecha = fecha

    @staticmethod
    def from_entity(entity: Transaction) -> 'TransactionDTO':
        """
        Convierte una entidad Transaction a TransactionDTO
        """
        try:
            if not entity:
                raise ValueError("No se puede convertir una entidad nula a DTO")
                
            return TransactionDTO(
                id=entity.id,
                cuenta_id=entity.cuenta_id,
                monto=entity.monto,
                tipo=entity.tipo,
                estado=entity.estado,  # Ya no necesitamos llamar .upper()
                fecha=entity.fecha
            )
        except Exception as e:
            logger.error(f"Error al convertir entidad a DTO: {str(e)}", exc_info=True)
            raise ValueError(f"Error en la conversión de entidad a DTO: {str(e)}")

    def __repr__(self):
        return f"TransactionDTO(id={self.id}, cuenta_id={self.cuenta_id}, monto={self.monto}, tipo={self.tipo}, estado='{self.estado}', fecha='{self.fecha}')"
