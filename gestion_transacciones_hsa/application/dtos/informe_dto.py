from typing import List
from decimal import Decimal
from .transaction_dto import TransactionDTO

class InformeDTO:
    def __init__(
        self,
        total_depositos: Decimal,
        total_retiros: Decimal,
        saldo_promedio: Decimal,
        transacciones: List[TransactionDTO]
    ):
        self.total_depositos = total_depositos
        self.total_retiros = total_retiros
        self.saldo_promedio = saldo_promedio
        self.transacciones = transacciones

    def __repr__(self):
        return f"InformeDTO(total_depositos={self.total_depositos}, total_retiros={self.total_retiros}, saldo_promedio={self.saldo_promedio}, transacciones={self.transacciones})"
