import unittest
from uuid import uuid4
from datetime import datetime
from decimal import Decimal
from domain.entities.transaction_type import TransactionType
from application.dtos.transaction_dto import TransactionDTO

class TestTransactionDTO(unittest.TestCase):
    # Definición de la clase de prueba que hereda de unittest.TestCase

    def test_inicializacion_atributos(self):
        # Método de prueba para la inicialización de atributos

        # Datos de prueba
        id = uuid4()  # Genera un UUID único para el id
        cuenta_id = uuid4()  # Genera un UUID único para cuenta_id
        monto = Decimal('1500.0')  # Asigna el valor 1500.0 al monto
        tipo = TransactionType.DEPOSITO  # Asigna la cadena "DEPOSITO" al tipo
        estado = "COMPLETADO"  # Asigna la cadena "COMPLETADO" al estado
        fecha = datetime(2024, 12, 15, 10, 30, 0)  # Asigna una fecha y hora específica a fecha

        # Crear instancia de TransaccionDTO
        transaccion = TransactionDTO(id, cuenta_id, monto, tipo, estado, fecha)
        # Crea una instancia de TransactionDTO con los datos de prueba

        # Verificar que los atributos se inicializan correctamente
        self.assertEqual(transaccion.id, id)  # Verifica que el id de la transacción es igual al id de prueba
        self.assertEqual(transaccion.cuenta_id, cuenta_id)  # Verifica que cuenta_id es igual al cuenta_id de prueba
        self.assertEqual(transaccion.monto, monto)  # Verifica que el monto es igual al monto de prueba
        self.assertEqual(transaccion.tipo, tipo)  # Verifica que el tipo es igual al tipo de prueba
        self.assertEqual(transaccion.estado, estado)  # Verifica que el estado es igual al estado de prueba
        self.assertEqual(transaccion.fecha, fecha)  # Verifica que la fecha es igual a la fecha de prueba

    def test_repr(self):
        # Arrange
        id = uuid4()
        cuenta_id = uuid4()
        monto = Decimal('100.00')
        tipo = TransactionType.DEPOSITO
        estado = 'PENDIENTE'
        fecha = datetime.now()

        transaccion = TransactionDTO(
            id=id,
            cuenta_id=cuenta_id,
            monto=monto,
            tipo=tipo,
            estado=estado,
            fecha=fecha
        )

        esperado = f"TransactionDTO(id={id}, cuenta_id={cuenta_id}, monto={monto}, tipo={tipo.name}, estado='{estado}', fecha='{fecha}')"

        # Act & Assert
        self.assertEqual(repr(transaccion), esperado)

if __name__ == "__main__":
    unittest.main()
