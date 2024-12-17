from application.dtos.transaction_dto import TransactionDTO
from application.dtos.informe_dto import InformeDTO
import domain.repositories.i_transaction_service as ITransactionService
import domain.repositories.i_account_repository as IAccountRepository
from uuid import UUID
from typing import List
from decimal import Decimal


'''
La Capa de Aplicación en una arquitectura basada en Domain-Driven Design (DDD) actúa
como un intermediario entre la capa de presentación (o servicios REST) y la capa de dominio.
Su principal responsabilidad es coordinar y orquestar las operaciones del sistema,
implementando los casos de uso definidos por el negocio sin contener lógica de negocio
propia.
Componentes Principales:
1. Servicios de Aplicación:
o TransactionApplicationService: Gestiona casos de uso como realizar
transacciones y generar informes financieros. Este servicio interactúa con los
servicios de dominio y otros componentes necesarios para cumplir con las
operaciones solicitadas.

'''



class TransactionApplicationService():
    def __init__(
        self, 
        transaction_service: ITransactionService, 
        account_repository: IAccountRepository
        ):
        self.transaction_service = transaction_service
        self.account_repository = account_repository


    def realizar_transaccion(self, dto: TransactionDTO):
        """
        Realiza una transacción a partir de un DTO con los datos de la transacción.
        """
        # Validar que la cuenta existe
        cuenta = self.account_repository.obtener_por_usuario(dto.cuenta_id)
        
        if not cuenta:
            raise ValueError("La cuenta no existe")

        # Realizar la transacción usando el servicio de dominio
        return self.transaction_service.realizar_transaccion(dto)

    def listar_transacciones(self, cuenta_id: UUID) -> List[TransactionDTO]:
        """
        Lista todas las transacciones asociadas a una cuenta específica.
        Args:
            cuenta_id: UUID de la cuenta
        Returns:
            List[TransactionDTO]: Lista de transacciones
        """
        cuenta = self.account_repository.obtener_por_usuario(cuenta_id)
        if not cuenta:
            raise ValueError("La cuenta no existe")
            
        return self.transaction_service.listar_transacciones(cuenta_id)

    def generar_informe_financiero(self, cuenta_id: UUID) -> InformeDTO:
        """
        Genera un informe financiero de una cuenta específica utilizando los datos
        básicos proporcionados por el servicio de dominio.
        Args:
            cuenta_id: UUID de la cuenta
        Returns:
            InformeDTO: Informe financiero de la cuenta
        """
        cuenta = self.account_repository.obtener_por_usuario(cuenta_id)
        if not cuenta:
            raise ValueError("La cuenta no existe")
            
        transacciones = self.transaction_service.listar_transacciones(cuenta_id)
        
        # Calcular totales a partir de las transacciones
        total_depositos = Decimal('0')
        total_retiros = Decimal('0')
        saldo_actual = Decimal('0')
        
        for transaccion in transacciones:
            monto = Decimal(str(transaccion.monto))
            if transaccion.tipo in ['DEPOSITO', 'TRANSFERENCIA_RECIBIDA']:
                total_depositos += monto
                saldo_actual += monto
            elif transaccion.tipo in ['RETIRO', 'TRANSFERENCIA_ENVIADA']:
                total_retiros += monto
                saldo_actual -= monto
        
        # Calcular saldo promedio usando el saldo actual
        saldo_promedio = saldo_actual / Decimal(str(len(transacciones))) if transacciones else Decimal('0')
        
        return InformeDTO(
            total_depositos=total_depositos,
            total_retiros=total_retiros,
            saldo_promedio=saldo_promedio,
            transacciones=transacciones
        )