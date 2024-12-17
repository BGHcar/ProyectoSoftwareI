# domain/services/transaction_service.py 
from domain.repositories.i_transaction_repository import ITransactionRepository
from domain.repositories.i_account_repository import IAccountRepository
from domain.entities.transaction import Transaction
from domain.entities.account import Account
from decimal import Decimal

from domain.entities.transaction_type import TransactionType

from domain.entities.transaction_type import TransactionType

class TransactionService:
    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        account_repository: IAccountRepository
    ):
        self._transaction_repository = transaction_repository
        self._account_repository = account_repository

    def procesar_transaccion(self, transaccion: Transaction):
        """
        Procesa una transacción verificando los límites diarios, fondos suficientes y actualizando el saldo.
        """
        cuenta = self._account_repository.obtener_por_usuario(transaccion.cuenta_id)
        if cuenta is None:
            raise ValueError(f"La cuenta con ID {transaccion.cuenta_id} no existe.")

        if not isinstance(transaccion.monto, Decimal):
            raise ValueError("El monto debe ser de tipo Decimal.")
        # Validar la transacción antes de procesarla
        self.validar_transaccion(transaccion, cuenta)

        # Validar fondos insuficientes en retiros
        if transaccion.tipo == TransactionType.RETIRO:
            if cuenta.saldo + transaccion.monto < 0:  # Saldo insuficiente
                raise ValueError("Fondos insuficientes para realizar la transacción.")

        # Guardar la transacción y actualizar el saldo
        cuenta.actualizar_saldo(transaccion.monto)
        self._transaction_repository.guardar(transaccion)

    def validar_transaccion(self, transaccion: Transaction, cuenta: Account):
        """
        Valida una transacción verificando si cumple con los límites diarios.
        """
        cuenta.verificar_limite_diario(transaccion.monto)

    def listar_transacciones_por_cuenta(self, cuenta_id):
        """
        Retorna todas las transacciones asociadas a una cuenta específica.
        """
        return self._transaction_repository.listar_por_cuenta(cuenta_id)
