from fastapi import APIRouter, HTTPException, Depends
from application.services.transaction_application_service import TransactionApplicationService
from app.mappers.transaction_mapper import TransactionMapper
from application.dtos.transaction_dto import TransactionDTO
from uuid import UUID, uuid4
from typing import List
from application.dtos.informe_dto import InformeDTO

# Crear el router para las rutas relacionadas con transacciones
router = APIRouter()

# Función para obtener la instancia del servicio de aplicación desde main.py
def get_transaction_app_service() -> TransactionApplicationService:
    from gestion_transacciones_hsa.app.main import transaction_app_service
    return transaction_app_service

@router.post("/transacciones/")
def realizar_transaccion(
    transaction_json: dict,
    transaction_app_service: TransactionApplicationService = Depends(get_transaction_app_service)
):
    """
    Realiza una transacción.
    Si no se proporciona un ID, se genera automáticamente.
    """
    try:
        # Generar automáticamente el ID de la transacción si no se proporciona
        transaction_id = transaction_json.get("id", str(uuid4()))
        transaction_json["id"] = transaction_id

        # Convertir JSON a DTO
        transaction_dto = TransactionMapper.json_to_dto(transaction_json)
        transaction_app_service.realizar_transaccion(transaction_dto)
        return {"message": "Transacción realizada con éxito", "transaction_id": transaction_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transacciones/{cuenta_id}", response_model=List[dict])
def listar_transacciones(
    cuenta_id: UUID,
    transaction_app_service: TransactionApplicationService = Depends(get_transaction_app_service)
):
    """
    Lista todas las transacciones de una cuenta específica.
    """
    try:
        transacciones = transaction_app_service.listar_transacciones(cuenta_id)
        return [TransactionMapper.dto_to_json(t) for t in transacciones]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
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
        informe: InformeDTO = transaction_app_service.generar_informe_financiero(cuenta_id)
        return {
            "total_depositos": float(informe.total_depositos),
            "total_retiros": float(informe.total_retiros),
            "saldo_promedio": float(informe.saldo_promedio),
            "transacciones": [TransactionMapper.dto_to_json(t) for t in informe.transacciones]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
