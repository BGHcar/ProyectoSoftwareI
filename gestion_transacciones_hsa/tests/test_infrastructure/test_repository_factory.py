# tests/test_infrastructure/test_repository_factory.py
import unittest  # Importa el módulo de pruebas unitarias
from infrastructure.factory.repository_factory import RepositoryFactory  # Importa la fábrica de repositorios
# Importaciones de los repositorios SQLite y MongoDB
from infrastructure.repositories.sqlite_transaction_repository import SQLiteTransactionRepository
from infrastructure.repositories.sqlite_account_repository import SQLiteAccountRepository
from infrastructure.repositories.mongo_transaction_repository import MongoTransactionRepository
from infrastructure.repositories.mongo_account_repository import MongoAccountRepository

class TestRepositoryFactory(unittest.TestCase):  # Define la clase de pruebas
    def test_crear_factory_con_sqlite_por_defecto(self):  # Prueba la creación por defecto
        factory = RepositoryFactory()  # Crea una instancia de la fábrica sin parámetros
        self.assertEqual(factory.db_type, "sqlite")  # Verifica que el tipo por defecto sea SQLite

    def test_crear_factory_con_tipo_db_invalido(self):  # Prueba el manejo de tipos inválidos
        with self.assertRaises(ValueError):  # Verifica que se lance ValueError
            RepositoryFactory("mysql")  # Intenta crear fábrica con tipo de DB no soportado

    def test_crear_sqlite_transaction_repository(self):  # Prueba creación de repositorio SQLite
        factory = RepositoryFactory("sqlite")  # Crea fábrica SQLite
        repo = factory.obtener_transaction_repository()  # Obtiene repositorio de transacciones
        self.assertIsInstance(repo, SQLiteTransactionRepository)  # Verifica el tipo correcto

    def test_crear_sqlite_account_repository(self):  # Prueba creación de repositorio de cuentas SQLite
        factory = RepositoryFactory("sqlite")
        repo = factory.obtener_account_repository()
        self.assertIsInstance(repo, SQLiteAccountRepository)

    def test_crear_mongo_transaction_repository(self):  # Prueba creación de repositorio MongoDB
        factory = RepositoryFactory("mongo")
        repo = factory.obtener_transaction_repository()
        self.assertIsInstance(repo, MongoTransactionRepository)

    def test_crear_mongo_account_repository(self):  # Prueba creación de repositorio de cuentas MongoDB
        factory = RepositoryFactory("mongo")
        repo = factory.obtener_account_repository()
        self.assertIsInstance(repo, MongoAccountRepository)

if __name__ == '__main__':  # Permite ejecutar las pruebas directamente
    unittest.main()  # Ejecuta todas las pruebas de la clase