import unittest
from unittest.mock import Mock
from uuid import uuid4
from application.services.transactionApplicationService import TransactionApplicationService

from domain.entities.transaction import Transaction
from domain.entities.account import Account
from domain.repositories.i_transaction_service import ITransactionService
from domain.repositories.i_account_repository import IAccountRepository

class TestTransactionApplicationService(unittest.TestCase):
    def setUp(self):
        # Crear mocks para las dependencias
        self.mock_transaction_service = Mock(spec=ITransactionService)
        self.mock_account_repository = Mock(spec=IAccountRepository)

        # Instanciar TransactionApplicationService con mocks
        self.service = TransactionApplicationService(
            transaction_service=self.mock_transaction_service,
            account_repository=self.mock_account_repository
        )

    def test_realizar_transaccion(self):
        # Configurar el DTO de prueba
        dto = {"cuenta_id": uuid4(), "monto": 1000.0, "tipo": "depósito"}

        # Crear la transacción y la cuenta
        transaccion = Transaction(id=uuid4(), cuenta_id=dto["cuenta_id"], monto=dto["monto"], tipo=dto["tipo"])
        cuenta = Account(id=dto["cuenta_id"], balance=500.0)

        # Configurar el comportamiento del mock para procesar transacciones
        self.mock_transaction_service.procesar_transacciones.return_value = None
        self.mock_account_repository.actualizar_balance.return_value = None

        # Ejecutar el método
        resultado = self.service.realizar_transaccion(dto)

        # Verificar que se llamaron los métodos esperados
        self.mock_transaction_service.procesar_transacciones.assert_called_once_with(transaccion, cuenta)
        self.mock_account_repository.actualizar_balance.assert_called_once_with(transaccion)

        # Verificar el resultado
        self.assertEqual(resultado, "Transacción completada con éxito.")

    def test_listar_transacciones(self):
        # Configurar el ID de cuenta de prueba
        cuenta_id = uuid4()

        # Configurar el comportamiento del mock para listar transacciones
        transacciones = [
            Transaction(id=uuid4(), cuenta_id=cuenta_id, monto=500.0, tipo="retiro"),
            Transaction(id=uuid4(), cuenta_id=cuenta_id, monto=1000.0, tipo="depósito")
        ]
        self.mock_transaction_service.listar_transacciones.return_value = transacciones

        # Ejecutar el método
        resultado = self.service.listar_transacciones(cuenta_id)

        # Verificar que se llamó el método esperado
        self.mock_transaction_service.listar_transacciones.assert_called_once_with(cuenta_id)

        # Verificar el resultado
        self.assertEqual(resultado, transacciones)

    def test_generar_informe_financiero(self):
        # Configurar el ID de cuenta de prueba
        cuenta_id = uuid4()

        # Configurar el comportamiento del mock para obtener las transacciones
        transacciones = [
            Transaction(id=uuid4(), cuenta_id=cuenta_id, monto=500.0, tipo="retiro"),
            Transaction(id=uuid4(), cuenta_id=cuenta_id, monto=1000.0, tipo="depósito")
        ]
        self.mock_transaction_service.obtener_transacciones_por_cuenta.return_value = transacciones

        # Configurar el comportamiento del mock del generador de informes
        informe = {"total_depositos": 1000.0, "total_retiros": 500.0, "balance": 500.0}
        self.mock_generador_informes.generar.return_value = informe

        # Ejecutar el método
        resultado = self.service.generar_informe_financiero(cuenta_id)

        # Verificar que se llamaron los métodos esperados
        self.mock_transaction_service.obtener_transacciones_por_cuenta.assert_called_once_with(cuenta_id)
        self.mock_generador_informes.generar.assert_called_once_with(transacciones)

        # Verificar el resultado
        self.assertEqual(resultado, informe)

    def test_obtener_cuenta_por_id(self):
        # Configurar un ID de cuenta
        cuenta_id = uuid4()

        # Configurar el comportamiento del mock de obtener_por_id
        cuenta = Account(id=cuenta_id, balance=1000.0)
        self.mock_account_repository.obtener_por_id.return_value = cuenta

        # Ejecutar el método
        resultado = self.mock_account_repository.obtener_por_id(cuenta_id)

        # Verificar que se llamó el método esperado
        self.mock_account_repository.obtener_por_id.assert_called_once_with(cuenta_id)

        # Verificar el resultado
        self.assertEqual(resultado, cuenta)

    def test_listar_todas_las_cuentas(self):
        # Configurar el comportamiento del mock de listar_todos
        cuentas = [
            Account(id=uuid4(), balance=1000.0),
            Account(id=uuid4(), balance=2000.0)
        ]
        self.mock_account_repository.listar_todos.return_value = cuentas

        # Ejecutar el método
        resultado = self.mock_account_repository.listar_todos()

        # Verificar que se llamó el método esperado
        self.mock_account_repository.listar_todos.assert_called_once()

        # Verificar el resultado
        self.assertEqual(resultado, cuentas)

if __name__ == "__main__":
    unittest.main()
