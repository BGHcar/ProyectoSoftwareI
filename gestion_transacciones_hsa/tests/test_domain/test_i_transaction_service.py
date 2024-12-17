import unittest
from unittest.mock import Mock
from uuid import UUID, uuid4  # Importa UUID explícitamente
from datetime import datetime
from typing import List

from gestion_transacciones_hsa.domain.entities.transaction import Transaction
from gestion_transacciones_hsa.domain.entities.account import Account
from gestion_transacciones_hsa.domain.repositories.i_transaction_service import ITransactionService

class TransactionServiceMock(ITransactionService):
    def procesar_transacciones(self, transaction: Transaction, account: Account) -> None:
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
            estado="activa"
        )
        
        self.transaccion = Transaction(
            id=uuid4(),
            cuenta_id=self.cuenta_id,
            monto=500.0,
            tipo="depósito",
            fecha=datetime.now()
        )

    def test_procesar_transacciones(self):
        """Prueba el procesamiento de transacciones"""
        # Ejecutar
        self.service.procesar_transacciones(self.transaccion, self.cuenta)
        
        # Verificar
        self.service.procesar_transacciones.assert_called_once_with(
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
