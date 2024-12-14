# tests/test_infrastructure/test_sqlite_transaction_repository.py
import unittest  # Importa el módulo de pruebas unitarias
import sqlite3   # Importa el módulo para trabajar con SQLite
from decimal import Decimal  # Para manejar números decimales con precisión
from datetime import datetime  # Para manejar fechas y tiempos
from uuid import UUID, uuid4  # Para generar identificadores únicos
from infrastructure.repositories.sqlite_transaction_repository import SQLiteTransactionRepository  # Importa el repositorio a probar
from domain.entities.transaction import Transaction, TransactionType, TransactionState  # Importa las entidades del dominio

class TestSQLiteTransactionRepository(unittest.TestCase):  # Define la clase de pruebas
    def setUp(self):  # Método que se ejecuta antes de cada prueba
        """Se ejecuta antes de cada prueba."""
        self.connection = sqlite3.connect(':memory:')  # Crea una base de datos en memoria
        
        # Crea la tabla de transacciones con sus campos
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS transacciones (
                id TEXT PRIMARY KEY,
                cuenta_id TEXT NOT NULL,
                monto DECIMAL(15,2) NOT NULL,
                tipo TEXT NOT NULL,
                estado TEXT NOT NULL,
                fecha TIMESTAMP NOT NULL
            )
        """)
        
        self.repository = SQLiteTransactionRepository(connection=self.connection)  # Inicializa el repositorio

    def tearDown(self):  # Método que se ejecuta después de cada prueba
        """Se ejecuta después de cada prueba."""
        if self.connection:
            self.connection.close()  # Cierra la conexión a la base de datos

    def _crear_transaccion_prueba(self) -> Transaction:  # Método auxiliar para crear transacciones de prueba
        """Helper para crear una transacción de prueba."""
        return Transaction(
            id=uuid4(),  # Genera un ID único
            cuenta_id=uuid4(),  # Genera un ID de cuenta único
            monto=Decimal('100.00'),  # Establece un monto de prueba
            tipo=TransactionType.DEPOSITO,  # Define el tipo como depósito
            estado=TransactionState.PENDIENTE,  # Estado inicial pendiente
            fecha=datetime.now()  # Fecha actual
        )

    def test_guardar_transaccion(self):  # Prueba el guardado de una transacción
        # Arrange: prepara los datos de prueba
        transaction_id = uuid4()
        cuenta_id = uuid4()
        transaction = Transaction(
            id=transaction_id,
            cuenta_id=cuenta_id,
            monto=Decimal('100.50'),
            tipo=TransactionType.DEPOSITO,
            estado=TransactionState.PENDIENTE,
            fecha=datetime.now()
        )

        # Act: ejecuta la acción a probar
        self.repository.guardar(transaction)
        recovered_transaction = self.repository.obtener_por_id(transaction_id)

        # Assert: verifica que los resultados sean correctos
        self.assertEqual(str(transaction.id), str(recovered_transaction.id))
        self.assertEqual(str(transaction.cuenta_id), str(recovered_transaction.cuenta_id))
        self.assertEqual(transaction.monto, recovered_transaction.monto)
        self.assertEqual(transaction.tipo, recovered_transaction.tipo)
        self.assertEqual(transaction.estado, recovered_transaction.estado)

    def test_obtener_transaccion_inexistente(self):  # Prueba la obtención de una transacción que no existe
        transaction_id = uuid4()
        with self.assertRaises(ValueError):  # Verifica que se lance una excepción ValueError
            self.repository.obtener_por_id(transaction_id)

    def test_listar_por_cuenta(self):  # Prueba listar transacciones por cuenta
        # Arrange: prepara los datos de prueba con múltiples transacciones
        cuenta_id = uuid4()
        transactions = [
            Transaction(
                id=uuid4(),
                cuenta_id=cuenta_id,
                monto=Decimal('100.00'),
                tipo=TransactionType.DEPOSITO,
                estado=TransactionState.APROBADA,
                fecha=datetime.now()
            ),
            Transaction(
                id=uuid4(),
                cuenta_id=cuenta_id,
                monto=Decimal('50.00'),
                tipo=TransactionType.RETIRO,
                estado=TransactionState.PENDIENTE,
                fecha=datetime.now()
            )
        ]
        
        # Act: guarda las transacciones y las recupera
        for transaction in transactions:
            self.repository.guardar(transaction)
        
        recovered_transactions = self.repository.listar_por_cuenta(cuenta_id)

        # Assert: verifica la cantidad y montos correctos
        self.assertEqual(len(recovered_transactions), 2)
        montos = [t.monto for t in recovered_transactions]
        self.assertIn(Decimal('100.00'), montos)
        self.assertIn(Decimal('50.00'), montos)

    def test_actualizar_transaccion_existente(self):  # Prueba la actualización de una transacción
        # Arrange: crea y guarda una transacción inicial
        transaction_id = uuid4()
        cuenta_id = uuid4()
        transaction = Transaction(
            id=transaction_id,
            cuenta_id=cuenta_id,
            monto=Decimal('100.00'),
            tipo=TransactionType.DEPOSITO,
            estado=TransactionState.PENDIENTE,
            fecha=datetime.now()
        )
        self.repository.guardar(transaction)

        # Act: modifica el estado y guarda
        transaction.estado = TransactionState.APROBADA
        self.repository.guardar(transaction)
        
        # Assert: verifica que el cambio se realizó correctamente
        updated_transaction = self.repository.obtener_por_id(transaction_id)
        self.assertEqual(updated_transaction.estado, TransactionState.APROBADA)

if __name__ == '__main__':
    unittest.main()  # Ejecuta las pruebas si se corre el archivo directamente