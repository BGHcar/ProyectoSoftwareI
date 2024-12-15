<<<<<<< HEAD
from abc import ABC, abstractmethod
from typing import List
from domain.models.account import Account

class IAccountRepository(ABC):
    """
    IAccountRepository: Abstracción para las operaciones de 
    persistencia relacionadas con las cuentas.
    """

    @abstractmethod
    def obtener_cuenta_por_id(self, cuenta_id: int) -> Account:
        pass

    @abstractmethod
    def obtener_todas_las_cuentas(self) -> List[Account]:
        pass

    @abstractmethod
    def crear_cuenta(self, cuenta: Account) -> None:
        pass

    @abstractmethod
    def actualizar_cuenta(self, cuenta: Account) -> None:
        pass

    @abstractmethod
    def eliminar_cuenta(self, cuenta_id: int) -> None:
        pass
=======
from uuid import UUID
from typing import List
from domain.entities.account import Account

class IAccountRepository:
    def obtener_por_id(self, id: UUID) -> Account:
        """
        Obtiene una cuenta por su ID.
        """
        pass

    def listar_todos(self) -> List[Account]:
        """
        Lista todas las cuentas.
        """
        pass

    def guardar(self, cuenta: Account):
        """
        Guarda una cuenta.
        """
        pass

    def eliminar(self, id: UUID):
        """
        Elimina una cuenta por su ID.
        """
        pass
>>>>>>> origin/bryan
