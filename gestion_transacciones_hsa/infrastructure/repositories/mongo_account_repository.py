# infrastructure/repositories/mongo_account_repository.py
from typing import List  # Importa el tipo List para tipar listas
from uuid import UUID   # Importa UUID para manejar identificadores únicos
from pymongo import MongoClient  # Cliente para conectar con MongoDB
from domain.repositories.i_account_repository import IAccountRepository  # Interfaz del repositorio
from domain.entities.account import Account  # Entidad Account
from decimal import Decimal  # Para manejar números decimales con precisión

class MongoAccountRepository(IAccountRepository):  # Implementación de repositorio con MongoDB
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')  # Conecta a MongoDB local
        self.db = self.client.hsa_db  # Selecciona la base de datos
        self.accounts = self.db.accounts  # Selecciona la colección de cuentas

    def __del__(self):
        self.client.close()  # Cierra la conexión al destruir el objeto

    def guardar(self, account: Account) -> None:
        account_dict = {  # Convierte la cuenta a diccionario para MongoDB
            "_id": str(account.id),  # ID como string
            "usuario_id": str(account.usuario_id),  # ID de usuario como string
            "saldo": float(account.saldo),  # Saldo como float
            "limite_diario": float(account.limite_diario)  # Límite como float
        }
        try:
            self.accounts.replace_one(  # Actualiza o inserta el documento
                {"_id": account_dict["_id"]},  # Busca por ID
                account_dict,  # Nuevo documento
                upsert=True  # Crea si no existe
            )
        except Exception as e:
            raise RuntimeError(f"Error al guardar la cuenta: {e}")

    def obtener_por_id(self, account_id: UUID) -> Account:
        try:
            account_dict = self.accounts.find_one({"_id": str(account_id)})  # Busca una cuenta por ID
            if account_dict is None:
                raise ValueError(f"Cuenta no encontrada: {account_id}")
            
            # Procesa el documento para convertirlo en objeto Account
            account_dict["id"] = account_dict["_id"]  # Copia _id a id
            del account_dict["_id"]  # Elimina _id para evitar duplicados
            account_dict["id"] = str(account_dict["id"])  # Convierte ID a string
            account_dict["usuario_id"] = str(account_dict["usuario_id"])  # Convierte usuario_id a string
            
            # Convierte valores numéricos a Decimal
            if not isinstance(account_dict["saldo"], Decimal):
                account_dict["saldo"] = Decimal(account_dict["saldo"])
            if not isinstance(account_dict["limite_diario"], Decimal):
                account_dict["limite_diario"] = Decimal(account_dict["limite_diario"])
            
            return Account.from_dict(account_dict)  # Crea objeto Account desde diccionario
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise RuntimeError(f"Error al obtener la cuenta por ID: {e}")

    def listar_todos(self) -> List[Account]:
        try:
            return [Account.from_dict(account) for account in self.accounts.find()]  # Lista todas las cuentas
        except Exception as e:
            raise RuntimeError(f"Error al listar todas las cuentas: {e}")
    
    def obtener_por_usuario(self, usuario_id: UUID) -> List[Account]:
        try:
            accounts = self.accounts.find({"usuario_id": str(usuario_id)})  # Busca cuentas por ID de usuario
            return [Account.from_dict(account) for account in accounts]  # Convierte resultados a objetos Account
        except Exception as e:
            raise RuntimeError(f"Error al obtener cuentas por usuario: {e}")