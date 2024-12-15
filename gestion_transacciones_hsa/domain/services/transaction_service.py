from abc import ABC, abstractmethod
from typing import List
from domain.models.transaction import Transaction

class IServicioTransacciones(ABC):

    @abstractmethod
    def crear_transaccion(self, transaccion: Transaction) -> Transaction:
        pass

    @abstractmethod
    def obtener_transaccion(self, id_transaccion: int) -> Transaction:
        pass

    @abstractmethod
    def actualizar_transaccion(self, transaccion: Transaction) -> Transaction:
        pass

    @abstractmethod
    def eliminar_transaccion(self, id_transaccion: int) -> None:
        pass

    @abstractmethod
    def listar_transacciones(self) -> List[Transaction]:
        pass