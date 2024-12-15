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
