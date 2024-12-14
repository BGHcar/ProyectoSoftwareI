# infrastructure/repositories/mongo_transaction_repository.py
from typing import List                          # Importa el tipo List para tipar listas
from uuid import UUID                           # Importa UUID para identificadores únicos
from decimal import Decimal                     # Importa Decimal para manejo preciso de números decimales
from datetime import datetime                   # Importa datetime para manejo de fechas
from pymongo import MongoClient                 # Cliente para conectar con MongoDB
from pymongo.database import Database           # Tipo Database de MongoDB
from domain.repositories.i_transaction_repository import ITransactionRepository  # Interfaz base
from domain.entities.transaction import Transaction  # Entidad de transacción

class MongoTransactionRepository(ITransactionRepository):  # Implementación MongoDB del repositorio
    """
    Implementación MongoDB del repositorio de transacciones.
    """
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):  # Constructor con URL de conexión
        """
        Inicializa el repositorio MongoDB.
        
        Args:
            connection_string: URI de conexión a MongoDB
        """
        self.client = MongoClient(connection_string)    # Crea conexión a MongoDB
        self.db: Database = self.client.hsa_db         # Selecciona la base de datos
        self.collection = self.db.transacciones        # Selecciona la colección
        self._crear_indices()                          # Crea índices al inicializar

    def _crear_indices(self) -> None:
        """Crea los índices necesarios en la colección."""
        self.collection.create_index("cuenta_id")      # Crea índice para búsquedas rápidas por cuenta_id

    def guardar(self, transaccion: Transaction) -> None:
        """
        Guarda una transacción en la base de datos.
        
        Args:
            transaccion: Objeto Transaction a guardar
        """
        transaction_dict = {                           # Convierte Transaction a diccionario
            "_id": str(transaccion.id),               # Convierte UUID a string
            "cuenta_id": str(transaccion.cuenta_id),  # Convierte UUID a string
            "monto": str(transaccion.monto),          # Convierte Decimal a string
            "tipo": transaccion.tipo,
            "estado": transaccion.estado,
            "fecha": transaccion.fecha.isoformat()    # Convierte datetime a string ISO
        }
        self.collection.replace_one(                  # Actualiza o inserta el documento
            {"_id": transaction_dict["_id"]},         # Busca por ID
            transaction_dict,                         # Nuevo documento
            upsert=True                              # Crea si no existe
        )

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
        transaction_dict = self.collection.find_one({"_id": str(id)})  # Busca documento por ID
        if not transaction_dict:
            raise ValueError(f"No se encontró la transacción con id {id}")
            
        return Transaction(                          # Convierte diccionario a Transaction
            id=UUID(transaction_dict["_id"]),       # Convierte string a UUID
            cuenta_id=UUID(transaction_dict["cuenta_id"]),  # Convierte string a UUID
            monto=Decimal(transaction_dict["monto"]),       # Convierte string a Decimal
            tipo=transaction_dict["tipo"],
            estado=transaction_dict["estado"],
            fecha=datetime.fromisoformat(transaction_dict["fecha"])  # Convierte ISO a datetime
        )

    def listar_por_cuenta(self, cuenta_id: UUID) -> List[Transaction]:
        """
        Lista todas las transacciones de una cuenta específica.
        
        Args:
            cuenta_id: UUID de la cuenta
            
        Returns:
            List[Transaction]: Lista de transacciones de la cuenta
        """
        transactions = self.collection.find({"cuenta_id": str(cuenta_id)})  # Busca todas las transacciones de una cuenta
        return [                                    # Convierte cada documento a Transaction
            Transaction(
                id=UUID(t["_id"]),
                cuenta_id=UUID(t["cuenta_id"]),
                monto=Decimal(t["monto"]),
                tipo=t["tipo"],
                estado=t["estado"],
                fecha=datetime.fromisoformat(t["fecha"])
            )
            for t in transactions                   # Itera sobre los resultados
        ]

    def __del__(self):                             # Destructor
        """Cierra la conexión al eliminar la instancia."""
        self.client.close()                        # Cierra la conexión a MongoDB