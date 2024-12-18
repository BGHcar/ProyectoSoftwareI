from fastapi import FastAPI
# En app/main.py
from infrastructure.repositories.sqlite_account_repository import SQLiteAccountRepository
from infrastructure.repositories.sqlite_transaction_repository import SQLiteTransactionRepository
from domain.services.transaction_service import TransactionService
from application.services.transaction_application_service import TransactionApplicationService
from app.controllers.transaction_controller import router as transaction_router
from app.controllers.account_controller import router as account_router

# Crear repositorios concretos
account_repository = SQLiteAccountRepository(db_path="database.db")
transaction_repository = SQLiteTransactionRepository(db_path="database.db")

# Crear el servicio de dominio
transaction_service = TransactionService(
    transaction_repository=transaction_repository,
    account_repository=account_repository,
)

# Crear el servicio de aplicación
transaction_app_service = TransactionApplicationService(
    transaction_service=transaction_service,
    account_repository=account_repository,
)

# Crear la aplicación FastAPI
app = FastAPI()

# Incluir los routers
app.include_router(transaction_router)
app.include_router(account_router)

@app.get("/")
def root():
    return {"message": "API de Gestión de Transacciones funcionando correctamente"}
