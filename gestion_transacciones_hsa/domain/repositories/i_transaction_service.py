from uuid import UUID
from typing import List
from domain.entities.transaction import Transaction
from domain.entities.account import Account
from abc import ABC, abstractmethod  # Importar ABC para crear una clase abstracta
from application.dtos.transaction_dto import TransactionDTO
from application.dtos.informe_dto import InformeDTO


class ITransactionService(ABC):
    """
    Interfaz que define las operaciones relacionadas con las transacciones,
    permitiendo que la lógica de negocio sea accesible de manera abstracta.
    """

    @abstractmethod
    def procesar_transaccion(self, transaction: Transaction, account: Account) -> None:
        """
        Procesa una transacción, realizando las validaciones y operaciones necesarias.
        Args:
            transaction (Transaction): La transacción a procesar.
            account (Account): La cuenta asociada a la transacción.
        """
        pass

    @abstractmethod
    def listar_transacciones(self, cuenta_id: UUID) -> List[Transaction]:
        """
        Lista todas las transacciones de una cuenta específica.
        Args:
            cuenta_id (UUID): El identificador de la cuenta.
        Returns:
            List[Transaction]: Lista de transacciones asociadas a la cuenta.
        """
        pass

    @abstractmethod
    def validar_transaccion(self, transaction: Transaction, account: Account) -> bool:
        """
        Valida una transacción verificando límites, saldo y restricciones.
        Args:
            transaction (Transaction): La transacción a validar.
            account (Account): La cuenta asociada a la transacción.
        Returns:
            bool: True si la transacción es válida, False de lo contrario.
        """
        pass

    @abstractmethod
    def obtener_balance_cuenta(self, cuenta_id: UUID) -> float:
        """
        Obtiene el balance actual de una cuenta.
        Args:
            cuenta_id (UUID): El identificador de la cuenta.
        Returns:
            float: El balance actual de la cuenta.
        """
        pass
