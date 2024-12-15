# Importación de módulos necesarios para las pruebas
import unittest  # Framework de pruebas unitarias
from unittest.mock import patch, MagicMock  # Herramientas para crear mocks
from datetime import datetime  # Para manejar fechas
from decimal import Decimal  # Para manejar números decimales precisos
from uuid import uuid4  # Para generar IDs únicos
from pymongo.collection import Collection  # Tipo de colección de MongoDB
from infrastructure.repositories.mongo_transaction_repository import MongoTransactionRepository  # Clase a probar
from domain.entities.transaction import Transaction  # Entidad de transacción

class TestMongoTransactionRepository(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada prueba."""
        self.mock_collection = MagicMock(spec=Collection)  # Crea un mock de la colección MongoDB
        self.patcher = patch('infrastructure.repositories.mongo_transaction_repository.MongoClient')  # Prepara el mock del cliente MongoDB
        self.mock_client = self.patcher.start()  # Inicia el mock
        
        # Configura la estructura simulada de MongoDB
        mock_db = MagicMock()
        mock_db.transacciones = self.mock_collection
        self.mock_client.return_value.hsa_db = mock_db
        
        self.repository = MongoTransactionRepository()  # Crea instancia del repositorio

    def tearDown(self):
        """Se ejecuta después de cada prueba."""
        self.patcher.stop()

    def test_guardar_transaccion(self):
        # Crea una transacción de prueba con datos ficticios
        transaction = Transaction(
            id=uuid4(),
            cuenta_id=uuid4(),
            monto=Decimal('100.50'),
            tipo='deposito',
            estado='pendiente',
            fecha=datetime.now()
        )

        # Ejecuta el método a probar
        self.repository.guardar(transaction)

        # Verifica que el método replace_one fue llamado correctamente
        self.mock_collection.replace_one.assert_called_once()
        args = self.mock_collection.replace_one.call_args[0]
        self.assertEqual(args[0], {"_id": str(transaction.id)})
        self.assertEqual(args[1]["monto"], str(transaction.monto))

    def test_obtener_por_id(self):
        # Configura datos de prueba
        transaction_id = uuid4()
        mock_transaction = {
            "_id": str(transaction_id),
            "cuenta_id": str(uuid4()),
            "monto": "100.50",
            "tipo": "deposito",
            "estado": "pendiente",
            "fecha": datetime.now().isoformat()
        }
        self.mock_collection.find_one.return_value = mock_transaction

        # Ejecuta el método y verifica resultados
        transaction = self.repository.obtener_por_id(transaction_id)
        self.mock_collection.find_one.assert_called_with({"_id": str(transaction_id)})
        self.assertEqual(str(transaction.id), mock_transaction["_id"])
        self.assertEqual(transaction.monto, Decimal(mock_transaction["monto"]))

    def test_obtener_transaccion_inexistente(self):
        # Arrange
        self.mock_collection.find_one.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError):
            self.repository.obtener_por_id(uuid4())

    def test_listar_por_cuenta(self):
        # Arrange
        cuenta_id = uuid4()
        mock_transactions = [
            {
                "_id": str(uuid4()),
                "cuenta_id": str(cuenta_id),
                "monto": "100.00",
                "tipo": "deposito",
                "estado": "completado",
                "fecha": datetime.now().isoformat()
            },
            {
                "_id": str(uuid4()),
                "cuenta_id": str(cuenta_id),
                "monto": "200.00",
                "tipo": "retiro",
                "estado": "pendiente",
                "fecha": datetime.now().isoformat()
            }
        ]
        self.mock_collection.find.return_value = mock_transactions

        # Act
        transactions = self.repository.listar_por_cuenta(cuenta_id)

        # Assert
        self.mock_collection.find.assert_called_with({"cuenta_id": str(cuenta_id)})
        self.assertEqual(len(transactions), 2)
        montos = [t.monto for t in transactions]
        self.assertIn(Decimal('100.00'), montos)
        self.assertIn(Decimal('200.00'), montos)

    def test_validar_precision_decimal(self):
        # Arrange
        transaction_id = uuid4()
        monto_exacto = "100.57"
        mock_transaction = {
            "_id": str(transaction_id),
            "cuenta_id": str(uuid4()),
            "monto": monto_exacto,
            "tipo": "deposito",
            "estado": "pendiente",
            "fecha": datetime.now().isoformat()
        }
        self.mock_collection.find_one.return_value = mock_transaction

        # Act
        transaction = self.repository.obtener_por_id(transaction_id)

        # Assert
        self.assertEqual(str(transaction.monto), monto_exacto)

if __name__ == '__main__':
    unittest.main()