# domain/services/transaction_service.py 
from domain.repositories.i_transaction_repository import ITransactionRepository
from domain.repositories.i_account_repository import IAccountRepository
from domain.entities.transaction import Transaction, TransactionState
from domain.entities.account import Account
from decimal import Decimal
from application.dtos.transaction_dto import TransactionDTO
import logging

from domain.entities.transaction_type import TransactionType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TransactionService:
    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        account_repository: IAccountRepository
    ):
        self._transaction_repository = transaction_repository
        self._account_repository = account_repository
        logger.debug(f"TransactionService inicializado con repositorio: {transaction_repository.__class__.__name__}")

    def procesar_transaccion(self, transaccion: Transaction) -> None:
        """
        Procesa y guarda una transacción en el repositorio correspondiente.
        """
        try:
            logger.debug(f"Procesando transacción en {self._transaction_repository.__class__.__name__}")
            logger.debug(f"Detalles de la transacción: {transaccion}")
            
            # Guardar la transacción
            self._transaction_repository.guardar(transaccion)
            logger.debug("Transacción guardada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al procesar transacción: {str(e)}", exc_info=True)
            raise

    def procesar_transaccion(self, transaccion: Transaction):
        """
        Procesa una transacción verificando los límites diarios, fondos suficientes y actualizando el saldo.
        """
        cuenta = self._account_repository.obtener_por_id(transaccion.cuenta_id)
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

    def realizar_transaccion(self, transaccion: Transaction) -> None:
        # Guardar en SQLite
        self._transaction_repository.guardar(transaccion)
        
        # Guardar en MongoDB si está disponible
        if self.mongo_transaction_repository:
            try:
                self.mongo_transaction_repository.guardar(transaccion)
            except Exception as e:
                logging.error(f"Error al guardar en MongoDB: {e}")

    def validar_transaccion(self, transaccion: Transaction, cuenta: Account):
        """
        Valida una transacción verificando si cumple con los límites diarios.
        """
        cuenta.verificar_limite_diario(transaccion.monto)

    def listar_transacciones_por_cuenta(self, cuenta_id):
        """
        Retorna todas las transacciones asociadas a una cuenta específica.
        """
        try:
            logger.debug(f"Intentando listar transacciones para cuenta_id: {cuenta_id}")
            cuenta = self._account_repository.obtener_por_id(cuenta_id)
            if cuenta is None:
                logger.error(f"Cuenta no encontrada para ID: {cuenta_id}")
                raise ValueError(f"La cuenta con ID {cuenta_id} no existe.")
                
            transacciones = self._transaction_repository.listar_por_cuenta(cuenta_id)
            logger.debug(f"Transacciones encontradas: {len(transacciones)}")
            return transacciones
            
        except Exception as e:
            logger.error(f"Error al listar transacciones: {str(e)}", exc_info=True)
            raise
