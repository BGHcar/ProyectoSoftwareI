import unittest
from unittest.mock import Mock
from uuid import UUID, uuid4
from typing import List
from gestion_transacciones_hsa.domain.repositories.i_transaction_repository import ITransactionRepository
from gestion_transacciones_hsa.domain.entities.transaction import Transaction


class TransactionRepositoryMock(ITransactionRepository):
    """Mock del repositorio de transacciones para pruebas"""
    def listar_por_cuenta(self, cuenta_id: UUID) -> List[Transaction]:
        pass

class TestITransactionRepository(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.repositorio = Mock(spec=TransactionRepositoryMock)
        self.cuenta_id = uuid4()
        # Crear transacción de prueba
        self.transaccion = Transaction(
            id=uuid4(),
            cuenta_id=self.cuenta_id,
            monto=1000.0,
            tipo="depósito",
            fecha="2024-03-15"
        )

    def test_listar_por_cuenta(self):
        """Prueba listar transacciones por cuenta"""
        # Configurar mock
        transacciones_esperadas = [self.transaccion]
        self.repositorio.listar_por_cuenta.return_value = transacciones_esperadas

        # Ejecutar
        resultado = self.repositorio.listar_por_cuenta(self.cuenta_id)

        # Verificar
        self.assertEqual(resultado, transacciones_esperadas)
        self.repositorio.listar_por_cuenta.assert_called_once_with(self.cuenta_id)

if __name__ == '__main__':
    unittest.main()