from uuid import UUID
from typing import List

from gestion_transacciones_hsa.domain.entities.account import Account
from gestion_transacciones_hsa.domain.repositories.i_repository import IRepository


class IAccountRepository(IRepository[Account]):
    """
    Interfaz para el repositorio de cuentas
    """
    
    
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

    def obtener_por_usuario(self, usuario_id: UUID) -> List[Account]:
        """
        Obtiene todas las cuentas asociadas a un usuario
        
        Args:
            usuario_id: UUID del usuario
            
        Returns:
            List[Account]: Lista de cuentas del usuario
            
        Raises:
            EntityNotFoundException: Si no se encuentran cuentas
        """
        pass
