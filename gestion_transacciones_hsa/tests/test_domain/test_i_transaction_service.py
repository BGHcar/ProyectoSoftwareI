import unittest
from unittest.mock import Mock
from uuid import UUID, uuid4  # Importa UUID explícitamente
from datetime import datetime
from typing import List

from domain.entities.transaction import Transaction
from domain.entities.account import Account
from domain.repositories.i_transaction_service import ITransactionService

class TransactionServiceMock(ITransactionService):
    def procesar_transaccion(self, transaction: Transaction, account: Account) -> None:
        pass

    def listar_transacciones(self, cuenta_id: UUID) -> List[Transaction]:
        pass

class TestITransactionService(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.service = Mock(spec=TransactionServiceMock)
        
        # Crear datos de prueba
        self.cuenta_id = uuid4()
        self.cuenta = Account(
            id=self.cuenta_id,
            usuario_id=uuid4(),
            saldo=1000.0,
            limite_diario=5000.0  # Añadido el límite diario requerido
        )
        
        self.transaccion = Transaction(
            id=uuid4(),
            cuenta_id=self.cuenta_id,
            monto=500.0,
            tipo="deposito",
            estado="pendiente",
            fecha=datetime.now()
        )

    def test_procesar_transaccion(self):
        """Prueba el procesamiento de transacciones"""
        # Ejecutar
        self.service.procesar_transaccion(self.transaccion, self.cuenta)
        
        # Verificar
        self.service.procesar_transaccion.assert_called_once_with(
            self.transaccion, 
            self.cuenta
        )

    def test_listar_transacciones(self):
        """Prueba listar transacciones por cuenta"""
        # Configurar
        transacciones_esperadas = [self.transaccion]
        self.service.listar_transacciones.return_value = transacciones_esperadas
        
        # Ejecutar
        resultado = self.service.listar_transacciones(self.cuenta_id)
        
        # Verificar
        self.assertEqual(resultado, transacciones_esperadas)
        self.service.listar_transacciones.assert_called_once_with(self.cuenta_id)

if __name__ == '__main__':
    unittest.main()

