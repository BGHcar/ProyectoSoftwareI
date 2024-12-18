from fastapi import APIRouter, HTTPException, Depends
from application.services.transaction_application_service import TransactionApplicationService
from app.mappers.transaction_mapper import TransactionMapper
from application.dtos.transaction_dto import TransactionDTO
from uuid import UUID, uuid4
from typing import List
from application.dtos.informe_dto import InformeDTO
from pydantic import BaseModel
from datetime import datetime
import logging
from domain.entities.transaction import TransactionState

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Crear el router para las rutas relacionadas con transacciones
router = APIRouter()

# Función para obtener la instancia del servicio de aplicación desde main.py
def get_transaction_app_service() -> TransactionApplicationService:
    from app.main import transaction_app_service
    return transaction_app_service

def get_mongo_transaction_service():
    from app.main import mongo_transaction_service
    return mongo_transaction_service

class TransactionRequest(BaseModel):
    cuenta_id: UUID
    monto: float
    tipo: str
    estado: str
    fecha: str

@router.post("/transacciones/")
def realizar_transaccion(
    transaction_request: TransactionRequest,
    transaction_app_service: TransactionApplicationService = Depends(get_transaction_app_service),
    mongo_service = Depends(get_mongo_transaction_service)
):
    """
    Realiza una transacción.
    Espera un objeto TransactionRequest con los campos necesarios.
    """
    try:
        logger.debug(f"Iniciando procesamiento de transacción con request: {transaction_request}")
        
        # Validar estado antes de procesar
        estado = transaction_request.estado.upper()
        try:
            TransactionState(estado)
        except ValueError:
            estados_validos = [e.value for e in TransactionState]
            raise ValueError(f"Estado inválido. Estados válidos: {estados_validos}")
            
        transaction_json = {
            "id": str(uuid4()),
            "cuenta_id": transaction_request.cuenta_id,  # Ya es UUID, no necesita conversión
            "monto": float(transaction_request.monto),
            "tipo": transaction_request.tipo.upper(),
            "estado": estado,
            "fecha": transaction_request.fecha
        }
        logger.debug(f"JSON creado: {transaction_json}")

        # Validar los campos requeridos
        if not all([transaction_json["cuenta_id"], transaction_json["monto"], 
                   transaction_json["tipo"], transaction_json["estado"]]):
            logger.error("Campos requeridos faltantes")
            raise ValueError("Todos los campos son requeridos")

        logger.debug("Convirtiendo JSON a DTO...")
        transaction_dto = TransactionMapper.json_to_dto(transaction_json)
        logger.debug(f"DTO creado exitosamente: {transaction_dto}")
        
        logger.debug("Realizando transacción...")
        transaction_app_service.realizar_transaccion(transaction_dto)  # SQLite
        
        try:
            # Convertir DTO a entidad para MongoDB
            transaction_entity = TransactionMapper.dto_to_entity(transaction_dto)
            logger.debug(f"Intentando guardar en MongoDB: {transaction_entity}")
            mongo_service.procesar_transaccion(transaction_entity)
            logger.debug("Transacción guardada exitosamente en MongoDB")
        except Exception as e:
            logger.error(f"Error al guardar en MongoDB: {str(e)}", exc_info=True)
            # Continuar aunque falle MongoDB
        
        logger.debug("Transacción completada exitosamente")
        
        return {"message": "Transacción realizada con éxito", 
                "transaction_id": transaction_json["id"]}
                
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Agregar logging del error real
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, 
                          detail=f"Error interno del servidor: {str(e)}")

@router.get("/transacciones/{cuenta_id}", response_model=List[dict])
def listar_transacciones(
    cuenta_id: UUID,
    transaction_app_service: TransactionApplicationService = Depends(get_transaction_app_service)
):
    """
    Lista todas las transacciones de una cuenta específica.
    """
    try:
        logger.debug(f"Iniciando listado de transacciones para cuenta_id: {cuenta_id}")
        logger.debug(f"Usando servicio: {transaction_app_service}")
        
        transacciones = transaction_app_service.listar_transacciones(cuenta_id)
        logger.debug(f"Transacciones recuperadas: {transacciones}")
        
        resultado = [TransactionMapper.dto_to_json(t) for t in transacciones]
        logger.debug(f"Transacciones convertidas a JSON: {resultado}")
        
        return resultado
    except ValueError as e:
        logger.error(f"Error de validación al listar transacciones: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado al listar transacciones: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/informes/{cuenta_id}", response_model=dict)
def generar_informe_financiero(
    cuenta_id: UUID,
    transaction_app_service: TransactionApplicationService = Depends(get_transaction_app_service)
):
    """
    Genera un informe financiero de una cuenta específica.
    """
    try:
        logger.debug(f"Iniciando generación de informe para cuenta_id: {cuenta_id}")
        logger.debug(f"Usando servicio: {transaction_app_service}")
        
        informe: InformeDTO = transaction_app_service.generar_informe_financiero(cuenta_id)
        logger.debug(f"Informe generado: {informe}")
        
        resultado = {
            "total_depositos": float(informe.total_depositos),
            "total_retiros": float(informe.total_retiros),
            "saldo_promedio": float(informe.saldo_promedio),
            "transacciones": [TransactionMapper.dto_to_json(t) for t in informe.transacciones]
        }
        logger.debug(f"Informe convertido a JSON: {resultado}")
        
        return resultado
    except ValueError as e:
        logger.error(f"Error de validación al generar informe: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado al generar informe: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
