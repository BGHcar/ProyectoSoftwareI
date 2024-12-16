class InformeDTO:
    def __init__(self, total_depositos: float, total_retiros: float, saldo_promedio: float, transacciones: float):
            self.total_depositos = total_depositos
            self.total_retiros = total_retiros
            self.saldo_promedio = saldo_promedio
            self.transacciones = transacciones
            
    def __repr__(self):
        return f"InformeDTO(total_depositos={self.total_depositos}, total_retiros={self.total_retiros}, saldo_promedio={self.saldo_promedio}, trasacciones={self.transacciones})"
    