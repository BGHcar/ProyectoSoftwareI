<<<<<<< HEAD
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
=======
# domain/entities/account.py
from uuid import UUID
from decimal import Decimal

class Account:
    def __init__(
        self,
        id: UUID,
        usuario_id: UUID,
        saldo: Decimal,
        limite_diario: Decimal
    ):
        if not self._is_valid_uuid(id) or not self._is_valid_uuid(usuario_id):
            raise ValueError("UUID mal formado.")
        self.id = id
        self.usuario_id = usuario_id
        self.saldo = saldo
        self.limite_diario = limite_diario

    @staticmethod
    def _is_valid_uuid(uuid_to_test, version=4):
        try:
            uuid_obj = UUID(str(uuid_to_test), version=version)
        except ValueError:
            return False
        return str(uuid_obj) == str(uuid_to_test)

    @classmethod
    def from_dict(cls, data):
        id_key = "_id" if "_id" in data else "id"
        return cls(
            id=UUID(data[id_key]),
            usuario_id=UUID(data["usuario_id"]),
            saldo=Decimal(str(data["saldo"])),
            limite_diario=Decimal(str(data["limite_diario"]))
        )

    def actualizar_saldo(self, monto: Decimal):
        """
        Actualiza el saldo de la cuenta.
        Permite realizar depósitos (monto positivo) o retiros (monto negativo).
        """
        if not isinstance(monto, Decimal):
            raise ValueError("El monto debe ser de tipo Decimal.")
        self.saldo += monto

    def verificar_limite_diario(self, monto: Decimal):
        """
        Verifica que un monto no exceda el límite diario permitido.
        """
        if not isinstance(monto, Decimal):
            raise ValueError("El monto debe ser de tipo Decimal.")
        if abs(monto) > self.limite_diario:
            raise ValueError("El monto excede el límite diario de la cuenta.")
>>>>>>> origin/bryan
