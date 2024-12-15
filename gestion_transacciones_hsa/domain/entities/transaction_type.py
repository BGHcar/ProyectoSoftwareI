# domain/entities/transaction_type.py

from enum import Enum

class TransactionType(Enum):
    DEPOSITO = "deposito"
    RETIRO = "retiro"

    @property
    def descripcion(self) -> str:
        descripciones = {
            "deposito": "Agrega dinero a la cuenta HSA del usuario.",
            "retiro": "Reduce el saldo de la cuenta HSA del usuario dentro de los límites establecidos."
        }
        return descripciones[self.value]

    @property
    def nombre(self) -> str:
        return self.value

