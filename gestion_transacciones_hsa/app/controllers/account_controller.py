from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from decimal import Decimal
from domain.entities.account import Account
from infrastructure.repositories.sqlite_account_repository import SQLiteAccountRepository

# Crear el router
router = APIRouter()

def get_account_repository() -> SQLiteAccountRepository:
    from app.main import account_repository
    return account_repository

@router.post("/cuentas/")
def crear_cuenta(
    cuenta_json: dict,
    account_repository: SQLiteAccountRepository = Depends(get_account_repository)
):
    """
    Crea una nueva cuenta en la base de datos.
    Genera automáticamente 'id' y 'usuario_id' si no se proporcionan.
    """
    try:
        # Generar 'id' automáticamente si no se proporciona
        cuenta_id = uuid4()

        # Generar 'usuario_id' automáticamente si no se proporciona
        usuario_id = uuid4()

        # Convertir JSON a entidad Account
        nueva_cuenta = Account(
            id=cuenta_id,
            usuario_id=usuario_id,
            saldo=Decimal(str(cuenta_json.get("saldo", 0.00))),
            limite_diario=Decimal(str(cuenta_json.get("limite_diario", 2000.00)))
        )

        # Guardar la cuenta en la base de datos
        account_repository.guardar(nueva_cuenta)
        return {"message": "Cuenta creada con éxito", "cuenta_id": str(nueva_cuenta.id), "usuario_id": str(nueva_cuenta.usuario_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
