import unittest
from unittest.mock import Mock
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal
from application.services.transaction_application_service import TransactionApplicationService
from application.dtos.transaction_dto import TransactionDTO
from application.dtos.informe_dto import InformeDTO
from domain.repositories.i_transaction_service import ITransactionService
from domain.repositories.i_account_repository import IAccountRepository

class TestTransactionApplicationService(unittest.TestCase):
    def setUp(self):
        self.transaction_service = Mock(spec=ITransactionService)
        self.account_repository = Mock(spec=IAccountRepository)
        self.service = TransactionApplicationService(
            self.transaction_service,
            self.account_repository
        )
        # Asegurar que el método existe en el mock
        self.transaction_service.generar_informe_financiero = Mock()
        # Agregar el método realizar_transaccion al mock
        self.transaction_service.realizar_transaccion = Mock(return_value="Transacción exitosa")

    def test_realizar_transaccion_exitosa(self):
        # Arrange
        dto = TransactionDTO(
            id=uuid4(),
            cuenta_id=uuid4(),
            monto=Decimal('100.0'),
            tipo="TRANSFERENCIA",
            estado="PENDIENTE",
            fecha=datetime.now()
        )
        self.account_repository.obtener_por_usuario.return_value = Mock()
        self.transaction_service.realizar_transaccion.return_value = "Transacción exitosa"

        # Act
        resultado = self.service.realizar_transaccion(dto)

        # Assert
        self.assertEqual(resultado, "Transacción exitosa")
        self.account_repository.obtener_por_usuario.assert_called_once_with(dto.cuenta_id)
        self.transaction_service.realizar_transaccion.assert_called_once_with(dto)

    def test_realizar_transaccion_cuenta_no_existe(self):
        # Arrange
        dto = TransactionDTO(
            id=uuid4(),
            cuenta_id=uuid4(),
            monto=Decimal('100.0'),
            tipo="TRANSFERENCIA",
            estado="PENDIENTE",
            fecha=datetime.now()
        )
        self.account_repository.obtener_por_usuario.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.realizar_transaccion(dto)
        self.assertEqual(str(context.exception), "La cuenta no existe")

    def test_listar_transacciones_exitoso(self):
        # Arrange
        cuenta_id = uuid4()
        transacciones_mock = [Mock(), Mock()]
        self.account_repository.obtener_por_usuario.return_value = Mock()
        self.transaction_service.listar_transacciones.return_value = transacciones_mock

        # Act
        resultado = self.service.listar_transacciones(cuenta_id)

        # Assert
        self.assertEqual(resultado, transacciones_mock)
        self.account_repository.obtener_por_usuario.assert_called_once_with(cuenta_id)
        self.transaction_service.listar_transacciones.assert_called_once_with(cuenta_id)

    def test_listar_transacciones_cuenta_no_existe(self):
        # Arrange
        cuenta_id = uuid4()
        self.account_repository.obtener_por_usuario.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.listar_transacciones(cuenta_id)
        self.assertEqual(str(context.exception), "La cuenta no existe")

    def test_generar_informe_financiero_exitoso(self):
        # Arrange
        cuenta_id = uuid4()
        self.account_repository.obtener_por_usuario.return_value = Mock()
        transacciones_mock = [
            Mock(monto=Decimal('100.0'), tipo='DEPOSITO'),
            Mock(monto=Decimal('50.0'), tipo='RETIRO')
        ]
        self.transaction_service.listar_transacciones.return_value = transacciones_mock

        # Act
        resultado = self.service.generar_informe_financiero(cuenta_id)

        # Assert
        self.assertIsInstance(resultado, InformeDTO)
        self.account_repository.obtener_por_usuario.assert_called_once_with(cuenta_id)
        self.transaction_service.listar_transacciones.assert_called_once_with(cuenta_id)

    def test_generar_informe_financiero_cuenta_no_existe(self):
        # Arrange
        cuenta_id = uuid4()
        self.account_repository.obtener_por_usuario.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.service.generar_informe_financiero(cuenta_id)
        self.assertEqual(str(context.exception), "La cuenta no existe")

if __name__ == '__main__':
    unittest.main()
