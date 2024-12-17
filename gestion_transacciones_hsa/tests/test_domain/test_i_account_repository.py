import unittest
from unittest.mock import Mock
from uuid import uuid4
from typing import List

from domain.entities.account import Account
from domain.repositories.i_account_repository import IAccountRepository

class TestAccountRepository(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.repository = Mock(spec=IAccountRepository)
        self.cuenta_id = uuid4()
        self.usuario_id = uuid4()
        self.cuenta_prueba = Account(
            id=self.cuenta_id,
            usuario_id=self.usuario_id,
            saldo=1000.0,
            limite_diario=float("500.0")
        )

    def test_obtener_por_id(self):
        """Prueba obtener cuenta por ID"""
        # Configurar mock
        self.repository.obtener_por_usuario.return_value = self.cuenta_prueba
        # Ejecutar
        cuenta = self.repository.obtener_por_id(self.cuenta_id)
        # Verificar
        self.assertEqual(cuenta, self.cuenta_prueba)
        self.repository.obtener_por_id.assert_called_once_with(self.cuenta_id)

    def test_listar_todos(self):
        """Prueba listar todas las cuentas"""
        # Configurar mock
        cuentas = [self.cuenta_prueba]
        self.repository.listar_todos.return_value = cuentas
        # Ejecutar
        resultado = self.repository.listar_todos()
        # Verificar
        self.assertEqual(resultado, cuentas)
        self.repository.listar_todos.assert_called_once()

    def test_guardar(self):
        """Prueba guardar cuenta"""
        # Ejecutar
        self.repository.guardar(self.cuenta_prueba)
        # Verificar
        self.repository.guardar.assert_called_once_with(self.cuenta_prueba)

    def test_obtener_por_usuario(self):
        """Prueba obtener cuentas por ID de usuario"""
        # Configurar mock
        cuentas_usuario = [self.cuenta_prueba]
        self.repository.obtener_por_usuario.return_value = cuentas_usuario

        # Ejecutar prueba
        cuentas = self.repository.obtener_por_usuario(self.usuario_id)

        # Verificaciones
        self.assertEqual(len(cuentas), 1)
        self.assertEqual(cuentas[0].usuario_id, self.usuario_id)
        self.repository.obtener_por_usuario.assert_called_once_with(self.usuario_id)

if __name__ == '__main__':
    unittest.main()