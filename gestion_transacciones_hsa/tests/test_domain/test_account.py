import unittest
from uuid import uuid4
from decimal import Decimal
from domain.entities.account import Account

class TestAccount(unittest.TestCase):
    def test_actualizar_saldo_incremento(self):
        """
        Prueba que actualizar_saldo incremente correctamente el saldo con un monto positivo (depósito).
        """
        usuario_id = uuid4()
        cuenta = Account(id=uuid4(), usuario_id=usuario_id, saldo=Decimal("100.00"), limite_diario=Decimal("1000.00"))
        
        cuenta.actualizar_saldo(Decimal("50.00"))  # Depósito
        self.assertEqual(cuenta.saldo, Decimal("150.00"), "El saldo no se incrementó correctamente.")

    def test_actualizar_saldo_decremento(self):
        """
        Prueba que actualizar_saldo decremente correctamente el saldo con un monto negativo (retiro).
        """
        usuario_id = uuid4()
        cuenta = Account(id=uuid4(), usuario_id=usuario_id, saldo=Decimal("200.00"), limite_diario=Decimal("1000.00"))
        
        cuenta.actualizar_saldo(Decimal("-50.00"))  # Retiro
        self.assertEqual(cuenta.saldo, Decimal("150.00"), "El saldo no se decrementó correctamente.")

    def test_actualizar_saldo_monto_cero(self):
        """
        Prueba que actualizar_saldo no afecta el saldo si el monto es cero.
        """
        usuario_id = uuid4()
        cuenta = Account(id=uuid4(), usuario_id=usuario_id, saldo=Decimal("200.00"), limite_diario=Decimal("1000.00"))
        
        cuenta.actualizar_saldo(Decimal("0.00"))  # Monto cero
        self.assertEqual(cuenta.saldo, Decimal("200.00"), "El saldo no debería cambiar con un monto cero.")
    def setUp(self):
        """
        Configuración inicial para las pruebas de Account.
        Crea una cuenta con un límite diario predefinido.
        """
        self.account = Account(
            id=uuid4(),
            usuario_id=uuid4(),
            saldo=Decimal("1000.00"),
            limite_diario=Decimal("500.00")
        )

        def test_monto_dentro_del_limite(self):
            """
            Prueba que no se lanza error cuando el monto está dentro del límite diario.
            """
        try:
            self.account.verificar_limite_diario(Decimal("400.00"))  # Dentro del límite
        except ValueError:
            self.fail("verificar_limite_diario lanzó un error para un monto dentro del límite.")

        def test_monto_excede_el_limite(self):
            """
            Prueba que se lanza ValueError cuando el monto excede el límite diario.
            """
        with self.assertRaises(ValueError) as context:
            self.account.verificar_limite_diario(Decimal("600.00"))  # Excede el límite
        self.assertEqual(str(context.exception), "El monto excede el límite diario permitido.")

        def test_monto_negativo_dentro_del_limite(self):
            """
            Prueba que no se lanza error cuando un monto negativo está dentro del límite diario.
            """
        try:
            self.account.verificar_limite_diario(Decimal("-400.00"))  # Dentro del límite
        except ValueError:
            self.fail("verificar_limite_diario lanzó un error para un monto negativo dentro del límite.")

        def test_monto_negativo_excede_el_limite(self):
            """
            Prueba que se lanza ValueError cuando un monto negativo excede el límite diario.
            """
        with self.assertRaises(ValueError) as context:
            self.account.verificar_limite_diario(Decimal("-600.00"))  # Excede el límite
        self.assertEqual(str(context.exception), "El monto excede el límite diario permitido.")
if __name__ == "__main__":
    unittest.main()
