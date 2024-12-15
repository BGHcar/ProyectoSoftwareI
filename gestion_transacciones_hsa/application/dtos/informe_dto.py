class InformeDTO:
    def __init__(self, ingresos, egresos, balance):
        self.ingresos = ingresos
        self.egresos = egresos
        self.balance = balance

    def __repr__(self):
        return f"InformeDTO(ingresos={self.ingresos}, egresos={self.egresos}, balance={self.balance})"