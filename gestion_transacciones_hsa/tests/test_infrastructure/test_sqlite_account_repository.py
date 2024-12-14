# Importación de módulos necesarios
import unittest                   # Framework para pruebas unitarias
import sqlite3                    # Módulo para trabajar con SQLite
from unittest.mock import patch   # Para hacer mock de objetos en pruebas
from decimal import Decimal       # Para manejar números decimales con precisión
from uuid import UUID, uuid4      # Para generar identificadores únicos
from infrastructure.repositories.sqlite_account_repository import SQLiteAccountRepository
from domain.entities.account import Account

class TestSQLiteAccountRepository(unittest.TestCase):
    def setUp(self):
        """Se ejecuta antes de cada prueba."""
        self.connection = sqlite3.connect(':memory:')    # Crear conexión a BD en memoria
        
        # Crear tabla de cuentas con sus campos
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS cuentas (
                id TEXT PRIMARY KEY,                     
                usuario_id TEXT NOT NULL,                
                saldo DECIMAL(10,2) NOT NULL,           
                limite_diario DECIMAL(10,2) NOT NULL    
            )
        """)
        
        # Inicializar el repositorio con la conexión de prueba
        self.repository = SQLiteAccountRepository(connection=self.connection)

    def tearDown(self):
        """Se ejecuta después de cada prueba."""
        if self.connection:
            self.connection.close()

    def _crear_cuenta_prueba(self) -> Account:
        """Helper que crea una cuenta con datos de prueba"""
        return Account(
            id=uuid4(),                    # Genera ID aleatorio
            usuario_id=uuid4(),            # Genera ID de usuario aleatorio
            saldo=Decimal('1000.00'),      # Saldo inicial
            limite_diario=Decimal('500.00') # Límite diario
        )

    def test_guardar_cuenta(self):
        # Prueba que una cuenta se guarde correctamente
        cuenta = self._crear_cuenta_prueba()
        self.repository.guardar(cuenta)
        cuenta_recuperada = self.repository.obtener_por_id(cuenta.id)
        # Verifica que todos los datos se guardaron correctamente
        self.assertEqual(str(cuenta.id), str(cuenta_recuperada.id))
        self.assertEqual(str(cuenta.usuario_id), str(cuenta_recuperada.usuario_id))
        self.assertEqual(cuenta.saldo, cuenta_recuperada.saldo)
        self.assertEqual(cuenta.limite_diario, cuenta_recuperada.limite_diario)

    def test_obtener_cuenta_inexistente(self):
        # Prueba que se lance error al buscar cuenta que no existe
        cuenta_id = uuid4()
        with self.assertRaises(ValueError):
            self.repository.obtener_por_id(cuenta_id)

    def test_listar_todos(self):
        # Prueba que se listen todas las cuentas correctamente
        cuentas = [self._crear_cuenta_prueba() for _ in range(3)]  # Crea 3 cuentas
        for cuenta in cuentas:
            self.repository.guardar(cuenta)
        
        cuentas_recuperadas = self.repository.listar_todos()
        # Verifica que se recuperaron todas las cuentas
        self.assertEqual(len(cuentas_recuperadas), 3)
        saldos = [cuenta.saldo for cuenta in cuentas_recuperadas]
        self.assertEqual(len(saldos), 3)
        for saldo in saldos:
            self.assertEqual(saldo, Decimal('1000.00'))

    def test_obtener_por_usuario(self):
        # Prueba que se obtengan solo las cuentas de un usuario específico
        usuario_id = uuid4()
        # Crea dos cuentas para el mismo usuario
        cuentas = [
            Account(
                id=uuid4(),
                usuario_id=usuario_id,
                saldo=Decimal('1000.00'),
                limite_diario=Decimal('500.00')
            ),
            Account(
                id=uuid4(),
                usuario_id=usuario_id,
                saldo=Decimal('2000.00'),
                limite_diario=Decimal('1000.00')
            )
        ]
        # Guardar cuenta de otro usuario para verificar que no se mezclan
        otra_cuenta = Account(
            id=uuid4(),
            usuario_id=uuid4(),
            saldo=Decimal('3000.00'),
            limite_diario=Decimal('1500.00')
        )
        
        for cuenta in cuentas + [otra_cuenta]:
            self.repository.guardar(cuenta)

        # Verifica que se recuperen solo las cuentas del usuario correcto
        cuentas_usuario = self.repository.obtener_por_usuario(usuario_id)
        self.assertEqual(len(cuentas_usuario), 2)
        saldos = [cuenta.saldo for cuenta in cuentas_usuario]
        self.assertIn(Decimal('1000.00'), saldos)
        self.assertIn(Decimal('2000.00'), saldos)

    def test_actualizar_cuenta_existente(self):
        # Prueba que se actualice correctamente una cuenta existente
        cuenta = self._crear_cuenta_prueba()
        self.repository.guardar(cuenta)
        cuenta.saldo = Decimal('1500.00')  # Modifica el saldo
        self.repository.guardar(cuenta)    # Actualiza la cuenta
        # Verifica que el cambio se guardó
        cuenta_actualizada = self.repository.obtener_por_id(cuenta.id)
        self.assertEqual(cuenta_actualizada.saldo, Decimal('1500.00'))

    def test_validar_precision_decimal(self):
        # Prueba que los números decimales mantengan su precisión
        cuenta = Account(
            id=uuid4(),
            usuario_id=uuid4(),
            saldo=Decimal('1000.50'),      # Prueba con decimales
            limite_diario=Decimal('500.25')
        )
        # Verifica que los decimales se mantienen exactos
        self.repository.guardar(cuenta)
        cuenta_recuperada = self.repository.obtener_por_id(cuenta.id)
        self.assertEqual(cuenta.saldo, cuenta_recuperada.saldo)
        self.assertEqual(cuenta.limite_diario, cuenta_recuperada.limite_diario)
        self.assertEqual(str(cuenta_recuperada.saldo), '1000.50')
        self.assertEqual(str(cuenta_recuperada.limite_diario), '500.25')

if __name__ == '__main__':
    unittest.main()