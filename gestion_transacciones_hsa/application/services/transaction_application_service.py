import logging
from application.dtos.transaction_dto import TransactionDTO
from application.dtos.informe_dto import InformeDTO
from domain.repositories.i_transaction_repository import ITransactionRepository
from domain.repositories.i_account_repository import IAccountRepository
from domain.services.transaction_service import TransactionService
from uuid import UUID
from typing import List
from decimal import Decimal
from domain.entities.transaction_type import TransactionType
from domain.entities.transaction import TransactionState

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TransactionApplicationService:
    def __init__(
        self,
        transaction_service: TransactionService,
        account_repository: IAccountRepository,
    ):
        self.transaction_service = transaction_service
        self.account_repository = account_repository

    def realizar_transaccion(self, dto: TransactionDTO):
        try:
            logger.debug(f"Procesando transacción - ID: {dto.id}, Tipo: {dto.tipo}, Estado: {dto.estado}")
            logger.debug(f"Iniciando proceso de transacción con DTO: {dto}")
            cuenta = self.account_repository.obtener_por_id(dto.cuenta_id)
            if not cuenta:
                raise ValueError("La cuenta no existe.")
            return self.transaction_service.procesar_transaccion(dto)
            logger.debug("Transacción completada exitosamente")
        except Exception as e:
            logger.error(f"Error en realizar_transaccion: {str(e)}", exc_info=True)
            raise

    def listar_transacciones(self, cuenta_id: UUID) -> List[TransactionDTO]:
        try:
            logger.debug(f"Application Service: Iniciando listado de transacciones para cuenta {cuenta_id}")
            
            # Verificar si la cuenta existe
            cuenta = self.account_repository.obtener_por_id(cuenta_id)
            if not cuenta:
                logger.error(f"Cuenta no encontrada: {cuenta_id}")
                raise ValueError(f"La cuenta {cuenta_id} no existe")
                
            transacciones = self.transaction_service.listar_transacciones_por_cuenta(cuenta_id)
            logger.debug(f"Transacciones recuperadas: {len(transacciones)}")
            
            dtos = [TransactionDTO.from_entity(t) for t in transacciones]
            logger.debug(f"DTOs creados: {len(dtos)}")
            
            return dtos
            
        except Exception as e:
            logger.error(f"Error en listar_transacciones: {str(e)}", exc_info=True)
            raise

    def generar_informe_financiero(self, cuenta_id: UUID) -> InformeDTO:
        try:
            cuenta = self.account_repository.obtener_por_id(cuenta_id)
            if not cuenta:
                raise ValueError("La cuenta no existe.")
            
            logger.debug("Obteniendo transacciones de la cuenta...")
            transacciones = self.transaction_service.listar_transacciones_por_cuenta(cuenta_id)
            
            logger.debug("Calculando totales de transacciones APROBADAS...")
            num_depositos = 0
            num_retiros = 0
            total_monto_depositos = Decimal("0")
            total_monto_retiros = Decimal("0")

            for t in transacciones:
                logger.debug(f"Procesando transacción: tipo={t.tipo}, estado={t.estado}, monto={t.monto}")
                if t.estado == TransactionState.APROBADA:
                    if t.tipo == TransactionType.DEPOSITO:
                        num_depositos += 1
                        total_monto_depositos += t.monto
                        logger.debug(f"Sumando depósito: monto={t.monto}, total_depositos={total_monto_depositos}")
                    elif t.tipo == TransactionType.RETIRO:
                        num_retiros += 1
                        total_monto_retiros += t.monto
                        logger.debug(f"Sumando retiro: monto={t.monto}, total_retiros={total_monto_retiros}")

            # Calcular saldo promedio considerando los montos
            saldo_acumulado = total_monto_depositos - total_monto_retiros
            transacciones_aprobadas = num_depositos + num_retiros
            saldo_promedio = (saldo_acumulado / transacciones_aprobadas 
                            if transacciones_aprobadas > 0 
                            else Decimal("0"))

            logger.debug(f"Totales finales: Num. Depósitos={num_depositos}, Num. Retiros={num_retiros}")
            logger.debug(f"Montos totales: Depósitos={total_monto_depositos}, Retiros={total_monto_retiros}")
            logger.debug(f"Saldo promedio calculado: {saldo_promedio}")
            
            dtos = [TransactionDTO.from_entity(t) for t in transacciones]

            return InformeDTO(
                total_depositos=num_depositos,
                total_retiros=num_retiros,
                saldo_promedio=saldo_promedio,
                transacciones=dtos
            )
        except Exception as e:
            logger.error(f"Error generando informe financiero: {str(e)}", exc_info=True)
            raise
