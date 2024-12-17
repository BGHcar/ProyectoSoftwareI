# domain/services/transaction_service.py 
from gestion_transacciones_hsa.domain.repositories.i_transaction_repository import ITransactionRepository
from gestion_transacciones_hsa.domain.repositories.i_account_repository import IAccountRepository
from gestion_transacciones_hsa.domain.entities.transaction import Transaction
from gestion_transacciones_hsa.domain.entities.account import Account

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
        Procesa una transacción verificando los límites diarios y actualizando el saldo de la cuenta.
        """
        cuenta = self._account_repository.obtener_por_id(transaccion.cuenta_id)
        if cuenta is None:
            raise ValueError(f"La cuenta con ID {transaccion.cuenta_id} no existe.")

        # Validar la transacción antes de procesarla
        self.validar_transaccion(transaccion, cuenta)

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
        return self._transaction_repository.obtener_por_cuenta(cuenta_id)

