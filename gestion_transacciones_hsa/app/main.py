from fastapi import FastAPI
from infrastructure.repositories.sqlite_account_repository import SQLiteAccountRepository
from infrastructure.repositories.sqlite_transaction_repository import SQLiteTransactionRepository
from infrastructure.repositories.mongo_account_repository import MongoAccountRepository
from infrastructure.repositories.mongo_transaction_repository import MongoTransactionRepository
from domain.services.transaction_service import TransactionService
from application.services.transaction_application_service import TransactionApplicationService
from app.controllers.transaction_controller import router as transaction_router
from app.controllers.account_controller import router as account_router

# Crear repositorios SQLite
account_repository = SQLiteAccountRepository(db_path="database.db")
transaction_repository = SQLiteTransactionRepository(db_path="database.db")

# Crear repositorios MongoDB
mongo_account_repository = MongoAccountRepository()
mongo_transaction_repository = MongoTransactionRepository()

# Crear el servicio de dominio con ambos repositorios
transaction_service = TransactionService(
    transaction_repository=transaction_repository,
    account_repository=account_repository
)

# Crear el servicio de aplicación
transaction_app_service = TransactionApplicationService(
    transaction_service=transaction_service,
    account_repository=account_repository
)

# Crear servicio de transacción para MongoDB
mongo_transaction_service = TransactionService(
    transaction_repository=mongo_transaction_repository,
    account_repository=mongo_account_repository
)

# Crear servicio de aplicación para MongoDB
mongo_app_service = TransactionApplicationService(
    transaction_service=mongo_transaction_service,
    account_repository=mongo_account_repository
)

# Crear la aplicación FastAPI
app = FastAPI()

# Incluir los routers
app.include_router(transaction_router)
app.include_router(account_router)

@app.get("/")
def root():
    return {"message": "API de Gestión de Transacciones funcionando correctamente"}
