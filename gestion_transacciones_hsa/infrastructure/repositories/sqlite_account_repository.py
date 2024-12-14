from typing import List, Optional  # Importa tipos para anotaciones tipadas
from uuid import UUID  # Importa clase UUID para identificadores únicos
from decimal import Decimal  # Importa Decimal para manejo preciso de números decimales
from contextlib import contextmanager  # Importa decorador para manejar contextos
import sqlite3  # Importa el módulo para trabajar con SQLite

# Importa interfaces y entidades del dominio
from domain.repositories.i_account_repository import IAccountRepository
from domain.entities.account import Account

class SQLiteAccountRepository(IAccountRepository):  # Define clase que implementa la interfaz IAccountRepository
    
    def __init__(self, db_path: str = "database.db", connection: Optional[sqlite3.Connection] = None):
        self.db_path = db_path  # Almacena la ruta de la base de datos
        self._test_connection = connection  # Guarda conexión de prueba si se proporciona
        self._create_tables()  # Inicializa las tablas

    @contextmanager  # Decorador para manejar el contexto de conexión
    def _get_connection(self):
        if self._test_connection is not None:  # Verifica si hay conexión de prueba
            yield self._test_connection  # Usa la conexión de prueba
            return
            
        conn = sqlite3.connect(self.db_path)  # Crea nueva conexión a la BD
        try:
            yield conn  # Proporciona la conexión
            conn.commit()  # Confirma cambios si todo está bien
        except Exception:
            conn.rollback()  # Revierte cambios si hay error
            raise
        finally:
            conn.close()  # Cierra la conexión en cualquier caso

    def _create_tables(self) -> None:
        """Crea la tabla de cuentas si no existe."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cuentas (
                    id TEXT PRIMARY KEY,
                    usuario_id TEXT NOT NULL,
                    saldo DECIMAL(15,2) NOT NULL,
                    limite_diario DECIMAL(15,2) NOT NULL
                )
            """)

    def guardar(self, cuenta: Account) -> None:
        """
        Guarda una cuenta en la base de datos.
        
        Args:
            cuenta: Objeto Account a guardar
        """
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO cuentas 
                (id, usuario_id, saldo, limite_diario)
                VALUES (?, ?, ?, ?)
            """, (
                str(cuenta.id),
                str(cuenta.usuario_id),
                f"{cuenta.saldo:.2f}",  # Formatear con 2 decimales
                f"{cuenta.limite_diario:.2f}"  # Formatear con 2 decimales
            ))

    def obtener_por_id(self, id: UUID) -> Account:
        """
        Obtiene una cuenta por su ID.
        
        Args:
            id: UUID de la cuenta
            
        Returns:
            Account: La cuenta encontrada
            
        Raises:
            ValueError: Si no se encuentra la cuenta
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM cuentas WHERE id = ?",
                (str(id),)
            )
            row = cursor.fetchone()
            
            if not row:
                raise ValueError(f"No se encontró la cuenta con id {id}")
            
            return Account(
                id=UUID(row[0]),
                usuario_id=UUID(row[1]),
                saldo=Decimal(f"{Decimal(str(row[2])):.2f}"),  # Forzar 2 decimales
                limite_diario=Decimal(f"{Decimal(str(row[3])):.2f}")  # Forzar 2 decimales
            )

    def listar_todos(self) -> List[Account]:
        """
        Lista todas las cuentas en la base de datos.
        
        Returns:
            List[Account]: Lista de todas las cuentas
        """
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM cuentas")
            return [
                Account(
                    id=UUID(row[0]),
                    usuario_id=UUID(row[1]),
                    saldo=Decimal(f"{Decimal(str(row[2])):.2f}"),  # Forzar 2 decimales
                    limite_diario=Decimal(f"{Decimal(str(row[3])):.2f}")  # Forzar 2 decimales
                )
                for row in cursor.fetchall()
            ]

    def obtener_por_usuario(self, usuario_id: UUID) -> List[Account]:
        """
        Obtiene todas las cuentas de un usuario específico.
        
        Args:
            usuario_id: UUID del usuario
            
        Returns:
            List[Account]: Lista de cuentas del usuario
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM cuentas WHERE usuario_id = ?",
                (str(usuario_id),)
            )
            return [
                Account(
                    id=UUID(row[0]),
                    usuario_id=UUID(row[1]),
                    saldo=Decimal(f"{Decimal(str(row[2])):.2f}"),  # Forzar 2 decimales
                    limite_diario=Decimal(f"{Decimal(str(row[3])):.2f}")  # Forzar 2 decimales
                )
                for row in cursor.fetchall()
            ]