from decimal import Decimal
from domain.entities.transaction_type import TransactionType
from application.dtos.transaction_dto import TransactionDTO

class TransactionMapper:
    @staticmethod
    def json_to_dto(data: dict) -> TransactionDTO:
        try:
            print(f"Recibido tipo: {data['tipo']}")  # Depuración
            tipo = TransactionType(data["tipo"].lower())
            print(f"Mapeado tipo a TransactionType: {tipo}")  # Depuración
            monto = Decimal(data["monto"])
        except Exception as e:
            raise ValueError(f"Error procesando tipo o monto: {e}")

        return TransactionDTO(
            id=data["id"],
            cuenta_id=data["cuenta_id"],
            monto=monto,
            tipo=tipo,
            estado=data["estado"],
            fecha=data["fecha"]
        )
