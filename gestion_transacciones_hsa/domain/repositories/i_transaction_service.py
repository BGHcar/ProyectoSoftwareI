# domain/repositories/i_transaction_service.py

from uuid import UUID
from typing import List
from gestion_transacciones_hsa.domain.entities.transaction import Transaction
from gestion_transacciones_hsa.domain.entities.account import Account

class ITransactionService:
    def procesar_transacciones(self, transactions: Transaction, account: Account):
        pass
    
    def listar_transacciones(self, cuenta_id: UUID) -> List[Transaction]:
        pass
