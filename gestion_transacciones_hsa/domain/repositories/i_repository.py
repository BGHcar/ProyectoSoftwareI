from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, TypeVar, Generic

T = TypeVar('T')  # Tipo genérico para la entidad

class IRepository(ABC, Generic[T]):
    """
    Interfaz base para repositorios que define operaciones CRUD básicas
    """
    
    @abstractmethod
    def guardar(self, entidad: T) -> None:
        """
        Guarda una entidad en el repositorio
        Args:
            entidad: Objeto a guardar
        Returns:
            None
        """
        pass

    @abstractmethod
    def obtener_por_id(self, id: UUID) -> T:
        """
        Obtiene una entidad por su ID
        Args:
            id: UUID de la entidad
        Returns:
            Objeto encontrado
        Raises:
            EntityNotFoundException: Si no se encuentra la entidad
        """
        pass

    @abstractmethod
    def listar_todos(self) -> List[T]:
        """
        Lista todas las entidades del repositorio
        Returns:
            Lista de entidades
        """
        pass