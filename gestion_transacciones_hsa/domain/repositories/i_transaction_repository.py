from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from abc import ABC, abstractmethod
from ..entities.transaction import Transaction
from ..repositories.i_repository import IRepository
from ..entities.transaction import Transaction

class ITransactionRepository(IRepository[Transaction]):
    """
    Interfaz específica para el repositorio de transacciones.
    """
    
    def get_by_account(self, account_id: UUID) -> List[Transaction]:
        """
        Lista todas las transacciones de una cuenta específica.
        
        Args:
            account_id: UUID de la cuenta
            
        Returns:
            List[Transaction]: Lista de transacciones de la cuenta
        """
        pass

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
