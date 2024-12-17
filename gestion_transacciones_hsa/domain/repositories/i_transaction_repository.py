from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from abc import ABC, abstractmethod
from gestion_transacciones_hsa.domain.entities.transaction import Transaction

class ITransactionRepository(ABC):
    """
    Abstracción para las operaciones de persistencia relacionadas con las transacciones.
    """

    @abstractmethod
    def listar_por_cuenta(self, cuenta_id: UUID) -> List[Transaction]:
        """
        Lista las transacciones asociadas a una cuenta por su ID.
        Args:
            cuenta_id (UUID): Identificador único de la cuenta.
        Returns:
            List[Transaction]: Lista de transacciones asociadas.
        """
        pass
    @abstractmethod
    def save(self, transaction: 'Transaction'):
            pass

    @abstractmethod
    def get_by_id(self, transaction_id: str):
            pass
