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