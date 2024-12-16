from uuid import UUID
from datetime import datetime

class TransactionDTO:
    def __init__(self, id: UUID, cuenta_id: UUID, monto: float, tipo: str, estado: str, fecha: datetime):
        self.id = id
        self.cuenta_id = cuenta_id
        self.monto = monto
        self.tipo = tipo
        self.estado = estado
        self.fecha = fecha

    def __repr__(self):
        return f"TransactionDTO(id={self.id}, cuenta_id={self.cuenta_id}, monto={self.monto}, tipo='{self.tipo}', estado='{self.estado}', fecha='{self.fecha}')"
    