class CuentaHSA:
    def __init__(self, id_cuenta, id_usuario, saldo, limite_retiro):
        self.id_cuenta = id_cuenta
        self.id_usuario = id_usuario
        self.saldo = saldo
        self.limite_retiro = limite_retiro

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
        else:
            raise ValueError("El monto del depósito debe ser positivo")

    def retirar(self, monto):
        if monto > 0:
            if monto <= self.limite_retiro <= self.saldo:
                self.saldo -= monto
            else:
                raise ValueError("El monto del retiro excede el límite o el saldo disponible")
        else:
            raise ValueError("El monto del retiro debe ser positivo")

    def obtener_saldo(self):
        return self.saldo

    def establecer_limite_retiro(self, nuevo_limite):
        if nuevo_limite > 0:
            self.limite_retiro = nuevo_limite
        else:
            raise ValueError("El límite de retiro debe ser positivo")
        
    
    def actualizar_saldo(self, monto):
        self.saldo += monto

    def verificar_limite(self, monto):
        return monto <= self.limite_retiro