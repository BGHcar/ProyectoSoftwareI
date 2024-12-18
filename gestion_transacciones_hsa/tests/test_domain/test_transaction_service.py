import uuid
import unittest
from domain.entities.account import Account
from domain.entities.transaction import Transaction, TransactionState
from domain.services.transaction_service import TransactionService
from domain.entities.transaction_type import TransactionType
from decimal import Decimal


class FakeTransactionRepository:
    def __init__(self):
        self.transactions = []

    def guardar(self, transaction):
        self.transactions.append(transaction)

    def get_all_by_account_id(self, account_id):
        return [t for t in self.transactions if t.account_id == account_id]

    def get_by_id(self, cuenta_id):
        """Retorna una cuenta por ID o None si no existe."""
        return self.get_all_by_account_id(cuenta_id)


class FakeAccountRepository:
    def __init__(self):
        self.accounts = {}

    def save(self, account):
        self.accounts[account.id] = account

    def obtener_por_id(self, account_id):
        return self.accounts.get(account_id)

    def get_by_id(self, cuenta_id):
        """Retorna una cuenta por ID o None si no existe."""
        return self.accounts.get(cuenta_id)


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        self.transaction_repo = FakeTransactionRepository()
        self.account_repo = FakeAccountRepository()
        self.transaction_service = TransactionService(self.transaction_repo, self.account_repo)

        valid_user_id = uuid.uuid4()
        valid_account_id = uuid.uuid4()
        
        account = Account(valid_account_id, valid_user_id, Decimal(500.0), Decimal(1000.0))
        self.account_repo.save(account)
        self.valid_account_id = valid_account_id
        self.valid_user_id = valid_user_id

    def test_deposit(self):
        transaction = Transaction("tx123", self.valid_account_id, Decimal(100.0), TransactionType.DEPOSITO, TransactionState.PENDIENTE)
        self.transaction_service.procesar_transaccion(transaction)

        account = self.account_repo.obtener_por_id(self.valid_account_id)
        self.assertEqual(account.saldo, 600.0)

    def test_deposito_con_monto_invalido(self):
        """
        Prueba que procesar_transaccion lanza un ValueError si el monto no es Decimal.
        """
        transaction = Transaction("tx124", self.valid_account_id, "100", TransactionType.DEPOSITO, TransactionState.PENDIENTE)
        with self.assertRaises(ValueError) as context:
            self.transaction_service.procesar_transaccion(transaction)
        self.assertEqual(str(context.exception), "El monto debe ser de tipo Decimal.")

    def test_limite_diario_excedido(self):
        """
        Prueba que no se permita un depósito si supera el límite diario.
        """
        transaction = Transaction("tx125", self.valid_account_id, Decimal(1500.0), TransactionType.DEPOSITO, TransactionState.PENDIENTE)
        with self.assertRaises(ValueError) as context:
            self.transaction_service.procesar_transaccion(transaction)
        self.assertEqual(str(context.exception), "El monto excede el límite diario permitido.")

    def test_retiro_exitoso(self):
        """
        Prueba que un retiro exitoso disminuye correctamente el saldo.
        """
        transaction = Transaction("tx126", self.valid_account_id, Decimal(-200.0), TransactionType.RETIRO, TransactionState.PENDIENTE)
        self.transaction_service.procesar_transaccion(transaction)

        account = self.account_repo.obtener_por_id(self.valid_account_id)
        self.assertEqual(account.saldo, 300.0)

    def test_retiro_con_fondos_insuficientes(self):
        """
        Prueba que un retiro mayor al saldo lanza un error de fondos insuficientes.
        """
        transaction = Transaction("tx127", self.valid_account_id, Decimal(-600.0), TransactionType.RETIRO, TransactionState.PENDIENTE)
        with self.assertRaises(ValueError) as context:
            self.transaction_service.procesar_transaccion(transaction)
        self.assertEqual(str(context.exception), "Fondos insuficientes para realizar la transacción.")

    def test_transaccion_con_cuenta_inexistente(self):
        """
        Prueba que procesar_transaccion lanza un error si la cuenta no existe.
        """
        invalid_account_id = uuid.uuid4()
        transaction = Transaction("tx128", invalid_account_id, Decimal(100.0), TransactionType.DEPOSITO, TransactionState.PENDIENTE)

        with self.assertRaises(ValueError) as context:
            self.transaction_service.procesar_transaccion(transaction)
        self.assertEqual(str(context.exception), f"La cuenta con ID {invalid_account_id} no existe.")


if __name__ == "__main__":
    unittest.main()
