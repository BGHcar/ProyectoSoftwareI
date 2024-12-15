class TransaccionDTO:
    def __init__(self, id_transaccion: int, monto: float, tipo_transaccion: str, fecha: str):
        self.id_transaccion = id_transaccion
        self.monto = monto
        self.tipo_transaccion = tipo_transaccion
        self.fecha = fecha

    def __repr__(self):
        return f"TransaccionDTO(id_transaccion={self.id_transaccion}, monto={self.monto}, tipo_transaccion='{self.tipo_transaccion}', fecha='{self.fecha}')"
