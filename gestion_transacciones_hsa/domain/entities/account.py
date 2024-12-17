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
        Verifica que el monto no exceda el límite diario permitido.
        """
        if abs(monto) > self.limite_diario:
            raise ValueError("El monto excede el límite diario permitido.")
