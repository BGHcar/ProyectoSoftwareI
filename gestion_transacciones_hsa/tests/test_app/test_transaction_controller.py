import unittest
from unittest.mock import Mock
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from app.controllers.transaction_controller import realizar_transaccion, listar_transacciones, generar_informe_financiero, TransactionRequest
from application.dtos.transaction_dto import TransactionDTO
from application.dtos.informe_dto import InformeDTO
from domain.entities.transaction_type import TransactionType

class TestTransactionController(unittest.TestCase):
    def setUp(self):
        self.transaction_app_service = Mock()
        self.mongo_service = Mock()

    def test_realizar_transaccion(self):
        # Arrange
        cuenta_id = uuid4()
        transaction_request = TransactionRequest(
            cuenta_id=cuenta_id,
            monto=100.50,
            tipo="DEPOSITO",
            estado="PENDIENTE",
            fecha="2023-11-21"
        )

        # Act
        result = realizar_transaccion(
            transaction_request=transaction_request,
            transaction_app_service=self.transaction_app_service,
            mongo_service=self.mongo_service
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertIn("message", result)
        self.assertIn("transaction_id", result)
        self.transaction_app_service.realizar_transaccion.assert_called_once()

    def test_listar_transacciones(self):
        # Arrange
        cuenta_id = uuid4()
        mock_transactions = [
            TransactionDTO(
                id=uuid4(),
                cuenta_id=cuenta_id,
                monto=Decimal("100.00"),
                tipo=TransactionType.DEPOSITO,
                estado="APROBADA",
                fecha=datetime.now()
            )
        ]
        self.transaction_app_service.listar_transacciones.return_value = mock_transactions

        # Act
        result = listar_transacciones(
            cuenta_id=cuenta_id,
            transaction_app_service=self.transaction_app_service
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.transaction_app_service.listar_transacciones.assert_called_once_with(cuenta_id)

    def test_generar_informe_financiero(self):
        # Arrange
        cuenta_id = uuid4()
        mock_informe = InformeDTO(
            total_depositos=Decimal("1000.00"),
            total_retiros=Decimal("500.00"),
            saldo_promedio=Decimal("750.00"),
            transacciones=[]
        )
        self.transaction_app_service.generar_informe_financiero.return_value = mock_informe

        # Act
        result = generar_informe_financiero(
            cuenta_id=cuenta_id,
            transaction_app_service=self.transaction_app_service
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertIn("total_depositos", result)
        self.assertIn("total_retiros", result)
        self.assertIn("saldo_promedio", result)
        self.assertIn("transacciones", result)
        self.transaction_app_service.generar_informe_financiero.assert_called_once_with(cuenta_id)

if __name__ == '__main__':
    unittest.main()
