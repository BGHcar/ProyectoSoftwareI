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
from domain.entities.transaction_type import TransactionType

class TestTransactionApplicationService(unittest.TestCase):
    def setUp(self):
        self.transaction_service = Mock(spec=ITransactionService)
        self.account_repository = Mock()  # Quitamos el spec para permitir cualquier método
        self.service = TransactionApplicationService(
            self.transaction_service,
            self.account_repository
        )
        # Configurar métodos del mock
        self.transaction_service.listar_transacciones = Mock()
        self.transaction_service.procesar_transaccion = Mock()
        # Agregar el método que el servicio está usando
        self.account_repository.obtener_por_id = self.account_repository.obtener_por_usuario

    def test_realizar_transaccion_exitosa(self):
        # Arrange
        cuenta_id = uuid4()
        dto = TransactionDTO(
            id=uuid4(),
            cuenta_id=cuenta_id,
            monto=Decimal('100.00'),
            tipo=TransactionType.DEPOSITO,
            estado='PENDIENTE',
            fecha=datetime.now()
        )
        cuenta_mock = Mock()
        self.account_repository.obtener_por_usuario.return_value = cuenta_mock
        self.transaction_service.procesar_transaccion.return_value = dto

        # Act
        resultado = self.service.realizar_transaccion(dto)

        # Assert
        self.assertEqual(resultado, dto)
        self.account_repository.obtener_por_usuario.assert_called_once_with(cuenta_id)

    def test_realizar_transaccion_cuenta_no_existe(self):
        # Arrange
        cuenta_id = uuid4()
        dto = TransactionDTO(
            id=uuid4(),
            cuenta_id=cuenta_id,
            monto=Decimal('100.00'),
            tipo=TransactionType.DEPOSITO,
            estado='PENDIENTE',
            fecha=datetime.now()
        )
        self.account_repository.obtener_por_usuario.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError):
            self.service.realizar_transaccion(dto)

if __name__ == '__main__':
    unittest.main()
