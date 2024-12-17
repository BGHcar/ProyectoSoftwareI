# domain/entities/user.py

from uuid import UUID
from typing import List, Optional
from gestion_transacciones_hsa.domain.entities.account import Account
class User:
    def __init__(
        self,
        id: UUID,
        nombre: str,
        correo: str,
        telefono: str,
        accounts: Optional[List[Account]] = None
    ):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.accounts = accounts if accounts is not None else []

    def agregar_cuenta(self, account: Account):
        """
        Agrega una cuenta a la lista de cuentas del usuario.
        """
        if not isinstance(account, Account):
            raise ValueError("El objeto proporcionado no es una instancia de Account.")
        self.accounts.append(account)

    def listar_cuentas(self) -> List[Account]:
        """
        Retorna la lista de cuentas asociadas al usuario.
        """
        return self.accounts

    def notificar(self, mensaje: str):
        """
        Envía una notificación al usuario.
        Actualmente, simplemente imprime el mensaje en la consola.
        """
        print(f"Se ha enviado un mensaje al usuario {self.nombre}: {mensaje}")
