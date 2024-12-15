<<<<<<< HEAD
from abc import ABC, abstractmethod
from typing import List
from domain.models.transaction import Transaction

class ITransactionRepository(ABC):
    """
    ITransactionRepository: Abstracción para las operaciones de 
    persistencia relacionadas con las transacciones.
    """

    @abstractmethod
    def obtener_transaccion_por_id(self, id_transaccion: int) -> Transaction:
        pass

    @abstractmethod
    def obtener_todas_las_transacciones(self) -> List[Transaction]:
        pass

    @abstractmethod
    def guardar_transaccion(self, transaccion: Transaction) -> None:
        pass

    @abstractmethod
    def eliminar_transaccion(self, id_transaccion: int) -> None:
        pass
=======
from uuid import UUID
from typing import List
from domain.entities.transaction import Transaction

class ITransactionRepository:
    def listar_por_cuenta(self, cuenta_id: UUID) -> List[Transaction]:
        """
        Lista las transacciones asociadas a una cuenta por su ID.
        """
        pass
>>>>>>> origin/bryan
