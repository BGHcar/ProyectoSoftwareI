from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from domain.entities.transaction import Transaction

class ITransactionRepository:
    def listar_por_cuenta(self, cuenta_id: UUID) -> List[Transaction]:
        """
        Lista las transacciones asociadas a una cuenta por su ID.
        """
        pass
    @abstractmethod
    def save(self, transaction: 'Transaction'):
            pass

    @abstractmethod
    def get_by_id(self, transaction_id: str):
            pass
