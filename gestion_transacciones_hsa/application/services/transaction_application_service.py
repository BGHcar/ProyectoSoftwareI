from application.dtos.transaction_dto import TransactionDTO
from application.dtos.informe_dto import InformeDTO
from gestion_transacciones_hsa.domain.repositories.i_transaction_repository import ITransactionRepository
from domain.repositories.i_account_repository import IAccountRepository
from domain.services.transaction_service import TransactionService
from uuid import UUID
from typing import List
from decimal import Decimal


class TransactionApplicationService:
    def __init__(
        self,
        transaction_service: TransactionService,
        account_repository: IAccountRepository,
    ):
        self.transaction_service = transaction_service
        self.account_repository = account_repository

    def realizar_transaccion(self, dto: TransactionDTO):
        cuenta = self.account_repository.obtener_por_id(dto.cuenta_id)
        if not cuenta:
            raise ValueError("La cuenta no existe.")
        return self.transaction_service.procesar_transaccion(dto)


    def listar_transacciones(self, cuenta_id: UUID) -> List[TransactionDTO]:
        transacciones = self.transaction_service.listar_transacciones_por_cuenta(cuenta_id)
        return [TransactionDTO.from_entity(t) for t in transacciones]

    def generar_informe_financiero(self, cuenta_id: UUID) -> InformeDTO:
        cuenta = self.account_repository.obtener_por_id(cuenta_id)
        if not cuenta:
            raise ValueError("La cuenta no existe.")
        transacciones = self.transaction_service.listar_transacciones_por_cuenta(cuenta_id)

        total_depositos = Decimal("0")
        total_retiros = Decimal("0")
        for t in transacciones:
            if t.tipo == "DEPOSITO":
                total_depositos += t.monto
            elif t.tipo == "RETIRO":
                total_retiros += t.monto

        saldo_promedio = cuenta.saldo / len(transacciones) if transacciones else cuenta.saldo

        return InformeDTO(
            total_depositos=total_depositos,
            total_retiros=total_retiros,
            saldo_promedio=saldo_promedio,
            transacciones=len(transacciones),
        )
