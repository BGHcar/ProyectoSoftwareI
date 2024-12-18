# domain/entities/transaction_type.py

from enum import Enum
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TransactionType(Enum):
    DEPOSITO = "DEPOSITO"
    RETIRO = "RETIRO"

    @classmethod
    def from_string(cls, value: str):
        try:
            logger.debug(f"Intentando convertir valor '{value}' a TransactionType")
            normalized_value = value.upper()
            logger.debug(f"Valor normalizado: '{normalized_value}'")
            
            for tipo in cls:
                if tipo.value == normalized_value:
                    logger.debug(f"Valor identificado como {tipo.name}")
                    return tipo
                    
            error_msg = f"Tipo de transacción no válido: {value}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        except Exception as e:
            error_msg = f"Error al procesar el tipo de transacción: {value}. Error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise ValueError(error_msg)

    @property
    def descripcion(self) -> str:
        descripciones = {
            TransactionType.DEPOSITO: "Agrega dinero a la cuenta HSA del usuario.",
            TransactionType.RETIRO: "Reduce el saldo de la cuenta HSA del usuario dentro de los límites establecidos."
        }
        return descripciones[self]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @property
    def value(self):
        return super().value

