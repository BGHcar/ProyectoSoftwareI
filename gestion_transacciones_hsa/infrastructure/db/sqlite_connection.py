# infrastructure/db/sqlite_connection.py
from contextlib import contextmanager       # Importa el decorador para crear administradores de contexto
import sqlite3                             # Importa la biblioteca para trabajar con SQLite
from typing import Generator               # Importa el tipo Generator para anotaciones de tipo

@contextmanager                            # Decorador que convierte la función en un administrador de contexto
def get_sqlite_connection(db_path: str) -> Generator[sqlite3.Connection, None, None]:    # Define función que recibe ruta BD y retorna un generador
    """
    Administrador de contexto para conexiones SQLite.
    
    Args:
        db_path (str): Ruta a la base de datos SQLite
        
    Yields:
        sqlite3.Connection: Conexión a la base de datos
    """
    conn = sqlite3.connect(db_path)        # Crea una conexión a la base de datos SQLite
    try:
        conn.execute("PRAGMA foreign_keys = ON")    # Activa el soporte para claves foráneas
        yield conn                         # Devuelve la conexión al contexto
        conn.commit()                      # Confirma los cambios si todo sale bien
    except Exception:
        conn.rollback()                    # Revierte los cambios si hay algún error
        raise                              # Re-lanza la excepción
    finally:
        conn.close()                       # Cierra la conexión en cualquier caso