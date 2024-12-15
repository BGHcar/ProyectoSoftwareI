# tests/test_infrastructure/test_mongo_account_repository.py
import unittest                                     # Importa el módulo de pruebas unitarias
from unittest.mock import patch, MagicMock          # Importa herramientas para crear objetos simulados
from decimal import Decimal                         # Para manejar números decimales con precisión
from uuid import uuid4, UUID                        # Para generar y manejar identificadores únicos
from pymongo.collection import Collection           # Para tipar la colección de MongoDB
from infrastructure.repositories.mongo_account_repository import MongoAccountRepository  # Clase a probar
from domain.entities.account import Account         # Entidad de cuenta que se va a usar

class TestMongoAccountRepository(unittest.TestCase):
    def setUp(self):                               # Método que se ejecuta antes de cada prueba
        self.mock_collection = MagicMock(spec=Collection)  # Crea una colección simulada de MongoDB
        self.patcher = patch('infrastructure.repositories.mongo_account_repository.MongoClient')  # Prepara el parche para MongoClient
        self.mock_client = self.patcher.start()    # Inicia el parche
        
        mock_db = MagicMock()                      # Crea una base de datos simulada
        mock_db.accounts = self.mock_collection     # Asigna la colección simulada a la BD
        self.mock_client.return_value.hsa_db = mock_db  # Configura el cliente para usar la BD simulada
        
        self.repository = MongoAccountRepository()  # Crea una instancia del repositorio a probar

    def tearDown(self):
        """Se ejecuta después de cada prueba."""
        self.patcher.stop()

    def test_guardar_cuenta(self):                 # Prueba el método de guardar cuenta
        cuenta = Account(                          # Crea una cuenta de prueba
            id=uuid4(),                            # Genera ID único
            usuario_id=uuid4(),                    # Genera ID de usuario único
            saldo=Decimal('1000.0'),              # Establece saldo inicial
            limite_diario=Decimal('500.0')        # Establece límite diario
        )
        self.repository.guardar(cuenta)            # Intenta guardar la cuenta
        self.mock_collection.replace_one.assert_called_once_with(  # Verifica que se llamó al método correcto de MongoDB
            {"_id": str(cuenta.id)},               # Criterio de búsqueda
            {                                      # Datos a guardar
                "_id": str(cuenta.id),
                "usuario_id": str(cuenta.usuario_id),
                "saldo": cuenta.saldo,
                "limite_diario": cuenta.limite_diario
            },
            upsert=True                           # Permite insertar si no existe
        )

    def test_obtener_por_id(self):                # Prueba el método de obtener cuenta por ID
        cuenta_id = uuid4()                        # Genera ID de prueba
        usuario_id = uuid4()                       # Genera ID de usuario de prueba
        mock_account = {                           # Crea datos simulados de cuenta
            "_id": str(cuenta_id),
            "usuario_id": str(usuario_id),
            "saldo": "1000.50",
            "limite_diario": "500.25"
        }
        self.mock_collection.find_one.return_value = mock_account.copy()  # Configura el resultado simulado

        cuenta = self.repository.obtener_por_id(cuenta_id)  # Ejecuta el método a probar
        
        # Verificaciones
        self.mock_collection.find_one.assert_called_once_with({"_id": str(cuenta_id)})  # Verifica la llamada correcta
        self.assertEqual(str(cuenta.id), mock_account["_id"])                           # Verifica ID
        self.assertEqual(str(cuenta.usuario_id), mock_account["usuario_id"])            # Verifica ID de usuario
        self.assertEqual(cuenta.saldo, Decimal(mock_account["saldo"]))                  # Verifica saldo
        self.assertEqual(cuenta.limite_diario, Decimal(mock_account["limite_diario"]))  # Verifica límite diario

    def test_listar_todos(self):                  # Prueba el método de listar todas las cuentas
        self.repository.listar_todos()             # Ejecuta el método
        self.mock_collection.find.assert_called_once()  # Verifica que se llamó al método find

    def test_obtener_por_usuario(self):           # Prueba obtener cuentas por usuario
        usuario_id = UUID('61c8fd7a-948b-4aef-b0fd-74baf22a4624')  # ID de usuario de prueba
        self.repository.obtener_por_usuario(usuario_id)  # Ejecuta el método
        self.mock_collection.find.assert_called_with({"usuario_id": str(usuario_id)})  # Verifica la llamada

    def test_obtener_cuenta_inexistente(self):    # Prueba el caso de cuenta no existente
        self.mock_collection.find_one.return_value = None  # Simula que no se encontró la cuenta
        
        with self.assertRaises(ValueError):        # Verifica que se lance ValueError
            self.repository.obtener_por_id(uuid4())

if __name__ == '__main__':                        # Permite ejecutar las pruebas directamente
    unittest.main()