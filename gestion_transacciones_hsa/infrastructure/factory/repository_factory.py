from typing import Type  # Importa el tipo Type para anotaciones de tipo
# Importaciones de interfaces de repositorios
from domain.repositories.i_transaction_repository import ITransactionRepository  # Interface para repositorio de transacciones
from domain.repositories.i_account_repository import IAccountRepository  # Interface para repositorio de cuentas

# Importaciones de implementaciones SQLite
from infrastructure.repositories.sqlite_transaction_repository import SQLiteTransactionRepository  # Implementación SQLite para transacciones
from infrastructure.repositories.sqlite_account_repository import SQLiteAccountRepository  # Implementación SQLite para cuentas

# Importaciones de implementaciones MongoDB
from infrastructure.repositories.mongo_transaction_repository import MongoTransactionRepository  # Implementación MongoDB para transacciones
from infrastructure.repositories.mongo_account_repository import MongoAccountRepository  # Implementación MongoDB para cuentas

class RepositoryFactory:  # Define la clase fábrica de repositorios
    """
    Fábrica para crear repositorios concretos según la configuración del sistema.
    Implementa el patrón Factory para la creación de repositorios.
    """
    
    def __init__(self, db_type: str = "sqlite"):  # Constructor que acepta el tipo de base de datos
        """
        Inicializa la fábrica con el tipo de base de datos.
        
        Args:
            db_type: Tipo de base de datos ('sqlite' o 'mongo')
        """
        self.db_type = db_type.lower()  # Almacena el tipo de BD en minúsculas
        self._validate_db_type()  # Valida que el tipo de BD sea válido
    
    def _validate_db_type(self) -> None:  # Método privado para validación
        """Valida que el tipo de base de datos sea soportado."""
        valid_types = ['sqlite', 'mongo']  # Define los tipos válidos de BD
        if self.db_type not in valid_types:  # Verifica si el tipo es válido
            raise ValueError(f"Tipo de base de datos no soportado. Tipos válidos: {valid_types}")  # Lanza error si no es válido

    def obtener_transaction_repository(self) -> ITransactionRepository:  # Método para obtener repositorio de transacciones
        """
        Retorna una instancia de ITransactionRepository según el tipo de base de datos configurado.
        
        Returns:
            ITransactionRepository: Una implementación concreta del repositorio de transacciones
        """
        if self.db_type == "sqlite":  # Si el tipo es SQLite
            return SQLiteTransactionRepository()  # Retorna implementación SQLite
        return MongoTransactionRepository()  # Si no, retorna implementación MongoDB
    
    def obtener_account_repository(self) -> IAccountRepository:  # Método para obtener repositorio de cuentas
        """
        Retorna una instancia de IAccountRepository según el tipo de base de datos configurado.
        
        Returns:
            IAccountRepository: Una implementación concreta del repositorio de cuentas
        """
        if self.db_type == "sqlite":  # Si el tipo es SQLite
            return SQLiteAccountRepository()  # Retorna implementación SQLite
        return MongoAccountRepository()  # Si no, retorna implementación MongoDB