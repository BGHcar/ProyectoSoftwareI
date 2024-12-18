import unittest
from unittest.mock import Mock
from decimal import Decimal
from app.controllers.account_controller import crear_cuenta

class TestAccountController(unittest.TestCase):
    def setUp(self):
        self.sqlite_repository = Mock()
        self.mongo_repository = Mock()

    def test_crear_cuenta(self):
        # Arrange
        cuenta_data = {
            "saldo": 1000.00,
            "limite_diario": 2000.00
        }

        # Act
        result = crear_cuenta(
            cuenta_json=cuenta_data,
            sqlite_repository=self.sqlite_repository,
            mongo_repository=self.mongo_repository
        )

        # Assert
        self.assertIsNotNone(result)
        self.assertIn("cuenta_id", result)
        self.assertIn("usuario_id", result)
        self.assertIn("message", result)
        self.sqlite_repository.guardar.assert_called_once()
        self.mongo_repository.guardar.assert_called_once()

if __name__ == '__main__':
    unittest.main()
