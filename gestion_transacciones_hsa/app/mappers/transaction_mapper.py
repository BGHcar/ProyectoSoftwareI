from decimal import Decimal
from domain.entities.transaction_type import TransactionType
from application.dtos.transaction_dto import TransactionDTO
from datetime import datetime
import logging
from uuid import UUID

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TransactionMapper:
    @staticmethod
    def json_to_dto(data: dict) -> TransactionDTO:
        try:
            logger.debug(f"Iniciando mapeo de JSON a DTO con datos: {data}")
            
            # Convertir strings a tipos apropiados
            id_trans = UUID(data["id"]) if isinstance(data["id"], str) else data["id"]
            cuenta_id = UUID(data["cuenta_id"]) if isinstance(data["cuenta_id"], str) else data["cuenta_id"]
            monto = Decimal(str(data["monto"]))
            fecha = datetime.strptime(data["fecha"], "%Y-%m-%d") if isinstance(data["fecha"], str) else data["fecha"]
            
            # Asegurarse de que el tipo sea TransactionType
            tipo = TransactionType.from_string(data["tipo"])
            logger.debug(f"Tipo convertido: {tipo.name}")
            
            dto = TransactionDTO(
                id=id_trans,
                cuenta_id=cuenta_id,
                monto=monto,
                tipo=tipo,
                estado=data["estado"],
                fecha=fecha
            )
            logger.debug(f"DTO creado exitosamente: {dto}")
            return dto
            
        except Exception as e:
            logger.error(f"Error en el mapeo: {str(e)}", exc_info=True)
            raise ValueError(f"Error en el mapeo: {str(e)}")

    @staticmethod
    def dto_to_json(dto: TransactionDTO) -> dict:
        return {
            "id": str(dto.id),
            "cuenta_id": str(dto.cuenta_id),
            "monto": float(dto.monto),
            "tipo": dto.tipo.name,
            "estado": dto.estado,
            "fecha": dto.fecha.strftime("%Y-%m-%d")
        }
