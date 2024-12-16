import domain.repositories.i_transaction_service as i_transaction_service
import domain.repositories.i_account_repository as i_account_repository



class TransactionApplicationService():
    def __init__(self, transaction_service: i_transaction_service.ITransactionService, account_repository: i_account_repository.IAccountRepository):
        self.transaction_service = transaction_service
        self.account_repository = account_repository


        def realizar_transaccion(self, dto):
            # Lógica para realizar una transacción usando el servicio de transacciones
            
            # Crear la transaccion 
            transaccion = self.transaction_service.crear_transaccion(dto)
            # Actualizar el balance de la cuenta
            self.account_repository.actualizar_balance(transaccion)
            return "Transacción completada con éxito."
        
        def listar_transacciones(self, cuenta_id):
            # Lógica para listar transacciones de una cuenta específica
            # Obtener las transacciones asociadas a la cuenta
            transacciones = self.transaction_service.obtener_transacciones_por_cuenta(cuenta_id)
            return transacciones
        
        def generar_informe_financiero(self, cuenta_id):
            # Lógica para generar un informe financiero para una cuenta específica
            # Obtener las transacciones de la cuenta
            transacciones = self.transaction_service.obtener_transacciones_por_cuenta(cuenta_id)
            # Generar el informe usando el generador de informes
            informe = self.generador_informes.generar(transacciones)
            return informe
