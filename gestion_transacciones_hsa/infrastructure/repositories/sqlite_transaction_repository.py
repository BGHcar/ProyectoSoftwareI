# infrastructure/repositories/sqlite_transaction_repository.py
from typing import List, Optional  # Importa tipos para anotaciones de tipo
from uuid import UUID  # Importa UUID para identificadores únicos
from decimal import Decimal  # Importa Decimal para manejo preciso de números decimales
from datetime import datetime  # Importa datetime para manejo de fechas y tiempo
from contextlib import contextmanager  # Importa decorador para manejar contextos
import sqlite3  # Importa el módulo para trabajar con SQLite

# Importa interfaces y entidades del dominio
from domain.repositories.i_transaction_repository import ITransactionRepository
from domain.entities.transaction import Transaction, TransactionType, TransactionState

class SQLiteTransactionRepository(ITransactionRepository):
    """
    Implementación SQLite del repositorio de transacciones.
    """
    
    def __init__(self, db_path: str = "database.db", connection: Optional[sqlite3.Connection] = None):
        """
        Inicializa el repositorio SQLite.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path  # Almacena la ruta de la base de datos
        self._test_connection = connection  # Almacena conexión de prueba si se proporciona
        self._create_tables()  # Crea las tablas necesarias

    @contextmanager
    def _get_connection(self):
        """
        Administrador de contexto para manejar la conexión a la base de datos.
        """
        if self._test_connection is not None:  # Verifica si hay una conexión de prueba
            yield self._test_connection  # Usa la conexión de prueba
            return
            
        conn = sqlite3.connect(self.db_path)  # Crea una nueva conexión a la base de datos
        try:
            yield conn  # Proporciona la conexión
            conn.commit()  # Confirma los cambios si todo está bien
        except Exception:
            conn.rollback()  # Revierte cambios si hay error
            raise
        finally:
            conn.close()  # Cierra la conexión en cualquier caso

    def _create_tables(self):
        with self._get_connection() as conn:  # Obtiene una conexión usando el context manager
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transacciones (
                    id TEXT PRIMARY KEY,
                    cuenta_id TEXT NOT NULL,
                    monto DECIMAL(15,2) NOT NULL,
                    tipo TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    fecha TIMESTAMP NOT NULL
                )
            """)

    def guardar(self, transaccion: Transaction) -> None:
        """
        Guarda una transacción en la base de datos.
        
        Args:
            transaccion: Objeto Transaction a guardar
        """
        with self._get_connection() as conn:  # Obtiene una conexión a la base de datos
            conn.execute("""
                INSERT OR REPLACE INTO transacciones 
                (id, cuenta_id, monto, tipo, estado, fecha)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(transaccion.id),  # Convierte UUID a string
                str(transaccion.cuenta_id),  # Convierte UUID a string
                f"{transaccion.monto:.2f}",  # Formatea el monto a 2 decimales
                transaccion.tipo.value,  # Obtiene el valor del enum
                transaccion.estado.value,  # Obtiene el valor del enum
                transaccion.fecha.isoformat()  # Convierte fecha a formato ISO
            ))

    def obtener_por_id(self, id: UUID) -> Transaction:
        """
        Obtiene una transacción por su ID.
        
        Args:
            id: UUID de la transacción
            
        Returns:
            Transaction: La transacción encontrada
            
        Raises:
            ValueError: Si no se encuentra la transacción
        """
        with self._get_connection() as conn:  # Obtiene una conexión a la base de datos
            cursor = conn.execute(
                "SELECT * FROM transacciones WHERE id = ?", # Consulta por ID
                (str(id),)  # Convierte UUID a string para la consulta
            )
            row = cursor.fetchone()  # Obtiene la primera fila del resultado
            
            if not row:  # Verifica si se encontró algún resultado
                raise ValueError(f"No se encontró la transacción con id {id}")
            
            return Transaction(  # Crea y retorna un objeto Transaction
                id=UUID(row[0]),  # Convierte string a UUID
                cuenta_id=UUID(row[1]),  # Convierte string a UUID
                monto=Decimal(str(row[2])),  # Convierte a Decimal
                tipo=TransactionType(row[3]),  # Convierte string a enum
                estado=TransactionState(row[4]),  # Convierte string a enum
                fecha=datetime.fromisoformat(row[5])  # Convierte string a datetime
            )

    def listar_por_cuenta(self, cuenta_id: UUID) -> List[Transaction]:
        """
        Lista todas las transacciones de una cuenta específica.
        
        Args:
            cuenta_id: UUID de la cuenta
            
        Returns:
            List[Transaction]: Lista de transacciones de la cuenta
        """
        with self._get_connection() as conn:  # Obtiene una conexión a la base de datos
            cursor = conn.execute(
                "SELECT * FROM transacciones WHERE cuenta_id = ?",  # Consulta por cuenta_id
                (str(cuenta_id),)  # Convierte UUID a string para la consulta
            )
            return [  # Retorna lista de transacciones
                Transaction(  # Crea objeto Transaction para cada fila
                    id=UUID(row[0]),  # Convierte string a UUID
                    cuenta_id=UUID(row[1]),  # Convierte string a UUID
                    monto=Decimal(str(row[2])),  # Convierte a Decimal
                    tipo=TransactionType(row[3]),  # Convierte string a enum
                    estado=TransactionState(row[4]),  # Convierte string a enum
                    fecha=datetime.fromisoformat(row[5])  # Convierte string a datetime
                )
                for row in cursor.fetchall()  # Itera sobre todas las filas
            ]