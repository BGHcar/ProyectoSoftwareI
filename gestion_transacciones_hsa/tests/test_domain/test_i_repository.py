import unittest
from uuid import UUID, uuid4
from typing import List
from unittest.mock import Mock
from domain.repositories.i_repository import IRepository

class EntidadPrueba:
    """Entidad de prueba para el repositorio genérico"""
    def __init__(self, id: UUID):
        self.id = id

class RepositorioPruebaMock(IRepository[EntidadPrueba]):
    """Implementación mock del repositorio para pruebas"""
    def guardar(self, entidad: EntidadPrueba) -> None:
        """Mock de guardar"""
        pass

    def obtener_por_id(self, id: UUID) -> EntidadPrueba:
        """Mock de obtener_por_id"""
        pass

    def listar_todos(self) -> List[EntidadPrueba]:
        """Mock de listar_todos"""
        pass

class TestIRepository(unittest.TestCase):
    def setUp(self):
        """Configuración inicial de pruebas"""
        self.repositorio = Mock(spec=RepositorioPruebaMock)
        self.id_prueba = uuid4()
        self.entidad_prueba = EntidadPrueba(self.id_prueba)

    def test_guardar_entidad(self):
        """Prueba método guardar"""
        # Ejecutar
        self.repositorio.guardar(self.entidad_prueba)
        # Verificar
        self.repositorio.guardar.assert_called_once_with(self.entidad_prueba)

    def test_obtener_por_id(self):
        """Prueba método obtener_por_id"""
        # Configurar
        self.repositorio.obtener_por_id.return_value = self.entidad_prueba
        # Ejecutar
        resultado = self.repositorio.obtener_por_id(self.id_prueba)
        # Verificar
        self.assertEqual(resultado, self.entidad_prueba)
        self.repositorio.obtener_por_id.assert_called_once_with(self.id_prueba)

    def test_listar_todos(self):
        """Prueba método listar_todos"""
        # Configurar
        entidades = [self.entidad_prueba]
        self.repositorio.listar_todos.return_value = entidades
        # Ejecutar
        resultado = self.repositorio.listar_todos()
        # Verificar
        self.assertEqual(resultado, entidades)
        self.repositorio.listar_todos.assert_called_once()

if __name__ == '__main__':
    unittest.main()