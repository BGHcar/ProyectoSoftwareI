from uuid import UUID
from typing import List

class IRepository:
    def __init__(self):
        pass

    def guardar(self, entidad: object):
        pass
    
    def obtener_por_id(self, id: UUID) -> object:
        pass
    def listar_todos(self) -> List[object]:
        pass